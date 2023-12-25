import joblib
import pandas as pd
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication

from OPEs_ID.defines import ColumnNames as _C
from OPEs_ID.elements.table import Cl, Cl35, Cl37, H1
from OPEs_ID.expr import ChemFormula
from OPEs_ID.formula import predict_formula
from OPEs_ID.io import load_mzml
from OPEs_ID.isotope_predict import predict_isotope
from OPEs_ID.ms2_tools import is_mass_in
from OPEs_ID.tools import ms2_ms1_roi, search_from_another_ms1
from OPEs_ID.utils import ProgressParallel
from .progress_adaptor import ProgressAdaptor
from ..config import config as CONFIG

from joblib.externals.loky import get_reusable_executor
 

class CancelError(RuntimeError):
    pass


@joblib.delayed
def get_formula(mz, Cl_isotope, is_Aryl, charge, mass_acc, lim_C, lim_H, lim_O, lim_DoU, lim_N, lim_P):
    isotope_expr = Cl_isotope
    if isotope_expr is None:
        n_Cl35 = 0
        n_Cl37 = 0
    else:
        n_Cl35 = isotope_expr[1][Cl35]
        n_Cl37 = isotope_expr[1][Cl37]
    if is_Aryl:
        min_DoU = 5
    else:
        min_DoU = 1

    if min(lim_DoU) < min_DoU:
        lim_DoU = [x for x in lim_DoU if x >= min_DoU]
    else:
        lim_DoU = [min_DoU]

    formulas = predict_formula(mz, mass_acc=mass_acc, charge=charge, lim_C=lim_C, lim_H=lim_H, lim_O=lim_O,
                               lim_DoU=lim_DoU, lim_N=lim_N, lim_P=lim_P, lim_Cl35=[n_Cl35], lim_Cl37=[n_Cl37])
    return formulas

def drop2H(f):
    e = f.copy()
    e.charge -= 2
    e[H1] -= 2
    return e


def flat_param(raw_str: str) -> list[int]:
    collects = set()
    for s in raw_str.replace(' ', '').split(','):
        if s == '':
            collects.add(0)
        elif s.isdigit():
            collects.add(int(s))
        else:
            lb, ub = s.split('-')
            collects.update(range(int(lb), int(ub) + 1))
    return list(collects)


