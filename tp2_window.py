import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, \
    QFileDialog, QTextEdit, QLabel, QPlainTextEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt
from fsl.wrappers import bet
import os
import fsl
from fsl.wrappers.fslmaths import fslmaths
import time


class TP2(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'MS Tool'
        self.left = 0
        self.top = 0
        self.width = 600
        self.height = 200
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.table_widget = TP2Window(self)
        self.setCentralWidget(self.table_widget)

        self.show()


class TP2Window(QWidget):

    def __init__(self, parent):
        self.create_directories()
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        # self.tabs.TabPosition()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

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
        # self.tabs.resize(300, 200)

        # Add tabs
        self.tab1_1 = QTabWidget()
        self.tab1_2 = QTabWidget()

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

        # self.tab2_1.layout = QVBoxLayout(self)
        file_btn_7 = QPushButton("Choose File for Flair Timepoint 2")
        self.myTextBox_7 = QTextEdit()
        self.myTextBox_7.setFixedHeight(40)
        verify_7 = QLabel("Please verify the file path")
        verify_7.setAlignment(Qt.AlignRight)

        file_btn_8 = QPushButton("Choose File for T1 Timepoint 2")
        self.myTextBox_8 = QTextEdit()
        self.myTextBox_8.setFixedHeight(40)
        verify_8 = QLabel("Please verify the file path")
        verify_8.setAlignment(Qt.AlignRight)

        bianca_obtain = QPushButton("Obtain the Bianca Output")

        self.editorOutput3 = QPlainTextEdit()
        self.editorOutput3.setStyleSheet("color: #ffffff; background-color: rgb(0,0,0);")

        open_fsl = QPushButton("Open in FSLEyes")

        self.tab1_1.layout.addWidget(file_btn_3)
        self.tab1_1.layout.addWidget(self.myTextBox_3)
        self.tab1_1.layout.addWidget(verify_3)

        self.tab1_1.layout.addWidget(file_btn_4)
        self.tab1_1.layout.addWidget(self.myTextBox_4)
        self.tab1_1.layout.addWidget(verify_4)

        self.tab1_1.layout.addWidget(file_btn_7)
        self.tab1_1.layout.addWidget(self.myTextBox_7)
        self.tab1_1.layout.addWidget(verify_7)

        self.tab1_1.layout.addWidget(file_btn_8)
        self.tab1_1.layout.addWidget(self.myTextBox_8)
        self.tab1_1.layout.addWidget(verify_8)

        self.tab1_1.layout.addWidget(bianca_obtain)

        self.tab1_1.layout.addWidget(self.editorOutput3, 7)

        self.tab1_1.layout.addWidget(open_fsl)

        file_btn_3.clicked.connect(self.open_1_1)
        file_btn_4.clicked.connect(self.open_2_1)
        file_btn_7.clicked.connect(self.open_5)
        file_btn_8.clicked.connect(self.open_6)
        bianca_obtain.clicked.connect(self.run_all_bianca)
        open_fsl.clicked.connect(self.open_fsleyes)

        self.tab1_1.setLayout(self.tab1_1.layout)

        # Troubleshoot Results Tab for Timepoint 1
        self.tab1_2.addTab(self.tab1, "Timepoint 1")
        self.tab1_2.addTab(self.tab2, "Timepoint 2")
        self.tab1_2.addTab(self.tab3, "Longitudinal Analysis")

        self.tab1.layout = QVBoxLayout(self)
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

        self.editorOutput4 = QPlainTextEdit()
        self.editorOutput4.setStyleSheet("color: #ffffff; background-color: rgb(0,0,0);")

        open_fsl2 = QPushButton("Open in FSLEyes")

        self.tab1.layout.addWidget(file_btn)
        self.tab1.layout.addWidget(self.myTextBox)
        self.tab1.layout.addWidget(verify_1)

        self.tab1.layout.addWidget(file_btn_2)
        self.tab1.layout.addWidget(self.myTextBox_2)
        self.tab1.layout.addWidget(verify_2)

        self.tab1.layout.addWidget(bet_btn)
        self.tab1.layout.addWidget(resample)
        self.tab1.layout.addWidget(register_flair)
        self.tab1.layout.addWidget(register_T1)
        self.tab1.layout.addWidget(Create_MF)
        self.tab1.layout.addWidget(BIANCA)
        self.tab1.layout.addWidget(Binary_mask)
        self.tab1.layout.addWidget(Ero_Dil)
        self.tab1.layout.addWidget(self.editorOutput4, 7)
        self.tab1.layout.addWidget(open_fsl2)

        self.tab1.setLayout(self.tab1.layout)

        file_btn.clicked.connect(self.open_1)  # connect clicked to self.open()
        file_btn_2.clicked.connect(self.open_2)  # connect clicked to self.open()
        bet_btn.clicked.connect(lambda: self.bet(self.editorOutput4))
        resample.clicked.connect(lambda: self.resample_flair(self.editorOutput4))
        register_flair.clicked.connect(lambda: self.register_to_MNI(self.editorOutput4))
        register_T1.clicked.connect(lambda: self.register_t1_to_flair(self.editorOutput4))
        Create_MF.clicked.connect(lambda: self.generate_masterfile(self.editorOutput4))
        BIANCA.clicked.connect(lambda: self.run_bianca(self.editorOutput4))
        Binary_mask.clicked.connect( self.bianca_binary)
        Ero_Dil.clicked.connect(lambda: self.bianca_open(self.editorOutput4))
        open_fsl2.clicked.connect(self.open_fsleyes2)

        # Troubleshoot Results for Tab Timepoint 2
        self.tab2.layout = QVBoxLayout(self)
        file_btn_5 = QPushButton("Choose File for Flair Timepoint 2")
        self.myTextBox_5 = QTextEdit()
        self.myTextBox_5.setFixedHeight(40)
        verify_5 = QLabel("Please verify the file path")
        verify_5.setAlignment(Qt.AlignRight)

        file_btn_6 = QPushButton("Choose File for T1 Timepoint 2")
        self.myTextBox_6 = QTextEdit()
        self.myTextBox_6.setFixedHeight(40)
        verify_6 = QLabel("Please verify the file path")
        verify_6.setAlignment(Qt.AlignRight)

        bet_btn_2 = QPushButton("Run Brain Extraction")
        resample_2 = QPushButton("Register the TP2 FLAIR Image to T1 FLAIR Image")
        register_flair_2 = QPushButton("Register the Resampled Brain to MNI Space")
        register_T1_2 = QPushButton("Register the T2 Image onto the Resampled Flair Image")
        Create_MF_2 = QPushButton("Create a Master file with the Generated Data for BIANCA")
        BIANCA_2 = QPushButton("Run the BIANCA Algorithm")
        Binary_mask_2 = QPushButton("Create a Binary Mask from the BIANCA Output")
        Ero_Dil_2 = QPushButton("Refine the Binary Mask")

        self.editorOutput5 = QPlainTextEdit()
        self.editorOutput5.setStyleSheet("color: #ffffff; background-color: rgb(0,0,0);")

        open_fsl3 = QPushButton("Open in FSLEyes")


        self.tab2.layout.addWidget(file_btn_5)
        self.tab2.layout.addWidget(self.myTextBox_5)
        self.tab2.layout.addWidget(verify_5)

        self.tab2.layout.addWidget(file_btn_6)
        self.tab2.layout.addWidget(self.myTextBox_6)
        self.tab2.layout.addWidget(verify_6)

        self.tab2.layout.addWidget(bet_btn_2)
        self.tab2.layout.addWidget(resample_2)
        self.tab2.layout.addWidget(register_flair_2)
        self.tab2.layout.addWidget(register_T1_2)
        self.tab2.layout.addWidget(Create_MF_2)
        self.tab2.layout.addWidget(BIANCA_2)
        self.tab2.layout.addWidget(Binary_mask_2)
        self.tab2.layout.addWidget(Ero_Dil_2)
        self.tab2.layout.addWidget(self.editorOutput5, 7)
        self.tab2.layout.addWidget(open_fsl3)

        file_btn_5.clicked.connect(self.open_3)  # connect clicked to self.open()
        file_btn_6.clicked.connect(self.open_4)  # connect clicked to self.open()
        bet_btn_2.clicked.connect(lambda: self.bet_2(self.editorOutput5))
        resample_2.clicked.connect(lambda: self.register_tp2_to_tp1(self.editorOutput5))
        register_flair_2.clicked.connect(lambda: self.register_to_MNI_2(self.editorOutput5))
        register_T1_2.clicked.connect(lambda: self.register_t1_to_flair_2(self.editorOutput5))
        Create_MF_2.clicked.connect(lambda: self.generate_masterfile_2(self.editorOutput5))
        BIANCA_2.clicked.connect(lambda: self.run_bianca_2(self.editorOutput5))
        Binary_mask_2.clicked.connect(self.bianca_binary_2)
        Ero_Dil_2.clicked.connect(lambda: self.bianca_open_2(self.editorOutput5))
        open_fsl3.clicked.connect(self.open_fsleyes3)

        self.tab2.setLayout(self.tab2.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        # Create Third Tab
        self.tab3.layout = QVBoxLayout(self)

        Subtraction = QPushButton("Obtain the New Lesion Mask")
        LostLesion = QPushButton("Obtain the Old Lesion Mask")
        TotalLesion = QPushButton("Obtain the Total Lesion Mask")

        self.editorOutput6 = QPlainTextEdit()
        self.editorOutput6.setStyleSheet("color: #ffffff; background-color: rgb(0,0,0);")

        Open_fsl_btn = QPushButton("Open the output in FSLEyes")

        self.tab3.layout.addWidget(Subtraction)
        self.tab3.layout.addWidget(LostLesion)
        self.tab3.layout.addWidget(TotalLesion)
        self.tab3.layout.addWidget(self.editorOutput6)
        self.tab3.layout.addWidget(Open_fsl_btn)

        self.tab3.setLayout(self.tab3.layout)

        Subtraction.clicked.connect(lambda: self.subtract_lesions(self.editorOutput6))
        LostLesion.clicked.connect(lambda: self.lost_lesions(self.editorOutput6))
        TotalLesion.clicked.connect(lambda: self.total_lesions(self.editorOutput6))

        Open_fsl_btn.clicked.connect(self.open_fsleyes4)

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

    def open_3(self):
        path = QFileDialog.getOpenFileName(self, 'Open a file', '',
                                           'All Files (*.gz)')
        if path != ('', ''):
            print("File path : " + path[0])
            self.myTextBox_5.setText(path[0])
            self.TP_2_FLAIR = path[0]
            print("Here" + self.TP_2_FLAIR)

    def open_4(self):
        path = QFileDialog.getOpenFileName(self, 'Open a file', '',
                                           'All Files (*.gz)')
        if path != ('', ''):
            print("File path : " + path[0])
            self.myTextBox_6.setText(path[0])
            self.TP_2_T1 = path[0]
            print("Here" + self.TP_2_T1)

    def open_5(self):
        path = QFileDialog.getOpenFileName(self, 'Open a file', '',
                                           'All Files (*.gz)')
        if path != ('', ''):
            print("File path : " + path[0])
            self.myTextBox_7.setText(path[0])
            self.TP_2_FLAIR = path[0]
            print("Here" + self.TP_2_FLAIR)

    def open_6(self):
        path = QFileDialog.getOpenFileName(self, 'Open a file', '',
                                           'All Files (*.gz)')
        if path != ('', ''):
            print("File path : " + path[0])
            self.myTextBox_8.setText(path[0])
            self.TP_2_T1 = path[0]
            print("Here" + self.TP_2_T1)

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

    def bet_2(self, outputbox):
        outputbox.insertPlainText(f" bet {self.TP_2_FLAIR} {self.TP_2_Flair_Brain} \n")
        QApplication.processEvents()
        p = os.popen(f" bet {self.TP_2_FLAIR} {self.TP_2_Flair_Brain}")
        if p:
            output = p.read()
            outputbox.insertPlainText(output)

        QApplication.processEvents()
        outputbox.insertPlainText(f" bet {self.TP_2_T1} {self.TP_2_T1_Brain} \n")
        p = os.popen(f" bet {self.TP_2_T1} {self.TP_2_T1_Brain}")
        if p:
            output = p.read()
            outputbox.insertPlainText(output)

        outputbox.insertPlainText("\n")
        QApplication.processEvents()

    def resample_flair(self, outputbox):
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

    def register_tp2_to_tp1(self, outputbox):
        outputbox.insertPlainText(
            f"flirt -in {self.TP_2_Flair_Brain} -ref {self.resampled_FLAIR_TP1} -out {self.registered_FLAIR_TP2} -omat {self.registered_FLAIR_TP2_mat} {self.registration_parameters} \n")
        outputbox.insertPlainText("\n")
        QApplication.processEvents()
        p = os.popen(
            f"flirt -in {self.TP_2_Flair_Brain} -ref {self.resampled_FLAIR_TP1} -out {self.registered_FLAIR_TP2} -omat {self.registered_FLAIR_TP2_mat} {self.registration_parameters}")
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

    def register_to_MNI_2(self, outputbox):
        outputbox.insertPlainText(
            f"flirt -in {self.registered_FLAIR_TP2} -ref {self.MNI_Brain} -out {self.registered_FLAIR_TP2_To_MNI} -omat {self.registered_FLAIR_TP2_To_MNI_mat} {self.registration_parameters} \n")
        outputbox.insertPlainText("\n")
        QApplication.processEvents()

        p = os.popen(
            f"flirt -in {self.registered_FLAIR_TP2} -ref {self.MNI_Brain} -out {self.registered_FLAIR_TP2_To_MNI} -omat {self.registered_FLAIR_TP2_To_MNI_mat} {self.registration_parameters}")
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

    def register_t1_to_flair_2(self, outputbox):
        outputbox.insertPlainText(
            f"flirt -in {self.TP_2_T1_Brain} -ref {self.registered_FLAIR_TP2} -out {self.TP_2_T1_Brain_To_Registered_FLAIR} -omat {self.TP_2_T1_Brain_To_Registered_FLAIR_mat} {self.registration_parameters} \n")
        outputbox.insertPlainText("\n")
        QApplication.processEvents()

        p = os.popen(
            f"flirt -in {self.TP_2_T1_Brain} -ref {self.registered_FLAIR_TP2} -out {self.TP_2_T1_Brain_To_Registered_FLAIR} -omat {self.TP_2_T1_Brain_To_Registered_FLAIR_mat} {self.registration_parameters}")
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
            "Generating Masterfile 1 \n")
        outputbox.insertPlainText("\n")
        QApplication.processEvents()

    def generate_masterfile_2(self, outputbox):
        file = open(self.TP_2_Masterfile, 'w')
        file.write(self.registered_FLAIR_TP2 + ' ')
        file.write(self.TP_2_T1_Brain_To_Registered_FLAIR + ' ')
        file.write(self.registered_FLAIR_TP2_To_MNI_mat + ' ')
        file.write(self.FLAIR_Lesion_Mask_2 + ' ')

        outputbox.insertPlainText(
            "Generating Masterfile 2 \n")
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

    def run_bianca_2(self, outputbox):
        outputbox.insertPlainText(
            f"bianca --singlefile={self.TP_2_Masterfile} --loadclassifierdata={self.Classifer} --querysubjectnum=1 --brainmaskfeaturenum=1 --featuresubset=1,2 --matfeaturenum=3 -o {self.Bianca_output_2} -v \n")
        outputbox.insertPlainText("\n")
        QApplication.processEvents()

        p = os.popen(
            f"bianca --singlefile={self.TP_2_Masterfile} --loadclassifierdata={self.Classifer} --querysubjectnum=1 --brainmaskfeaturenum=1 --featuresubset=1,2 --matfeaturenum=3 -o {self.Bianca_output_2} -v")
        if p:
            output = p.read()
            outputbox.insertPlainText(output)
        QApplication.processEvents()

    def bianca_binary(self):
        fslmaths(self.Bianca_output).thr(0.9).bin().run(self.Bianca_output_bin)

    def bianca_binary_2(self):
        fslmaths(self.Bianca_output_2).thr(0.9).bin().run(self.Bianca_output_bin_2)

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

    def bianca_open_2(self, outputbox):
        outputbox.insertPlainText(
            f"fslmaths {self.Bianca_output_bin_2} -kernel box 2 -ero -dilM {self.Bianca_output_bin_ero_dilM_2} \n")
        outputbox.insertPlainText("\n")
        QApplication.processEvents()

        p = os.popen(
            f"fslmaths {self.Bianca_output_bin_2} -kernel box 2 -ero -dilM {self.Bianca_output_bin_ero_dilM_2}")
        if p:
            output = p.read()
            outputbox.insertPlainText(output)
        QApplication.processEvents()

    def subtract_lesions(self, outputbox):
        outputbox.insertPlainText(
            f"fslmaths {self.Bianca_output_bin_ero_dilM_2} -sub {self.Bianca_output_bin_ero_dilM} New_lesion_mask.nii.gz \n")
        outputbox.insertPlainText("\n")
        QApplication.processEvents()

        p = os.popen(
            f"fslmaths {self.Bianca_output_bin_ero_dilM_2} -sub {self.Bianca_output_bin_ero_dilM} New_lesion_mask.nii.gz")
        if p:
            output = p.read()
            outputbox.insertPlainText(output)
        QApplication.processEvents()

    def lost_lesions(self, outputbox):
        outputbox.insertPlainText(
            f"fslmaths {self.Bianca_output_bin_ero_dilM} -sub {self.Bianca_output_bin_ero_dilM_2} Old_lesion_mask.nii.gz \n")
        outputbox.insertPlainText("\n")
        QApplication.processEvents()

        p = os.popen(
            f"fslmaths {self.Bianca_output_bin_ero_dilM} -sub {self.Bianca_output_bin_ero_dilM_2} Old_lesion_mask.nii.gz")
        if p:
            output = p.read()
            outputbox.insertPlainText(output)
        QApplication.processEvents()

    def total_lesions(self, outputbox):
        outputbox.insertPlainText(
            f"fslmaths {self.Bianca_output_bin_ero_dilM_2} -add {self.Bianca_output_bin_ero_dilM} Total_lesion_mask.nii.gz \n")
        outputbox.insertPlainText("\n")
        QApplication.processEvents()

        p = os.popen(
            f"fslmaths {self.Bianca_output_bin_ero_dilM_2} -add {self.Bianca_output_bin_ero_dilM} Total_lesion_mask.nii.gz")
        if p:
            output = p.read()
            outputbox.insertPlainText(output)
        QApplication.processEvents()

    # def open_in_bianca(self):
    #     x = os.system(f"fsleyes {self.Bianca_output_bin_ero_dilM_2} -add {self.Bianca_output_bin_ero_dilM} Total_lesion_mask.nii.gz")

    def run_all_bianca(self):
        self.bet(self.editorOutput3)
        self.resample_flair(self.editorOutput3)
        self.register_to_MNI(self.editorOutput3)
        self.register_t1_to_flair(self.editorOutput3)
        self.generate_masterfile(self.editorOutput3)
        self.run_bianca(self.editorOutput3)
        self.bianca_binary()
        self.bianca_open(self.editorOutput3)

        self.bet_2(self.editorOutput3)
        self.register_tp2_to_tp1(self.editorOutput3)
        self.register_to_MNI_2(self.editorOutput3)
        self.register_t1_to_flair_2(self.editorOutput3)
        self.generate_masterfile_2(self.editorOutput3)
        self.run_bianca_2(self.editorOutput3)
        self.bianca_binary_2()
        self.bianca_open_2(self.editorOutput3)

        self.subtract_lesions(self.editorOutput3)
        self.lost_lesions(self.editorOutput3)
        self.total_lesions(self.editorOutput3)

        self.editorOutput3.insertPlainText("Completed!")

    def open_fsleyes(self):
        x = os.system(
            f"fsleyes {self.resampled_FLAIR_TP1} {self.registered_FLAIR_TP2}  {self.Bianca_output_bin_ero_dilM_2} -dr 0 1 -cm red-yellow &")

    def open_fsleyes2(self):
        x = os.system(f"fsleyes {self.resampled_FLAIR_TP1} {self.Bianca_output_bin_ero_dilM} -dr 0 1 -cm red-yellow &")

    def open_fsleyes3(self):
        x = os.system(f"fsleyes {self.registered_FLAIR_TP2} {self.Bianca_output_bin_ero_dilM_2} -dr 0 1 -cm red-yellow &")

    def open_fsleyes4(self):
        x = os.system(f"fsleyes {self.Bianca_output_bin_ero_dilM_2} -dr 0 1 -cm red-yellow New_lesion_mask.nii.gz -dr 0 1 -cm blue-lightblue  Old_lesion_mask.nii.gz -dr 0 1 -cm blue-blue Total_lesion_mask.nii.gz -dr 0 1 -cm green &")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TP2()
    sys.exit(app.exec_())
