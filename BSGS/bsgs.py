import math
import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication


def bsgs(g, betha, n):
    g,betha,n=int(g), int(betha),int(n)

    m = math.floor(math.sqrt(n)) + 1
    # print(m)
    # Giant
    a = []
    for i in range(1, m + 1): #O(m)
        a.append(g ** (m * i) % n)
    # print(a)
    # Baby
    b = []
    for j in range(1, m): #O(m)
        temp = betha * g ** j % n
        b.append(temp)
        # print(temp)
        if temp in a:
            return a, b, temp, m * (a.index(temp) + 1) - j

"""
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUiType("guibsgs.ui", self)
        self.pushButton.clicked.connect(self.Solver)

    def Solver(self):
        g = self.genEdit.text()
        betha = self.bethaEdit.text()
        n = self.modEdit.text()

        a, b, power = bsgs(g, betha, n)
        self.babyEdit.setText(str(a))
        self.giantEdit.setText(str(b))
        self.powerEdit.setText(str(power))


def run():
    app = QApplication(sys.argv)
    GUI=MainWindow()
    GUI.show()
    sys.exit(app.exec_())
"""

if __name__ == "__main__":
    print("Введите числа: a, b, mod n:")
    a,b,mod=input(), input(), input()
    print("Малые шаги %s\nБольшие шаги %s\nСовпадающее число %s\nСтепень %s" % (bsgs(a,b,mod)[0],bsgs(a,b,mod)[1],bsgs(a,b,mod)[2],bsgs(a,b,mod)[3]))
    os.system("pause")