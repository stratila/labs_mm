import sys
import pyqtgraph as pg
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QLineEdit,
    QGridLayout,
    QLabel,
    QDialog,
    QVBoxLayout
)
from PyQt5.QtGui import QDoubleValidator
from lab3 import dissipation_coefficient


INPUTS_NAMES = ['d2', 'd3', 'd4', 'd5', 'd8', 'd91', 'd90', 'l1',
                'l2', 'l3', 'l4', 'l5', 'l6', 'l7', 'l8', 'l9', 'l10']

DEFAULT_VALUES = [145, 136, 220, 165, 165, 165, 100, 10, 320, 254,
                  70, 280, 10, 10, 300, 300, 150]


# https://pythonspot.com/pyqt5-tabs/ #TODO make next lab with tabs


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self._plot_items = []
        self._inputs = []

        self.setWindowTitle("Lab 3")
        self.setGeometry(100, 100, 800, 500)
        self.init_components()
        self.qt_connections()
        self.show()

    def init_components(self):
        widget = QWidget()
        layout = QGridLayout()
        widget.setLayout(layout)

        for i, nv in enumerate(zip(INPUTS_NAMES, DEFAULT_VALUES)):
            name, value = nv
            text = QLineEdit(f'{value}')
            text.setValidator(QDoubleValidator())
            label = QLabel(f'{name}:')
            self._inputs.append(text)

            layout.addWidget(label, i, 0)
            layout.addWidget(text, i, 1)

        self.calculate_button = QPushButton('Build')
        layout.addWidget(self.calculate_button, 17, 0)
        self.plot = pg.plot()
        layout.addWidget(self.plot, 0, 3, 17, 1)
        self.setCentralWidget(widget)

    def qt_connections(self):
        self.calculate_button.clicked.connect(self.show_chart)

    def show_chart(self):
        self._remove_plot_items()
        '''
        plot_curve = pg.PlotCurveItem()
        to = int(self.text.text()) # if not empty
        plot_curve.setData(
            np.sin(np.linspace(0, to)) +
            np.random.normal(scale=0.1, size=len(np.linspace(0, to)))
        )
        self._plot_items.append(plot_curve)'''
        data = map(lambda n: n*10**-3, (float(inp.text()) for inp in self._inputs))
        k, x, y = dissipation_coefficient(*data)

        dk_dialog = QDialog()
        dk_dialog.setWindowTitle("Dissipation Coefficient")
        dk_dialog.layout = QVBoxLayout()
        dk_dialog.layout.addWidget(QLabel(f"k={k}"))
        dk_dialog.setLayout(dk_dialog.layout)

        plot_curve = pg.PlotCurveItem()
        plot_curve.setData(x, y)

        self.plot.addItem(plot_curve)
        self._plot_items.append(plot_curve)

        dk_dialog.exec()

    def _remove_plot_items(self):
        for item in self._plot_items:
            self.plot.removeItem(item)
        self._plot_items.clear()


app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec())
