from typing import cast, Optional

from PySide6.QtCore import QModelIndex, QSize, QRect
from PySide6.QtGui import QPainter, QTextDocument, QAbstractTextDocumentLayout, QPalette
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem, QStyle
from rdkit.Chem.Draw import rdMolDraw2D

from OPEs_ID.expr import ChemFormula
from .model import MyRole, ExtraProperty

# TODO: Move to a global configuration
DEFAULT_RENDER_PIXEL_SIZE = (100, 100)


# noinspection PyArgumentList
def make_svg(mol, size: Optional[tuple[int, int]] = None):
    mol = rdMolDraw2D.PrepareMolForDrawing(mol)
    if size is None:
        drawer = rdMolDraw2D.MolDraw2DSVG(*DEFAULT_RENDER_PIXEL_SIZE)
    else:
        drawer = rdMolDraw2D.MolDraw2DSVG(*size)
    drawer.DrawMolecule(mol)
    drawer.FinishDrawing()
    return drawer.GetDrawingText()


class ChemicalDelegate(QStyledItemDelegate):

    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(
            self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex
    ) -> None:
        extra_prop = ExtraProperty(index.data(MyRole.ExtraPropertyRole))
        if extra_prop == ExtraProperty.Normal:
            super().paint(painter, option, index)
        elif extra_prop == ExtraProperty.ChemicalFormula:
            formula = cast(ChemFormula, index.data(MyRole.ChemicalFormulaRole))
            options = QStyleOptionViewItem(option)
            self.initStyleOption(options, index)
            painter.save()
            doc = QTextDocument()
            doc.setHtml(formula.html())
            options.text = ""
            options.widget.style().drawControl(QStyle.CE_ItemViewItem, option, painter)
            painter.translate(option.rect.topLeft())
            clip = QRect(0, 0, options.rect.width(), options.rect.height())
            ctx = QAbstractTextDocumentLayout.PaintContext()
            if option.state & QStyle.State_Selected:
                ctx.palette.setColor(QPalette.Text, option.palette.color(QPalette.Active, QPalette.HighlightedText))
            ctx.clip = clip
            painter.translate(0, 0.5 * (options.rect.height() - doc.size().height()))
            doc.documentLayout().draw(painter, ctx)
            # doc.drawContents(painter, clip)
            painter.restore()
        elif extra_prop == ExtraProperty.MolSVG:
            bounds = option.rect
            bounds.moveTo(
                option.rect.center().x() - bounds.width() / 2,
                option.rect.center().y() - bounds.height() / 2,
            )
            mol = index.data(MyRole.RDkitMolRole)
            svg_data = make_svg(mol, size=(bounds.width(), bounds.height()))
            svg_renderer = QSvgRenderer(svg_data.encode(), self)
            svg_renderer.render(painter, bounds)
        elif extra_prop == ExtraProperty.MetfragResult:
            option.text = index.data(MyRole.MetfragResultRole)
            super().paint(painter, option, index)

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        extra_prop = index.data(MyRole.ExtraPropertyRole)
        if extra_prop == ExtraProperty.Normal:
            return super().sizeHint(option, index)
        elif extra_prop == ExtraProperty.ChemicalFormula:
            formula = cast(ChemFormula, index.data(MyRole.ChemicalFormulaRole))
            text_document = QTextDocument()
            text_document.setHtml(formula.html())
            size = text_document.size().toSize()
            return size + QSize(4, 4)
        elif extra_prop == ExtraProperty.MolSVG:
            # svg_data = index.data(Qt.DisplayRole).encode()
            # svg_renderer = QSvgRenderer(svg_data)
            # return svg_renderer.defaultSize()
            return QSize(*DEFAULT_RENDER_PIXEL_SIZE)
        else:
            return super().sizeHint(option, index)
