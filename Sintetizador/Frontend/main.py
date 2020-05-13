from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QFrame

from Frontend.MainWindow import Ui_MainWindow
from Frontend.MplWidget import MplWidget

from Player.Working_Classes import Player

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

        #Este es el reporductor, aca tengo todos los tracks, el archivo midi y lo necesario para sintetizar
        self.player = Player(11025)


        ###   Callbacks   ###

        self.ui.Reproducir_track1.clicked.connect(lambda: self.play_track(1))
        self.ui.Reproducir_track2.clicked.connect(lambda: self.play_track(2))
        self.ui.Reproducir_track3.clicked.connect(lambda: self.play_track(3))
        self.ui.Reproducir_track4.clicked.connect(lambda: self.play_track(4))
        self.ui.Reproducir_track5.clicked.connect(lambda: self.play_track(5))
        self.ui.Reproducir_track6.clicked.connect(lambda: self.play_track(6))
        self.ui.Reproducir_track7.clicked.connect(lambda: self.play_track(7))
        self.ui.Reproducir_track8.clicked.connect(lambda: self.play_track(8))
        self.ui.Reproducir_track9.clicked.connect(lambda: self.play_track(9))
        self.ui.Reproducir_track10.clicked.connect(lambda: self.play_track(10))
        self.ui.Reproducir_track11.clicked.connect(lambda: self.play_track(11))
        self.ui.Reproducir_track12.clicked.connect(lambda: self.play_track(12))
        self.ui.Reproducir_track13.clicked.connect(lambda: self.play_track(13))
        self.ui.Reproducir_track14.clicked.connect(lambda: self.play_track(14))
        self.ui.Reproducir_track15.clicked.connect(lambda: self.play_track(15))
        self.ui.Reproducir_track16.clicked.connect(lambda: self.play_track(16))



        self.ui.cargar_archivo.clicked.connect(self.load_mid)
        self.ui.synthesis_selector.currentIndexChanged.connect(self.change_synth)
        self.ui.add_track.clicked.connect(self.add_track)
        #self.ui.pushButton.clicked.connect(self.add_track)
        #self.ui.pushButton_2.clicked.connect(self.remove_track)


        ###   Callbacks   ###

    # Carga el archivo midi a player
    def load_mid(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Midi Files (*.mid)", options=options)
        if fileName:
            self.player.load_file(fileName)
            self.player.create_tracks()
            print(self.player.tracks)
            # en este punto tengo EN PLAYER todos los tracks del midi que abri con el boton, y cada track con su
            # respectiva nota, etc...

            self.ui.track_number.setText('Hay %s tracks en su archivo MIDI' % len(self.player.tracks))

            self.ui.track_selector.clear()
            for track in self.player.tracks:
                self.ui.track_selector.addItem('Track %s' % track.iden)

    def change_synth(self):
        current_text = self.ui.synthesis_selector.currentText()
        if current_text == 'Sintesis aditiva':
            self.ui.instrument_selector.clear()
            self.ui.instrument_selector.addItems(['flute', 'piano', 'violin', 'trumpet'])
        elif current_text == 'Sintesis fisica':
            self.ui.instrument_selector.clear()
            self.ui.instrument_selector.addItems(['guitar', 'drums'])
        elif current_text == 'Sintesis basada en muestras':
            pass

    def add_track(self):
        reproductor  = 0
        for ui in self.ui.scrollAreaWidgetContents.children():
            reproductor += 1
            if isinstance(ui, QFrame) and not ui.isEnabled():
                # Agrego track al primer reproductor desactivado que encuentro
                ui.setEnabled(True)

                lista = self.ui.track_selector.currentText().split()
                ind = int(lista[1])

                self.ui.track_selector.removeItem(self.ui.track_selector.currentIndex())

                current_instrument = self.ui.instrument_selector.currentText()
                current_form = self.ui.synthesis_selector.currentText()

                # todo agregar sintesis basada en muestras
                if current_form == 'Sintesis aditiva':
                    current_form = 'additive'
                elif current_form == 'Sintesis fisica':
                    current_form = 'physical'
                elif current_form == 'Sintesis basada en muestras':
                    pass

                self.player.tracks[ind - 1].set_reproductor(reproductor)

                self.player.synthesize_track(ind, current_form, current_instrument)
                print('sintetizo')

                self.player.play_track(ind)

                break


    # plays desired track
    def play_track(self, iden):
        self.player.play_track(iden)

    # plays all the tracks at the same time
    def play_song(self):
        pass

    # plots track timelines
    def plot_timelines(self):
        pass

    # Pots spectrogram
    def plot_spectrogram(self):
        pass



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