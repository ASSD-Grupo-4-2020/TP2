from PyQt5 import QtWidgets, QtCore

from Frontend.MainWindow import Ui_MainWindow
from Frontend.MplWidget import MplWidget

import sys


#####  This code makes exceptions appear when sometimes pyqt wraps them in some random error  #####
sys._excepthook = sys.excepthook

def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

sys.excepthook = my_exception_hook

####################################################################################################


class MainWindow(QtWidgets.QMainWindow):
    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

        self.rows = 0
        #esta lista contiene los marcos que a su vez tienen a la timeline y el panel de control dentro
        self.tracks = []


        ###   Callbacks   ###


        self.ui.pushButton.clicked.connect(self.add_track)
        self.ui.pushButton_2.clicked.connect(self.remove_track)


        ###   Callbacks   ###


    #creates track object
    def create_track(self):
        pass


    #adds track to gui
    def add_track(self):

        #track = TrackUI()
        #track.setParent(self.ui.scrollAreaWidgetContents)
        self.ui.trackwindow_layout.addWidget(TrackUI())
        #self.rows += 1

        #frame = QtWidgets.QFrame(self.ui.scrollAreaWidgetContents)
        #frame.setMinimumSize(QtCore.QSize(0, 230))
        ##frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        #frame.setFrameShadow(QtWidgets.QFrame.Raised)
        #frame.setObjectName("frame" + str(self.rows + 1))

        #horizontallayout = QtWidgets.QHBoxLayout(frame)
        #horizontallayout.setObjectName("horizontalLayout" + str(self.rows + 1))

        #control_panel = QtWidgets.QWidget(frame)
        #control_panel.setMinimumSize(QtCore.QSize(150, 0))
        #control_panel.setObjectName("control_panel" + str(self.rows + 1))
        #horizontallayout.addWidget(control_panel)

        #tracktimeline = MplWidget(frame)
        #tracktimeline.setMinimumSize(QtCore.QSize(400, 0))
        #tracktimeline.setObjectName("tracktimeline" + str(self.rows + 1))
        #horizontallayout.addWidget(tracktimeline)

        #elf.ui.trackwindow_layout.addWidget(frame)
        #self.tracks.append(frame)
        lista = self.ui.scrollAreaWidgetContents.children()

        print(lista)






        #frame = QtWidgets.QFrame(self.ui.scrollAreaWidgetContents)
        #sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        #sizePolicy.setHorizontalStretch(0)
        #sizePolicy.setVerticalStretch(0)
        #sizePolicy.setHeightForWidth(frame.sizePolicy().hasHeightForWidth())
        #frame.setSizePolicy(sizePolicy)
        #frame.setMinimumSize(QtCore.QSize(0, 200))
        #frame.setObjectName("frame" + str(row + 1))
        #self.ui.trackwindow_layout.addWidget(frame, row + 1, 1, 1, 1)

        #tracktimeline = MplWidget(frame)
        #sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        #sizePolicy.setHorizontalStretch(0)
        #sizePolicy.setVerticalStretch(0)
        #sizePolicy.setHeightForWidth(tracktimeline.sizePolicy().hasHeightForWidth())
        #tracktimeline.setSizePolicy(sizePolicy)
        #tracktimeline.setMinimumSize(QtCore.QSize(400, 200))
        #tracktimeline.setObjectName("tracktimeline" + str(row + 1))
        #self.ui.trackwindow_layout.addWidget(tracktimeline, row + 1, 1, 1, 1)


        #trackframe = QtWidgets.QFrame(self.ui.scrollAreaWidgetContents)
        #sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        #sizePolicy.setHorizontalStretch(0)
        #sizePolicy.setVerticalStretch(0)
        #sizePolicy.setHeightForWidth(trackframe.sizePolicy().hasHeightForWidth())
        #trackframe.setSizePolicy(sizePolicy)
        #trackframe.setMinimumSize(QtCore.QSize(150, 100))
        #trackframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        #trackframe.setFrameShadow(QtWidgets.QFrame.Raised)
        #t3rackframe.setObjectName("trackframe" + str(row + 1))
        #self.ui.trackwindow_layout.addWidget(trackframe, row + 1, 0, 1, 1)



    #removes track from gui
    def remove_track(self):
        for widget in self.ui.scrollAreaWidgetContents.children():
            if type(widget) == TrackUI:
                print(type(widget))
                self.ui.trackwindow_layout.removeWidget(widget)
                widget.deleteLater()
                widget.wiget_name = None

    #plays desired track
    def play_track(self):
        pass

    #plays all the tracks at the same time
    def play_song(self):
        pass

    #plots track timelines
    def plot_timelines(self):
        pass

    #Pots spectrogram
    def plot_spectrogram(self):
        pass


class TrackUI(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(TrackUI, self).__init__(parent)

        self.setMinimumSize(QtCore.QSize(0, 230))

        self.control_panel = QtWidgets.QWidget()
        self.control_panel.setMinimumSize(QtCore.QSize(150, 0))

        self.tracktimeline = MplWidget()
        self.tracktimeline.setMinimumSize(QtCore.QSize(400, 0))

        layout = QtWidgets.QHBoxLayout()

        layout.addWidget(self.control_panel)
        layout.addWidget(self.tracktimeline)

        self.setLayout(layout)







# Controlador de ventanas, conecta señales que le dicen a las distintas ventanas cuando abrirse y cerrarse
class Controller:

    def __init__(self):
        pass

    def show_main(self):
        self.window = MainWindow()
        self.window.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_main()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()