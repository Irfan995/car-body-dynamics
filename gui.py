from car_model_form_widget import *
from PyQt5 import uic
import sys
from PyQt5 import QtWidgets as qtw
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from quarter_car_model import *


class MainWindow(qtw.QWidget, Ui_Form):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        
        
        # Create the maptlotlib FigureCanvas object, 
        # which defines a single set of axes as self.axes.
        self.figure = Figure(figsize=(6,8),tight_layout=True, frameon=True)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.figure.tight_layout()
        self.modelOutput.layout().addWidget(self.canvas)

        # Set predefined values to input
        self.car_body_mass.setText('450')
        self.car_speed.setText('120')
        self.suspension_spring.setText('15000')
        self.suspension_shock_absorber.setText('4500')
        self.wheel_mass.setText('20')
        self.tire_spring_constant.setText('90000')
        self.ramp_angle.setText('45')
        self.t.setText('3')

        # activate signal slot
        self.calculate.clicked.connect(self.show_graph)
        
        self.show()

    def show_graph(self):
        m1 = self.car_body_mass.text()
        v = self.car_speed.text()
        k1 = self.suspension_spring.text() 
        c1 = self.suspension_shock_absorber.text()
        m2 = self.wheel_mass.text()
        k2 = self.tire_spring_constant.text()
        ramp_angle = self.ramp_angle.text()
        t = self.t.text()
        ymag = 6

        car_model = CarModel(int(m1), int(m2), int(c1), int(k1), int(k2), 
                            int(ymag), int(v), int(ramp_angle), int(t))
        self.ax.clear()
        car_model.plot(self.ax)
        self.canvas.draw()


if __name__== '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    mw.setWindowTitle('Car Model')
    sys.exit(app.exec())