# noinspection PyArgumentList
class CalcWorker(QObject):
    calculationFinished = Signal(bool, arguments=["isSuccess"])
    progressUpdate = Signal(str, int, arguments=["id", "value"])

    def __init__(self, parent=None):
        super().__init__(parent)
        self.cancel_flag = False

    def check_cancel(self):
        if self.cancel_flag:
            raise CancelError("Cancel")

    def startCalc(self):
        self.cancel_flag = False
        self.calc_data = {}
        # LOAD FILE
        ms1_neg, ms2_neg = load_mzml(CONFIG["path.neg_file"], progress=ProgressAdaptor(self, "data_load", 0, 50))
        self.check_cancel()
        ms1_pos, ms2_pos = load_mzml(CONFIG["path.pos_file"], progress=ProgressAdaptor(self, "data_load", 50, 100))
        self.check_cancel()

        # SCREEN MS2
        target_ions = CONFIG['target_ion.ions']
        MS2_FILTER_MASS_ACC = CONFIG['target_ion.mass_acc']
        dic = {}
        target_ions = ProgressAdaptor(self, "ms2_screen", 0, 100)(target_ions)
        for ion in target_ions:
            dic[ion.refname] = is_mass_in(ms2_pos[_C.SpecMZ], ion.mass, rtol=MS2_FILTER_MASS_ACC)
        search_results = pd.DataFrame(dic, index=ms2_pos.index)
        hit_sel = search_results.any(axis=1)
        arly_ions_names = [ion.refname for ion in target_ions if ion.type == 'Aryl']
        hit_results = search_results[hit_sel]
        self.calc_data["OPEFragment"] = hit_results.assign(**{_C.OPEClass: "Alkly"})
        self.calc_data["OPEFragment"].loc[hit_results[arly_ions_names].any(axis=1), _C.OPEClass] = "Aryl"
        self.calc_data["FragMS2"] = ms2_pos.loc[hit_sel]
        self.check_cancel()

        # DETECT ROI
        ROI_AGGREGATION_MASS_ACC = CONFIG['ROI.mass_acc']
        ms2_OPE_pos_roi_id, ms1_pos_roi_group = ms2_ms1_roi(self.calc_data["FragMS2"], ms1_pos,
                                                            ROI_AGGREGATION_MASS_ACC,
                                                            progress=ProgressAdaptor(self, "roi", 0, 100))
        peak_idx = ms2_OPE_pos_roi_id.groupby(_C.ROIGroupID)[_C.PrecursorMS1Int].idxmax()
        ms2_pos_OPE_peak = self.calc_data["FragMS2"].loc[peak_idx].copy()
        ms2_pos_OPE_peak[_C.ROIGroupID] = ms2_OPE_pos_roi_id.loc[ms2_pos_OPE_peak.index, _C.ROIGroupID]
        self.calc_data["FragMS2Peak"] = ms2_pos_OPE_peak
        del ms2_pos_OPE_peak
        self.check_cancel()

        # CALCULATE Cl NUMBER
        isotope_params = {Cl: flat_param(CONFIG["formula.isotope.Cl"])}
        self.calc_data["FragMS2Peak"]["Isotopes"] = predict_isotope(self.calc_data["FragMS2Peak"], ms1_pos,
                                                                    isotope_params, mass_acc=5e-6, top_n=5,
                                                                    progress=ProgressAdaptor(self, "cl", 0, 100))
        self.check_cancel()

        # FORMULA PREDICTION
        spec_info = self.calc_data["FragMS2Peak"]
        arly_info = self.calc_data["OPEFragment"]
        mass_acc = CONFIG["formula.mass_acc"]
        lim_C = flat_param(CONFIG["formula.element.C12"])
        lim_H = flat_param(CONFIG["formula.element.H1"])
        lim_O = flat_param(CONFIG["formula.element.O16"])
        lim_DoU = flat_param(CONFIG["formula.element.DoU"])
        lim_N = flat_param(CONFIG["formula.element.N14"])
        lim_P = flat_param(CONFIG["formula.element.P31"])
        tasks = [get_formula(spec_info.at[idx, _C.PrecursorMZ], spec_info.at[idx, _C.Isotopes],
                             arly_info.at[idx, _C.OPEClass] == "Aryl", charge=1, mass_acc=mass_acc, lim_C=lim_C,
                             lim_H=lim_H, lim_O=lim_O, lim_DoU=lim_DoU, lim_N=lim_N, lim_P=lim_P) for idx in
                 spec_info.index]
        formulas = ProgressParallel(n_jobs=-1)(tasks, progress=ProgressAdaptor(self, "formula", 0, 100))
        self.calc_data["FragMS2Peak"][_C.FormulaList] = formulas
        self.calc_data["FragMS2PeakWithFormula"] = self.calc_data["FragMS2Peak"].loc[
            self.calc_data["FragMS2Peak"]["Formulas"].apply(lambda x: len(x) != 0)]
        del formulas, spec_info, arly_info
        self.check_cancel()

        # CHECK tri-/di-/mono-esters
        tri_pos = []
        for ms2_idx, rt, precursor_mz, ms1int, formulas in self.calc_data["FragMS2PeakWithFormula"][
            [_C.RT, _C.PrecursorMZ, _C.PrecursorMS1Int, _C.FormulaList]].itertuples():
            for f in ProgressAdaptor(self, "tri-ester", 0, 100)(formulas):
                mass = drop2H(f).mass
                tic_int = search_from_another_ms1(mass, rt, ms1_neg, 5e-6, rt_atol=60)
                tri_pos.append((ms2_idx, f, (precursor_mz - f.mass) / f.mass, ms1int > tic_int))

        self.check_cancel()
        tri_pos_df = pd.DataFrame(tri_pos, columns=[_C.MS2IDX, _C.Formula, "Deviation", "Tri-ester"])
        self.output1_results = pd.merge(tri_pos_df, self.calc_data["FragMS2PeakWithFormula"].drop(
            columns=["Formulas", _C.ROIGroupID]), left_on=_C.MS2IDX, right_index=True).reset_index(drop=True).merge(
            self.calc_data["OPEFragment"], left_on=_C.MS2IDX, right_index=True)

        self.calculationFinished.emit(True)
        get_reusable_executor().shutdown(wait=True) # shutdown joblib loky executor
        self.moveToThread(QApplication.instance().thread())
        
        
