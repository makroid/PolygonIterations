from PyQt5.QtWidgets import QWidget, QApplication, QFormLayout, QSlider, QHBoxLayout
from PyQt5.QtGui import QPainter, QColor, QBrush, QPolygonF
from PyQt5.QtCore import QPointF
from PyQt5.QtCore import Qt
import sys
import math


INIT_NCORNERS = 4
INIT_NITERS = 20
INIT_REDUCE = 0.75


def createPoly(n, r, cx, cy, rot=0):
    polygon = QPolygonF()
    w = 360 / n  # angle per step
    for i in range(n):  # add the points of polygon
        t = w * i + rot + 45
        x = r * math.cos(math.radians(t))
        y = r * math.sin(math.radians(t))
        polygon.append(QPointF(cx + x, cy + y))

    return polygon


class ControlWidget(QWidget):
    def __init__(self, draw_widget):
        super().__init__()

        self.draw_widget = draw_widget
        self.layout = QFormLayout()

        self.slider_corners = QSlider(Qt.Horizontal)
        self.slider_corners.setRange(3, 12)
        self.slider_corners.setValue(INIT_NCORNERS)
        self.slider_corners.setTickInterval(1)
        self.slider_corners.valueChanged[int].connect(self.slider_val_changed)

        self.slider_iters = QSlider(Qt.Horizontal)
        self.slider_iters.setRange(1, 100)
        self.slider_iters.setValue(INIT_NITERS)
        self.slider_iters.setTickInterval(1)
        self.slider_iters.valueChanged[int].connect(self.slider_val_changed)

        self.slider_reduce = QSlider(Qt.Horizontal)
        self.slider_reduce.setRange(1, 99)
        self.slider_reduce.setValue(int(INIT_REDUCE*100))
        self.slider_reduce.setTickInterval(1)
        self.slider_reduce.valueChanged[int].connect(self.slider_val_changed)

        self.layout.addRow("Corners", self.slider_corners)
        self.layout.addRow("Iters", self.slider_iters)
        self.layout.addRow("Reduce", self.slider_reduce)

        self.setMaximumWidth(200)

        self.setLayout(self.layout)


    def slider_val_changed(self, value):
        self.draw_widget.n_iters = self.slider_iters.value()
        self.draw_widget.n_corners = self.slider_corners.value()
        self.draw_widget.f_reduce = self.slider_reduce.value() / 100
        self.draw_widget.repaint()



class DrawPolyWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.n_iters = INIT_NITERS
        self.n_corners = INIT_NCORNERS
        self.f_reduce = INIT_REDUCE

        self.initUI()


    def initUI(self):
        self.setMinimumSize(500, 500)


    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawPolygons(qp)
        qp.end()


    def drawPolygons(self, qp):
        #col = QColor(255, 255, 255)
        #col.setNamedColor('#d4d4d4')
        #qp.setPen(col)

        alpha = math.degrees(math.atan((1 - self.f_reduce) / self.f_reduce))

        f = self.f_reduce
        s = self.width()/2 + 0
        rot = 0

        for i in range(self.n_iters):
            poly = createPoly(n=self.n_corners, r=s, cx=self.width() / 2, cy=self.height() / 2, rot=rot)

            red = 10 + i * (255 // self.n_iters)
            blue = 55
            green = i * (255 // self.n_iters)

            qp.setBrush(QColor(red, green, blue))
            qp.drawPolygon(poly)

            s = math.sqrt(s*s*f*f + s*s*(1-f)*(1-f))
            rot = (i+1) * alpha



class MainWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.draw_widget = DrawPolyWidget()
        self.control_widget = ControlWidget(self.draw_widget)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.control_widget)
        self.layout.addWidget(self.draw_widget)

        self.setLayout(self.layout)

        self.setGeometry(300, 300, 800, 500)

        self.setWindowTitle('PolygonIterations')
        self.show()


def main():
    app = QApplication(sys.argv)
    ex = MainWidget()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()