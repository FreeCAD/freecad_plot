from PySide2 import QtCore, QtGui, QtWidgets

import FreeCADGui

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backend_bases import FigureManagerBase
from matplotlib.backends.backend_qt5agg import FigureCanvas as FigCan
from matplotlib.backends.backend_qt5agg import FigureManager as FigMan
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT, ToolbarQt
from matplotlib import backend_tools, cbook

class FigureManager(FigureManagerBase):
    all_widgets = []
    def __init__(self, canvas, num):
        super().__init__(canvas, num)
        self.mw = FreeCADGui.getMainWindow()
        self.mdi = self.mw.findChild(QtWidgets.QMdiArea)
        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(QtWidgets.QHBoxLayout())
        self.mdi.addSubWindow(self.widget)
        self.widget.layout().addWidget(self.canvas)
        self.widget.show()

        FigureManager.all_widgets.append(self.widget)

        self.toolbar = self._get_toolbar(self.canvas, self.widget)
        self.widget.layout().setMenuBar(self.toolbar)
        self.canvas.set_widget_name = self.set_widget_name

    def show(self):
        self.canvas.draw_idle()

    def _get_toolbar(self, canvas, parent):
        # must be inited after the window, drawingArea and figure
        # attrs are set
        if matplotlib.rcParams['toolbar'] == 'toolbar2':
            toolbar = NavigationToolbar2QT(canvas, parent, True)
        elif matplotlib.rcParams['toolbar'] == 'toolmanager':
            toolbar = ToolbarQt(self.toolmanager, self.window)
        else:
            toolbar = None
        return toolbar

    def set_widget_name(self):
        if not self.widget.windowTitle() and plt.gca().get_title():
            self.widget.setWindowTitle(plt.gca().get_title())

class FigureCanvas(FigCan):
    def draw_idle(self):
        super().draw_idle()
        if hasattr(self, "set_widget_name"):
            self.set_widget_name()
