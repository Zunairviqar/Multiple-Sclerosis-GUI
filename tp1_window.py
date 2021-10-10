import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, \
    QFileDialog, QTextEdit, QLabel, QPlainTextEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt
from fsl.wrappers import bet
import os
import fsl
import time
from fsl.wrappers.fslmaths import fslmaths
import subprocess as sp


class TP1(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'MS Tool'
        self.left = 0
        self.top = 0
        self.width = 600
        self.height = 200
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.table_widget = TP1_Window(self)
        self.setCentralWidget(self.table_widget)
        self.show()


class TP1_Window(QWidget):
    def __init__(self, parent):
        self.create_directories()
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        # self.tabs.TabPosition()
        style = """
        QTabBar::tab {
            margin-right:10px;
            background-color: rgb(255, 255, 255);
            padding-left:5px;
            padding-right:5px;
            padding-top:3px;
            padding-bottom:3px;
            border-radius:5px;
        }
        QTabWidget::tab-bar{
            alignment: left;
        }
        QTabBar::tab:selected {
            color: #ffffff;
            background-color: rgb(0,0,255);
        }

        """
        self.setStyleSheet(style)

        # Add tabs
        self.tab1_1 = QWidget()
        self.tab1_2 = QWidget()

        # Create Timepoint 1 inner tab
        self.tabs.addTab(self.tab1_1, "Rapid Results")
        self.tabs.addTab(self.tab1_2, "Troubleshoot")

        # Rapid Results Tab Timepoint 1
        self.tab1_1.layout = QVBoxLayout(self)
        file_btn_3 = QPushButton("Choose File for Flair Timepoint 1")
        self.myTextBox_3 = QTextEdit()
        self.myTextBox_3.setFixedHeight(40)
        verify_3 = QLabel("Please verify the file path")
        verify_3.setAlignment(Qt.AlignRight)

        file_btn_4 = QPushButton("Choose File for T1 Timepoint 1")
        self.myTextBox_4 = QTextEdit()
        self.myTextBox_4.setFixedHeight(40)
        verify_4 = QLabel("Please verify the file path")
        verify_4.setAlignment(Qt.AlignRight)

        bianca_obtain = QPushButton("Obtain the Bianca Output")

        self.editorOutput = QPlainTextEdit()
        self.editorOutput.setStyleSheet("color: #ffffff; background-color: rgb(0,0,0);")

        open_fsl = QPushButton("Open the output in FSLEyes")

        self.tab1_1.layout.addWidget(file_btn_3)
        self.tab1_1.layout.addWidget(self.myTextBox_3)
        self.tab1_1.layout.addWidget(verify_3)

        self.tab1_1.layout.addWidget(file_btn_4)
        self.tab1_1.layout.addWidget(self.myTextBox_4)
        self.tab1_1.layout.addWidget(verify_4)

        self.tab1_1.layout.addWidget(bianca_obtain)
        self.tab1_1.layout.addWidget(self.editorOutput, 7)
        self.tab1_1.layout.addWidget(open_fsl)

        file_btn_3.clicked.connect(self.open_1_1)
        file_btn_4.clicked.connect(self.open_2_1)
        bianca_obtain.clicked.connect(self.run_all_bianca)
        open_fsl.clicked.connect(self.open_fsleyes)

        self.tab1_1.setLayout(self.tab1_1.layout)

        # Troubleshoot Results Tab Timepoint 1
        self.tab1_2.layout = QVBoxLayout(self)
        file_btn = QPushButton("Choose File for Flair Timepoint 1")
        self.myTextBox = QTextEdit()
        self.myTextBox.setFixedHeight(40)
        verify_1 = QLabel("Please verify the file path")
        verify_1.setAlignment(Qt.AlignRight)

        file_btn_2 = QPushButton("Choose File for T1 Timepoint 1")
        self.myTextBox_2 = QTextEdit()
        self.myTextBox_2.setFixedHeight(40)
        verify_2 = QLabel("Please verify the file path")
        verify_2.setAlignment(Qt.AlignRight)

        bet_btn = QPushButton("Run Brain Extraction")
        resample = QPushButton("Resample the FLAIR Image to Testing Data")
        register_flair = QPushButton("Register the Resampled Brain to MNI Space")
        register_T1 = QPushButton("Register the T1 Image onto the Resampled Flair Image")
        Create_MF = QPushButton("Create a Master file with the Generated Data for BIANCA")
        BIANCA = QPushButton("Run the BIANCA Algorithm")
        Binary_mask = QPushButton("Create a Binary Mask from the BIANCA Output")
        Ero_Dil = QPushButton("Refine the Binary Mask")
        open_fsl2 = QPushButton("Open the output in FSLEyes")

        self.editorOutput2 = QPlainTextEdit()

        self.editorOutput2.setStyleSheet("color: #ffffff; background-color: rgb(0,0,0);")

        self.tab1_2.layout.addWidget(file_btn)
        self.tab1_2.layout.addWidget(self.myTextBox)
        self.tab1_2.layout.addWidget(verify_1)

        self.tab1_2.layout.addWidget(file_btn_2)
        self.tab1_2.layout.addWidget(self.myTextBox_2)
        self.tab1_2.layout.addWidget(verify_2)

        self.tab1_2.layout.addWidget(bet_btn)
        self.tab1_2.layout.addWidget(resample)
        self.tab1_2.layout.addWidget(register_flair)
        self.tab1_2.layout.addWidget(register_T1)
        self.tab1_2.layout.addWidget(Create_MF)
        self.tab1_2.layout.addWidget(BIANCA)
        self.tab1_2.layout.addWidget(Binary_mask)
        self.tab1_2.layout.addWidget(Ero_Dil)
        self.tab1_2.layout.addWidget(self.editorOutput2, 7)
        self.tab1_2.layout.addWidget(open_fsl2)



        self.tab1_2.setLayout(self.tab1_2.layout)

        file_btn.clicked.connect(self.open_1)  # connect clicked to self.open()
        file_btn_2.clicked.connect(self.open_2)  # connect clicked to self.open()
        bet_btn.clicked.connect(lambda: self.bet(self.editorOutput2))
        resample.clicked.connect(lambda: self.resample_flair(self.editorOutput2))
        register_flair.clicked.connect(lambda: self.register_to_MNI(self.editorOutput2))
        register_T1.clicked.connect(lambda: self.register_t1_to_flair(self.editorOutput2))
        Create_MF.clicked.connect(lambda: self.generate_masterfile(self.editorOutput2))
        BIANCA.clicked.connect(lambda: self.run_bianca(self.editorOutput2))
        Binary_mask.clicked.connect(self.bianca_binary)
        Ero_Dil.clicked.connect(lambda: self.bianca_open(self.editorOutput2))
        open_fsl2.clicked.connect(self.open_fsleyes)


        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

    # Create Directories for Storing TP1 and TP2 Data
    def create_directories(self):
        # Directory Names
        directory_1 = "TP1"
        directory_2 = "TP2"
        directory_3 = "Results"
        # Parent Directory path
        x = os.getcwdb()
        print(x)
        y = str(x).replace("b'", '')
        z = y.replace("'", '')
        parent_dir = z

        # Path
        path = os.path.join(parent_dir, directory_1)
        try:
            os.mkdir(path)
        except OSError as error:
            print(error)

        path = os.path.join(parent_dir, directory_2)
        try:
            os.mkdir(path)
        except OSError as error:
            print(error)

        path = os.path.join(parent_dir, directory_3)
        try:
            os.mkdir(path)
        except OSError as error:
            print(error)

        self.TP_1_Flair_Brain = 'TP1/FLAIR_TP1_Test_Brain'
        self.TP_1_T1_Brain = 'TP1/T1_TP1_Test_Brain'

        self.sample_brain = 'data/Samples/FLAIR_brain_sample.nii.gz'
        self.resampled_FLAIR_TP1 = 'TP1/resample_FLAIR_TP1_test_to_sample.nii.gz'

        self.MNI_Brain = '/usr/local/fsl/data/standard/MNI152_T1_2mm_brain.nii.gz'
        self.resampled_FLAIR_TP1_To_MNI = 'TP1/resampled_FLAIR_TP1_test_to_sample_TO_MNI.nii.gz'
        self.resampled_FLAIR_TP1_To_MNI_mat = 'TP1/resampled_FLAIR_TP1_test_to_sample_TO_MNI.mat'
        self.registration_parameters = '-bins 256 -cost normcorr -searchrx -180 180 -searchry -180 180 -searchrz -180 180 -dof 7  -interp nearestneighbour'

        self.TP_1_T1_Brain_To_Resampled_FLAIR = 'TP1/reg_T1_TP1_test_to_resample_FLAIR_TP1.nii.gz'
        self.TP_1_T1_Brain_To_Resampled_FLAIR_mat = 'TP1/reg_T1_TP1_test_to_resample_FLAIR_TP1.mat'

        self.FLAIR_Lesion_Mask = 'TP1/FLAIR_Lesion_mask.nii.gz'
        self.TP_1_Masterfile = 'TP1/masterfile_TP1.txt'

        self.Classifer = 'data/Samples/mytraining'
        self.Bianca_output = 'TP1/bianca_output'
        self.Bianca_output_bin = 'TP1/bianca_output_bin.nii.gz'
        self.Bianca_output_bin_ero_dilM = 'TP1/bianca_output_bin_ero_kernel_box_2_dilM.nii.gz'

        self.TP_2_Flair_Brain = 'TP2/FLAIR_TP2_Test_Brain'
        self.TP_2_T1_Brain = 'TP2/T1_TP2_Test_Brain'

        self.registered_FLAIR_TP2 = 'TP2/reg_FLAIR_TP2_test_to_sample.nii.gz'
        self.registered_FLAIR_TP2_mat = 'TP2/reg_FLAIR_TP2_test_to_sample.nii.gz.mat'
        self.registered_FLAIR_TP2_To_MNI = 'TP2/reg_FLAIR_TP2_test_to_sample_TO_MNI.nii.gz'
        self.registered_FLAIR_TP2_To_MNI_mat = 'TP2/reg_FLAIR_TP2_test_to_sample_TO_MNI.mat'

        self.TP_2_T1_Brain_To_Registered_FLAIR = 'TP2/reg_T1_TP2_test_to_resample_FLAIR_TP2.nii.gz'
        self.TP_2_T1_Brain_To_Registered_FLAIR_mat = 'TP2/reg_T1_TP2_test_to_resample_FLAIR_TP2.mat'

        self.FLAIR_Lesion_Mask_2 = 'TP2/FLAIR_Lesion_mask.nii.gz'
        self.TP_2_Masterfile = 'TP2/masterfile_TP2.txt'

        self.Bianca_output_2 = 'TP2/bianca_output'
        self.Bianca_output_bin_2 = 'TP2/bianca_output_bin.nii.gz'
        self.Bianca_output_bin_ero_dilM_2 = 'TP2/bianca_output_bin_ero_kernel_box_2_dilM.nii.gz'

    def open_1(self):
        path = QFileDialog.getOpenFileName(self, 'Open a file', '',
                                           'All Files (*.*)')
        if path != ('', ''):
            print("File path : " + path[0])
            self.myTextBox.setText(path[0])
            self.TP_1_Flair = path[0]

    def open_2(self):
        path = QFileDialog.getOpenFileName(self, 'Open a file', '',
                                           'All Files (*.gz)')
        if path != ('', ''):
            print("File path : " + path[0])
            self.myTextBox_2.setText(path[0])
            self.TP_1_T1 = path[0]

    def open_1_1(self):
        path = QFileDialog.getOpenFileName(self, 'Open a file', '',
                                           'All Files (*.*)')
        if path != ('', ''):
            print("File path : " + path[0])
            self.myTextBox_3.setText(path[0])
            self.TP_1_Flair = path[0]

    def open_2_1(self):
        path = QFileDialog.getOpenFileName(self, 'Open a file', '',
                                           'All Files (*.gz)')
        if path != ('', ''):
            print("File path : " + path[0])
            self.myTextBox_4.setText(path[0])
            self.TP_1_T1 = path[0]

    def bet(self, outputbox):
        outputbox.insertPlainText(f" bet {self.TP_1_Flair} {self.TP_1_Flair_Brain} \n")
        QApplication.processEvents()
        p = os.popen(f" bet {self.TP_1_Flair} {self.TP_1_Flair_Brain}")
        if p:
            output = p.read()
            outputbox.insertPlainText(output)

        QApplication.processEvents()
        outputbox.insertPlainText(f" bet {self.TP_1_T1} {self.TP_1_T1_Brain} \n")
        p = os.popen(f" bet {self.TP_1_T1} {self.TP_1_T1_Brain}")
        if p:
            output = p.read()
            outputbox.insertPlainText(output)

        outputbox.insertPlainText("\n")
        QApplication.processEvents()

    def resample_flair(self, outputbox):
        # x = os.system(
        #     f"flirt -in {self.TP_1_Flair_Brain} -ref {self.sample_brain} -out {self.resampled_FLAIR_TP1} -applyxfm")

        outputbox.insertPlainText(
            f"flirt -in {self.TP_1_Flair_Brain} -ref {self.sample_brain} -out {self.resampled_FLAIR_TP1} -applyxfm \n")
        outputbox.insertPlainText("\n")
        QApplication.processEvents()
        p = os.popen(
            f"flirt -in {self.TP_1_Flair_Brain} -ref {self.sample_brain} -out {self.resampled_FLAIR_TP1} -applyxfm")
        if p:
            output = p.read()
            outputbox.insertPlainText(output)
        QApplication.processEvents()

    def register_to_MNI(self, outputbox):
        outputbox.insertPlainText(
            f"flirt -in {self.resampled_FLAIR_TP1} -ref {self.MNI_Brain} -out {self.resampled_FLAIR_TP1_To_MNI} -omat {self.resampled_FLAIR_TP1_To_MNI_mat} {self.registration_parameters} \n")
        outputbox.insertPlainText("\n")
        QApplication.processEvents()

        p = os.popen(
            f"flirt -in {self.resampled_FLAIR_TP1} -ref {self.MNI_Brain} -out {self.resampled_FLAIR_TP1_To_MNI} -omat {self.resampled_FLAIR_TP1_To_MNI_mat} {self.registration_parameters}")
        if p:
            output = p.read()
            outputbox.insertPlainText(output)
        QApplication.processEvents()

    def register_t1_to_flair(self, outputbox):
        outputbox.insertPlainText(
            f"flirt -in {self.TP_1_T1_Brain} -ref {self.resampled_FLAIR_TP1} -out {self.TP_1_T1_Brain_To_Resampled_FLAIR} -omat {self.TP_1_T1_Brain_To_Resampled_FLAIR_mat} {self.registration_parameters} \n")
        outputbox.insertPlainText("\n")
        QApplication.processEvents()

        p = os.popen(
            f"flirt -in {self.TP_1_T1_Brain} -ref {self.resampled_FLAIR_TP1} -out {self.TP_1_T1_Brain_To_Resampled_FLAIR} -omat {self.TP_1_T1_Brain_To_Resampled_FLAIR_mat} {self.registration_parameters}")
        if p:
            output = p.read()
            outputbox.insertPlainText(output)
        QApplication.processEvents()

    def generate_masterfile(self, outputbox):
        file = open(self.TP_1_Masterfile, 'w')
        file.write(self.resampled_FLAIR_TP1 + ' ')
        file.write(self.TP_1_T1_Brain_To_Resampled_FLAIR + ' ')
        file.write(self.resampled_FLAIR_TP1_To_MNI_mat + ' ')
        file.write(self.FLAIR_Lesion_Mask + ' ')
        outputbox.insertPlainText(
            "Generating Masterfile \n")
        outputbox.insertPlainText("\n")
        QApplication.processEvents()

    def run_bianca(self, outputbox):
        outputbox.insertPlainText(
             f"bianca --singlefile={self.TP_1_Masterfile} --loadclassifierdata={self.Classifer} --querysubjectnum=1 --brainmaskfeaturenum=1 --featuresubset=1,2 --matfeaturenum=3 -o {self.Bianca_output} -v \n")
        outputbox.insertPlainText("\n")
        QApplication.processEvents()

        p = os.popen(
             f"bianca --singlefile={self.TP_1_Masterfile} --loadclassifierdata={self.Classifer} --querysubjectnum=1 --brainmaskfeaturenum=1 --featuresubset=1,2 --matfeaturenum=3 -o {self.Bianca_output} -v")
        if p:
            output = p.read()
            outputbox.insertPlainText(output)
        QApplication.processEvents()

    def bianca_binary(self):
        fslmaths(self.Bianca_output).thr(0.9).bin().run(self.Bianca_output_bin)

    def bianca_open(self, outputbox):
        outputbox.insertPlainText(
             f"fslmaths {self.Bianca_output_bin} -kernel box 2 -ero -dilM {self.Bianca_output_bin_ero_dilM} \n")
        outputbox.insertPlainText("\n")
        QApplication.processEvents()

        p = os.popen(
             f"fslmaths {self.Bianca_output_bin} -kernel box 2 -ero -dilM {self.Bianca_output_bin_ero_dilM}")
        if p:
            output = p.read()
            outputbox.insertPlainText(output)
        QApplication.processEvents()

    def run_all_bianca(self):
        self.bet(self.editorOutput)
        time.sleep(1)
        self.resample_flair(self.editorOutput)
        self.register_to_MNI(self.editorOutput)
        self.register_t1_to_flair(self.editorOutput)
        self.generate_masterfile(self.editorOutput)
        self.run_bianca(self.editorOutput)
        self.bianca_binary()
        self.bianca_open(self.editorOutput)
        self.editorOutput.insertPlainText("Completed!")

    def open_fsleyes(self):
        x = os.system(f"fsleyes {self.resampled_FLAIR_TP1} {self.Bianca_output_bin_ero_dilM} -dr 0 1 -cm red-yellow &")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TP1()
    sys.exit(app.exec_())
