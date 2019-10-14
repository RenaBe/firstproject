from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit,\
        QInputDialog, QApplication,QFileDialog, QLabel,QVBoxLayout
from PyQt5.QtCore import QCoreApplication

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import Class_LY12
import Class_las
import sys


class InputDialogWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.figure = plt.figure()          #画布
        self.canvas = FigureCanvas(self.figure)

        btn = QPushButton('打开文件', self)  #建立打开文件按钮
        btn.clicked.connect(self.getText)

        qbtn = QPushButton('退出', self)     #建立退出按钮
        qbtn.clicked.connect(QCoreApplication.instance().quit)

        lab1 = QLabel('Class_LY12',self)     #标签
        lab2 = QLabel('Class_las',self)

        self.qle1 = QLineEdit(self)          #显示文本
        self.qle2 = QLineEdit(self)

        layout = QVBoxLayout(self)           #页面布局
        layout.addWidget(btn)  #
        layout.addWidget(qbtn)

        layout.addWidget(lab1)
        layout.addWidget(self.qle1)
        layout.addWidget(lab2)
        layout.addWidget(self.qle2)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.setWindowTitle('UI界面')
        self.setGeometry(300, 300, 800, 600)
        self.show()

    
    def getText(self):
        fname = QFileDialog.getOpenFileNames(self,'Open file', '/home')
        if fname[0]:
            lst_1 = []
            lst_2 = []
            ax = self.figure.gca()
            ax.clear()
            for i in fname[0]:
                filename = i.split("/")[-1]   #las_8_31_2_20190926_大夹具.txt
                if filename[:2] =='LY':
                    a = Class_LY12.LY12(filename)
                    if a:
                        data_LY = {
                                'filename':filename,
                                '模量(0307)': a.test_modu_0307,
                                '模量(最大斜率)' :a.test_modu_maxSlope
                                }
                        lst_1.append(data_LY)
                        ax.plot(a._dis, a._load, label=filename)
                        ax.legend()


                elif filename[:2] =='la':
                    b = Class_las.las(filename)
                    if b:
                        data_la ={
                                'filename':filename,
                                'ult_load':b.ult_load,
                                "test_modu_0307":b.test_modu_0307,
                                'test_yieldL':b.test_yieldL,
                                'test_yieldS':b.test_yieldS,
                                "test_modu_maxSlope":b.test_modu_maxSlope,
                                'test_yieldL':b.test_yieldL,
                                'test_yieldS':b.test_yieldS
                                }
                        lst_2.append(data_la)
                        ax.plot(b._dis, b._load, label=filename)
                        ax.legend()

            self.qle1.setText(str(lst_1))
            self.qle2.setText(str(lst_2))
            self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = InputDialogWindow()
    sys.exit(app.exec_())