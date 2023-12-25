import os
from pathlib import Path
import shutil
from typing import cast
import tempfile

import pandas as pd
from PySide6.QtCore import QModelIndex, Qt
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox, QWidget

from OPEs_ID.expr import ChemFormula
from OPEs_ID.metfrag import MetFragParameter

from ..calc.metfrag import MetfragThread
from ..config import config as CONFIG
from ..const_name import ColumnNames as C
from ..dataframe_table import DataFrameModel, ExtraProperty
from ..dialogs.MetfragConfigDialog import MetfragConfigDialog
from ..dialogs.ProgressDialog import ProgressDialog
from .ResultPage_ui import Ui_ResultPage


def chargedToNeutralFormula(f: ChemFormula):
    from OPEs_ID.elements.table import H1

    e = f.copy()
    e[H1] -= e.charge
    e.charge = 0
    return e


def _count_metfrag(data):
    if isinstance(data, pd.DataFrame):
        return str(data.shape[0])
    else:
        return "error"


def save_metfrag_result(results: pd.DataFrame, savedir: Path):
    from collections import namedtuple

    from OPEs_ID.metfrag.output import to_excel_with_mol_img
    from OPEs_ID.metfrag.run import MetFragFailed

    savedir.mkdir(exist_ok=True)
    NoResultEntry = namedtuple(
        "NoResultEntry",
        ["RT", "Precursor", "formula", "comments", "webcode", "stdout", "stderr"],
    )
    no_results = []
    for idx in results.index:
        rt = results.at[idx, C.RT]
        precursor_mz = results.at[idx, C.PrecursorMZ]
        formula = results.at[idx, C.Formula]
        metfrag_result: pd.DataFrame | MetFragFailed = results.at[idx, C.MetfragResults]
        param: MetFragParameter = results.at[idx, C.MetfragParams]
        if isinstance(metfrag_result, MetFragFailed):
            no_results.append(
                NoResultEntry(
                    rt,
                    precursor_mz,
                    formula,
                    None,
                    metfrag_result.returncode,
                    metfrag_result.stdout,
                    metfrag_result.stderr,
                )
            )
        else:
            if metfrag_result.size == 0:
                no_results.append(
                    NoResultEntry(
                        rt,
                        precursor_mz,
                        param.NeutralPrecursorMolecularFormula,
                        "No Valid",
                        None,
                        None,
                        None,
                    )
                )
            else:
                to_excel_with_mol_img(
                    metfrag_result,
                    fname=savedir / f"{precursor_mz:.4f}_{rt:.4f}_{formula}.xlsx",
                    metfrag_param=param,
                )

    if len(no_results) != 0:
        pd.DataFrame(no_results).to_excel(savedir / "no_results.xlsx")


def make_metfrag_params(output1_results: pd.DataFrame, configs=None):
    target_ions = CONFIG["target_ion.ions"]
    metfrag_params = []
    temp_dir = configs["temp_dir"]
    for (
        idx,
        ms2_idx,
        precursor_mz,
        formula,
        mz_spec,
        int_spec,
        is_tri,
    ) in output1_results[
        [C.MS2IDX, C.PrecursorMZ, C.Formula, C.SpecMZ, C.SpecINT, C.IsTriester]
    ].itertuples():
        neutral_formula = chargedToNeutralFormula(formula).monoisotopic_formula()
        p = MetFragParameter()
        p.NeutralPrecursorMolecularFormula = neutral_formula
        p.PeakListString = ";".join(f"{a}_{b}" for (a, b) in zip(mz_spec, int_spec))
        p.IonizedPrecursorMass = precursor_mz
        p.MaximumTreeDepth = configs["max_tree_depth"]
        p.MetFragDatabaseType = configs["db_type"]
        if configs["db_type"] in ["LocalCSV", "LocalSDF"]:
            p.LocalDatabasePath = configs["db_path"]

        smarts_list = []
        if configs["constraints.fragment"]:
            if is_tri:
                smarts_list.append("[#6]-O-P(=O)(-O-[#6])-O-[#6]")
            else:
                smarts_list.append("[HO]-P(=O)(-O)-O-[#6]")

        if configs["constraints.ester_type"]:
            for ion in target_ions:
                if output1_results.at[idx, ion.refname]:
                    smarts_list.append(ion.smarts)

        p.FilterSmartsInclusionList = smarts_list
        p.MetFragPreProcessingCandidateFilter = ["UnconnectedCompoundFilter"]
        if len(p.FilterSmartsInclusionList) != 0:
            p.MetFragPreProcessingCandidateFilter.append(
                "SmartsSubstructureInclusionFilter"
            )
        p.MetFragScoreTypes = "FragmenterScore"
        p.MetFragScoreWeights = 1
        p.ResultsPath = temp_dir / "compute_dir"
        p.SampleName = rf"{ms2_idx}_{neutral_formula}_{precursor_mz}"
        p.m_ParamSavePath = (
            temp_dir
            / "param_dir"
            / f"{ms2_idx}_{neutral_formula}_{precursor_mz}_param.txt"
        )

        metfrag_params.append(p)
    return metfrag_params


