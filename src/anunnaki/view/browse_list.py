import logging
from typing import Union

from PySide6.QtCore import Qt, QModelIndex, QSize, Signal, QTimer
from PySide6.QtGui import QPainter, QBrush, QColor, QPainterPath, QPen
from PySide6.QtWidgets import QListWidget, QListView, QStyleOptionViewItem, QStyledItemDelegate
from anunnaki_source.models import Media, Kind


class BrowseDelegate(QStyledItemDelegate):
    def __init__(self):
        super().__init__()

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        data: Media = index.data(Qt.ItemDataRole.UserRole)
        poster = index.data(Qt.ItemDataRole.DecorationRole)

        b_width = option.rect.width()
        b_height = option.rect.height()

        title = data.title
        kind = data.kind
        year = data.year

        title_rect = option.rect.adjusted(10, b_height-(b_height/6), 0, 0)
        poster_rect = option.rect.adjusted(10, 10, 0, -b_height/6)
        kind_rect = option.rect.adjusted(20, 15, -b_width+40, -b_height+35)
        year_rect = option.rect.adjusted(b_width-50, 15, -10, -b_height+35)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if poster:
            path = QPainterPath()
            path.addRoundedRect(poster_rect, 5, 5)
            painter.setClipPath(path)
            pen = QPen(QColor("0xffffff"), 5)
            painter.setPen(pen)
            painter.drawPixmap(poster_rect, poster)
            painter.setClipping(False)
        else:
            painter.fillRect(poster_rect, QBrush(QColor("#2c2c2c"), Qt.BrushStyle.SolidPattern))

        if year:
            path = QPainterPath()
            path.addRoundedRect(year_rect, 5, 2)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.fillPath(path, QColor("#1e17ff"))
            painter.drawPath(path)
            painter.setPen(QColor("#ffeff6"))
            painter.drawText(year_rect, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter, str(year))

        if kind:
            k = str(kind.name[0])
            path = QPainterPath()
            path.addRoundedRect(kind_rect, 5, 2)
            painter.setPen(Qt.PenStyle.NoPen)
            if kind == Kind.MOVIES:
                painter.fillPath(path, QColor("#ff1352"))
            else:
                painter.fillPath(path, QColor("#fff70f"))
            painter.drawPath(path)
            if kind == Kind.MOVIES:
                painter.setPen(QColor("#ffffff"))
            else:
                painter.setPen(QColor("#000000"))

            painter.drawText(kind_rect, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter, k)

        painter.setPen(QColor("#ffffff"))
        painter.drawText(title_rect, Qt.AlignmentFlag.AlignHCenter | Qt.TextFlag.TextWordWrap, title)

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        # size = super().sizeHint(option, index)
        # logging.debug(f"size {size}")
        return QSize(180, 300)


class BrowseList(QListWidget):
    list_end_reached = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        timer = QTimer(self)
        timer.setInterval(2000)
        timer.timeout.connect(self.on_time)

        self.setMovement(QListView.Movement.Static)
        self.setFlow(QListView.Flow.LeftToRight)
        self.setWrapping(True)
        # self.setViewMode(QListView.ViewMode.ListMode)
        self.setResizeMode(QListView.ResizeMode.Adjust)
        self.setItemDelegate(BrowseDelegate())
        self.setDragDropMode(QListView.DragDropMode.NoDragDrop)
        self.setDefaultDropAction(Qt.DropAction.IgnoreAction)

        self.scroll = self.verticalScrollBar()
        self.scroll.valueChanged.connect(lambda value: [self.list_end_reached.emit() if value == self.scroll.maximum() else None])

        timer.start()

    def on_time(self):
        # logging.debug("timer update")
        if self.scroll.value()+2 >= self.scroll.maximum():
            self.list_end_reached.emit()
