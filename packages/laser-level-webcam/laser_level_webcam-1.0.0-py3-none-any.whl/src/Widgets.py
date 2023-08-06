from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtCore import Qt
from PySide6.QtCore import Signal
from PySide6.QtGui import QColor
from PySide6.QtGui import QFont
from PySide6.QtGui import QPainter
from PySide6.QtGui import QPaintEvent
from PySide6.QtGui import QPen
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget
from scipy.interpolate import CubicSpline

from .DataClasses import FrameData
from .DataClasses import Sample
from .utils import get_units
from .utils import units_of_measurements


style = {
    "axes.grid": "True",
    "axes.edgecolor": "white",
    "axes.linewidth": "0",
    "xtick.major.size": "0",
    "ytick.major.size": "0",
    "xtick.minor.size": "0",
    "ytick.minor.size": "0",
    "text.color": "0.9",
    "axes.labelcolor": "0.9",
    "xtick.color": "0.9",
    "ytick.color": "0.9",
    "grid.color": "2A3459",
    "font.sans-serif": "Overpass, Helvetica, Helvetica Neue, Arial, Liberation \
        Sans, DejaVu Sans, Bitstream Vera Sans, sans-serif",
    "figure.facecolor": "202124",
    "axes.facecolor": "101012",
    "savefig.facecolor": "212946",
    "image.cmap": "RdPu",
}
plt.style.use(style)


class Graph(QWidget):  # type: ignore
    def __init__(self, samples: list[Sample]):
        super().__init__()

        self.samples = samples
        self.units = ""
        self.mode = ""
        self.selected_index = 0

        # Layouts
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Line chart
        fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(fig)

        self.ax.set_ylabel(self.units)
        self.ax.autoscale_view("tight")

        main_layout.addWidget(self.canvas)

    def set_selected_index(self, index: int) -> None:
        self.selected_index = index + 1
        self.update_graph()

    def set_units(self, units: str) -> None:
        self.units = units
        self.update_graph()

    def set_mode(self, mode: str) -> None:
        self.mode = mode
        self.update_graph()

    def update_graph(self) -> None:
        # Clear the axis and plot the data
        self.ax.clear()

        if self.units is None or self.mode is None or len(self.samples) == 0:
            self.canvas.draw()
            return

        unit_multiplier = units_of_measurements[self.units]

        x = np.arange(1, len(self.samples) + 1)
        y = []

        min_sample = 0.0
        max_sample = 0.0
        if self.mode == "Raw":
            # Raw points
            for s in self.samples:
                y.append(s.y * unit_multiplier)
            min_sample = min(y)
            max_sample = max(y)
            self.ax.plot(x, y, marker="o", markersize=5, label="Samples")

            # Fit a smooth curve to the data points
            if len(x) > 2:
                f = CubicSpline(x, y, bc_type="clamped")
                smooth_x = np.linspace(x[0], x[-1], 500)
                smooth_y = f(smooth_x)
                self.ax.plot(smooth_x, smooth_y, linewidth=2, label="Smooth")

            # Plot line
            line = np.polyfit(x, y, 1)
            line = np.polyval(line, x)
            self.ax.set_ylabel(self.units)
            self.ax.plot(x, line, label="Slope")

        else:
            # Raw points
            for s in self.samples:
                y.append(s.linYError * unit_multiplier)
            self.ax.plot(x, y, marker="o", markersize=5, label="Samples")

            min_sample = min(y)
            max_sample = max(y)

            # Fit a smooth curve to the data points
            if len(x) > 2:
                f = CubicSpline(x, y, bc_type="clamped")
                smooth_x = np.linspace(x[0], x[-1], 500)
                smooth_y = f(smooth_x)
                self.ax.plot(smooth_x, smooth_y, linewidth=2, label="Smooth")

            # Plot line
            self.ax.set_ylabel(self.units)
            zeros = np.zeros(len(self.samples))
            self.ax.plot(x, zeros, label="Slope")

        # Plot selected index
        if type(self.selected_index) is int and self.selected_index >= 0:
            x = np.array([self.selected_index, self.selected_index])
            y = np.array([min_sample, max_sample])

            self.ax.plot(x, y, linewidth=7, color="#380000", zorder=-1)
            self.ax.set_alpha(0.2)

        # Increase the number of ticks on the y-axis
        num_ticks = 10
        ticks = np.linspace(min(y), max(y), num_ticks)
        self.ax.set_yticks(ticks)

        self.ax.legend()
        self.canvas.draw()


class PixmapWidget(QWidget):  # type: ignore
    OnHeightChanged = Signal(int)

    def __init__(self) -> None:
        super().__init__()

        self.pixmap = QPixmap(100, 100)
        self.pixmap.fill(QColor(0, 0, 0))

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)

        if not self.pixmap:
            return

        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        new_height = event.size().height()
        self.OnHeightChanged.emit(new_height)

    def setPixmap(self, pixmap: QPixmap) -> None:
        self.pixmap = pixmap
        self.update()


class AnalyserWidget(QWidget):  # type: ignore
    def __init__(self) -> None:
        super().__init__()
        self.pixmap = QPixmap(100, 100)
        self.pixmap.fill(QColor(0, 0, 0))
        self.sample = 0  # location of the sample in pixel space on the widget
        self.zero = 0  # location of zero. if not set, it's None
        self.text = ""  # Text to display if zero is set. shows the distance from zero

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)
        painter = QPainter(self)

        # Pixmap
        painter.drawPixmap(self.rect(), self.pixmap)

        # Sample
        if self.sample:
            pen = QPen(Qt.green, 0, Qt.SolidLine)
            painter.setPen(pen)
            painter.drawLine(0, self.sample, self.width(), self.sample)

        # zero
        if self.zero:
            painter.setPen(Qt.red)
            painter.drawLine(0, self.zero, self.width(), self.zero)

        if self.text:
            painter.setFont(QFont("Arial", 12))
            painter.setPen(Qt.green)
            textWidth = painter.fontMetrics().horizontalAdvance(self.text)
            textHeight = painter.fontMetrics().height()
            x = (self.width() - textWidth) / 2
            y = self.sample - (textHeight / 2)
            painter.setPen(Qt.green)
            painter.drawText(int(x), int(y), self.text)

    def set_data(self, data: FrameData) -> None:
        self.pixmap = data.pixmap
        self.sample = data.sample
        self.zero = data.zero
        self.text = data.text
        self.update()


class TableUnit(QTableWidgetItem):  # type: ignore
    def __init__(self) -> None:
        super().__init__()
        self.units = ""
        self.value = 0.0

    def set_units(self, units: str) -> None:
        self.units = units

    def data(self, role: int) -> Any:
        super().data(role)
        if role == Qt.DisplayRole:
            return get_units(self.units, self.value)
        return None