class ResultPage(QWidget):
    DIALOGS = {}

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ResultPage()
        self.ui.setupUi(self)

        self.ui.metfragButton.clicked.connect(self.calcMetfrag)
        self.ui.saveButton.clicked.connect(self.saveResults)

        self.ui.resultsTableView.doubleClicked.connect(self.showItemDetail)

    def setGeneralResult(self, result: pd.DataFrame):
        model = DataFrameModel(
            result,
            extra_prop={C.Formula: ExtraProperty.ChemicalFormula},
            hide_columns=[C.SpecMZ, C.SpecINT],
        )
        self.ui.resultsTableView.setModel(model)

    def showItemDetail(self, index: QModelIndex):
        from ..dialogs.MetfragResultDialog import MetfragResultDialog

        model = cast(DataFrameModel, index.model())
        row = index.row()
        if C.MetfragResults in model._data.columns:
            data = model._data.at[row, C.MetfragResults]
            if isinstance(data, pd.DataFrame):
                data = data.copy()
                data.insert(0, "Mol", data["InChI"])
                dialog = MetfragResultDialog.fromDataFrame(
                    data, extra_prop={"Mol": ExtraProperty.MolSVG}
                )
                dialog.setModal(False)
                dialog.show()
                self.DIALOGS[id(dialog)] = dialog

                def delete():
                    del self.DIALOGS[id(dialog)]

                dialog.finished.connect(delete)

    def openMetfragConfigDialog(self):
        dialog = MetfragConfigDialog(CONFIG["metfrag"], self)
        
        if (code := dialog.exec()) == QDialog.Accepted:
            CONFIG["metfrag"] = dialog.configs()
            # for k, v in dialog.configs().items():
            #     CONFIG['metfrag.{k}'] = v
        return code

    def calcMetfrag(self):
        if self.openMetfragConfigDialog() == QDialog.Rejected:
            return

        from OPEs_ID.metfrag.config import RuntimeConfig

        RuntimeConfig.set_java_exe(CONFIG["metfrag.java_path"])

        model = cast(DataFrameModel, self.ui.resultsTableView.model())
        configs = CONFIG["metfrag"]
        if configs["temp_dir"] is None:
            tempdir = tempfile.TemporaryDirectory(prefix="OPEs-ID")
            configs["temp_dir"] = Path(tempdir.name)

        params = make_metfrag_params(model._data, configs)
        thread = MetfragThread(params, CONFIG["metfrag.n_job"], self)
        progress_dialog = ProgressDialog(["metfrag"], self)
        progress_dialog.updateDescription("metfrag", "Metfrag")
        thread.progressUpdate.connect(progress_dialog.updateProgress)
        thread.start()
        thread.calculationFinished.connect(progress_dialog.accept)  # TODO
        if progress_dialog.exec() == QDialog.Accepted:
            model.add_column(
                C.MetfragResults,
                thread.results,
                ExtraProperty.MetfragResult,
                column_rename="Metfrag Counts",
            )
            model.add_column(C.MetfragParams, params, hide=True)
        try:
            tempdir.cleanup()
        except:
            pass

    def saveResults(self):
        m = self.ui.resultsTableView.model()
        if isinstance(m, DataFrameModel):
            save_path, _ = QFileDialog.getSaveFileName(
                self, self.tr("Save Results"), "."
            )
            if save_path:
                save_path = Path(save_path)
                save_path = save_path.with_suffix(".xlsx")
                result = m._data.drop(
                    columns=[C.MS2IDX, C.MS2IDX, C.SpecMZ, C.SpecINT]
                ).sort_values([C.OPEClass, C.RT])
                if C.MetfragResults in m._data.columns:
                    metfrag_savedir = save_path.with_suffix(".metfrag")
                    if metfrag_savedir.exists():
                        if (
                            QMessageBox.warning(
                                self,
                                "Metfrag Save",
                                f"The Target Directory/File already exists.\n{metfrag_savedir} will be replaced.",
                                QMessageBox.Yes,
                                QMessageBox.No,
                            )
                            != QMessageBox.Yes
                        ):
                            return
                        if metfrag_savedir.is_dir():
                            shutil.rmtree(metfrag_savedir)
                        else:
                            os.remove(metfrag_savedir)
                    save_metfrag_result(result, metfrag_savedir)
                    result[C.MetfragResults] = result[C.MetfragResults].apply(
                        _count_metfrag
                    )
                result.set_index(
                    [
                        C.OPEClass,
                        C.RT,
                        C.PrecursorMZ,
                        C.PrecursorMS1Int,
                        C.Isotopes,
                        C.IsTriester,
                    ]
                ).to_excel(save_path)
        else:
            QMessageBox.warning(self, "No results", "No results to be saved.")


def save_metfrag_result(result_df: pd.DataFrame, savedir: Path):
    from collections import namedtuple
    from OPEs_ID.metfrag.run import MetFragFailed
    from OPEs_ID.metfrag.output import to_excel_with_mol_img

    savedir.mkdir(parents=True, exist_ok=True)
    NoResultEntry = namedtuple(
        "NoResultEntry",
        ["RT", "Procursor", "formula", "comments", "webcode", "stdout", "stderr"],
    )
    no_results = []
    for rt, precursor_mz, formula, param, metfrag_result in result_df.loc[
        :, [C.RT, C.PrecursorMZ, C.Formula, C.MetfragParams, C.MetfragResults]
    ].itertuples(index=False):
        if isinstance(metfrag_result, MetFragFailed):
            no_results.append(
                NoResultEntry(
                    rt,
                    precursor_mz,
                    formula,
                    None,
                    metfrag_result.returncode,
                    metfrag_result.stdout,
                    metfrag_result.stderr,
                )
            )
        else:
            if metfrag_result.size == 0:
                no_results.append(
                    NoResultEntry(
                        rt,
                        precursor_mz,
                        param.NeutralPrecursorMolecularFormula,
                        "No Valid",
                        None,
                        None,
                        None,
                    )
                )
            else:
                to_excel_with_mol_img(
                    metfrag_result,
                    fname=savedir / f"{precursor_mz:.4f}_{rt:.4f}_{formula}.xlsx",
                    metfrag_param=param,
                )

    if len(no_results) != 0:
        pd.DataFrame(no_results).to_excel(savedir / "no_results.xlsx")
