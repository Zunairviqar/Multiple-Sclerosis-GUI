import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, \
    QFileDialog, QTextEdit, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt
from fsl.wrappers import bet
import os
import fsl
from fsl.wrappers.fslmaths import fslmaths


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'MS Tool'
        self.left = 0
        self.top = 0
        self.width = 600
        self.height = 200
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()


class MyTableWidget(QWidget):

    def __init__(self, parent):
        self.create_directories()
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        # self.tabs.TabPosition()
        self.tab1 = QTabWidget()
        self.tab2 = QTabWidget()
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
        self.tabs.addTab(self.tab1, "Timepoint 1")
        self.tabs.addTab(self.tab2, "Timepoint 2")
        self.tabs.addTab(self.tab3, "Longitudinal Analysis")

        self.tab1_1 = QWidget()
        self.tab1_2 = QWidget()

        # Create Timepoint 1 inner tab
        self.tab1.addTab(self.tab1_1, "Rapid Results")
        self.tab1.addTab(self.tab1_2, "Troubleshoot")

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

        self.tab1_1.layout.addWidget(file_btn_3)
        self.tab1_1.layout.addWidget(self.myTextBox_3)
        self.tab1_1.layout.addWidget(verify_3)

        self.tab1_1.layout.addWidget(file_btn_4)
        self.tab1_1.layout.addWidget(self.myTextBox_4)
        self.tab1_1.layout.addWidget(verify_4)

        self.tab1_1.layout.addWidget(bianca_obtain)

        file_btn_3.clicked.connect(self.open_1_1)
        file_btn_4.clicked.connect(self.open_2_1)
        bianca_obtain.clicked.connect(self.run_all_bianca)

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

        self.tab1_2.setLayout(self.tab1_2.layout)

        file_btn.clicked.connect(self.open_1)  # connect clicked to self.open()
        file_btn_2.clicked.connect(self.open_2)  # connect clicked to self.open()
        bet_btn.clicked.connect(self.bet)
        resample.clicked.connect(self.resample_flair)
        register_flair.clicked.connect(self.register_to_MNI)
        register_T1.clicked.connect(self.register_t1_to_flair)
        Create_MF.clicked.connect(self.generate_masterfile)
        BIANCA.clicked.connect(self.run_bianca)
        Binary_mask.clicked.connect(self.bianca_binary)
        Ero_Dil.clicked.connect(self.bianca_open)

        # # Create second tab
        self.tab2_1 = QWidget()
        self.tab2_2 = QWidget()

        # Create Timepoint 2 Inner tabs
        self.tab2.addTab(self.tab2_1, "Rapid Results")
        self.tab2.addTab(self.tab2_2, "Troubleshoot")

        # RAPID RESULTS TAB COMES HERE
        self.tab2_1.layout = QVBoxLayout(self)
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

        bianca_obtain_2 = QPushButton("Obtain the Bianca Output")

        self.tab2_1.layout.addWidget(file_btn_7)
        self.tab2_1.layout.addWidget(self.myTextBox_7)
        self.tab2_1.layout.addWidget(verify_7)

        self.tab2_1.layout.addWidget(file_btn_8)
        self.tab2_1.layout.addWidget(self.myTextBox_8)
        self.tab2_1.layout.addWidget(verify_8)

        self.tab2_1.layout.addWidget(bianca_obtain_2)

        self.tab2_1.setLayout(self.tab2_1.layout)

        file_btn_7.clicked.connect(self.open_5)
        file_btn_8.clicked.connect(self.open_6)
        bianca_obtain_2.clicked.connect(self.run_all_bianca_2)

        # Troubleshoot Results Tab Timepoint 2
        self.tab2_2.layout = QVBoxLayout(self)
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

        self.tab2_2.layout.addWidget(file_btn_5)
        self.tab2_2.layout.addWidget(self.myTextBox_5)
        self.tab2_2.layout.addWidget(verify_5)

        self.tab2_2.layout.addWidget(file_btn_6)
        self.tab2_2.layout.addWidget(self.myTextBox_6)
        self.tab2_2.layout.addWidget(verify_6)

        self.tab2_2.layout.addWidget(bet_btn_2)
        self.tab2_2.layout.addWidget(resample_2)
        self.tab2_2.layout.addWidget(register_flair_2)
        self.tab2_2.layout.addWidget(register_T1_2)
        self.tab2_2.layout.addWidget(Create_MF_2)
        self.tab2_2.layout.addWidget(BIANCA_2)
        self.tab2_2.layout.addWidget(Binary_mask_2)
        self.tab2_2.layout.addWidget(Ero_Dil_2)

        file_btn_5.clicked.connect(self.open_3)  # connect clicked to self.open()
        file_btn_6.clicked.connect(self.open_4)  # connect clicked to self.open()
        bet_btn_2.clicked.connect(self.bet_2)
        resample_2.clicked.connect(self.register_tp2_to_tp1)
        register_flair_2.clicked.connect(self.register_to_MNI_2)
        register_T1_2.clicked.connect(self.register_t1_to_flair_2)
        Create_MF_2.clicked.connect(self.generate_masterfile_2)
        BIANCA_2.clicked.connect(self.run_bianca_2)
        Binary_mask_2.clicked.connect(self.bianca_binary_2)
        Ero_Dil_2.clicked.connect(self.bianca_open_2)

        self.tab2_2.setLayout(self.tab2_2.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        # Create Third Tab
        self.tab3.layout = QVBoxLayout(self)

        Subtraction = QPushButton("Obtain the New Lesion Mask")
        LostLesion = QPushButton("Obtain the Old Lesion Mask")
        TotalLesion = QPushButton("Obtain the Total Lesion Mask")
        Open_bianca_btn = QPushButton("Open the output in FSLEyes")

        self.tab3.layout.addWidget(Subtraction)
        self.tab3.layout.addWidget(LostLesion)
        self.tab3.layout.addWidget(TotalLesion)
        self.tab3.layout.addWidget(Open_bianca_btn)

        self.tab3.setLayout(self.tab3.layout)

        Subtraction.clicked.connect(self.subtract_lesions)
        LostLesion.clicked.connect(self.lost_lesions)
        TotalLesion.clicked.connect(self.total_lesions)
        # Open_bianca_btn.clicked.connect(self.open_in_bianca)

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

    def bet(self):
        bet(self.TP_1_Flair, self.TP_1_Flair_Brain)
        bet(self.TP_1_T1, self.TP_1_T1_Brain)

    def bet_2(self):
        bet(self.TP_2_FLAIR, self.TP_2_Flair_Brain)
        bet(self.TP_2_T1, self.TP_2_T1_Brain)

    def resample_flair(self):
        x = os.system(
            f"flirt -in {self.TP_1_Flair_Brain} -ref {self.sample_brain} -out {self.resampled_FLAIR_TP1} -applyxfm")

    def register_tp2_to_tp1(self):
        x = os.system(
            f"flirt -in {self.TP_2_Flair_Brain} -ref {self.resampled_FLAIR_TP1} -out {self.registered_FLAIR_TP2} -omat {self.registered_FLAIR_TP2_mat} {self.registration_parameters}")

    def register_to_MNI(self):
        x = os.system(
            f"flirt -in {self.resampled_FLAIR_TP1} -ref {self.MNI_Brain} -out {self.resampled_FLAIR_TP1_To_MNI} -omat {self.resampled_FLAIR_TP1_To_MNI_mat} {self.registration_parameters}")

    def register_to_MNI_2(self):
        x = os.system(
            f"flirt -in {self.registered_FLAIR_TP2} -ref {self.MNI_Brain} -out {self.registered_FLAIR_TP2_To_MNI} -omat {self.registered_FLAIR_TP2_To_MNI_mat} {self.registration_parameters}")

    def register_t1_to_flair(self):
        x = os.system(
            f"flirt -in {self.TP_1_T1_Brain} -ref {self.resampled_FLAIR_TP1} -out {self.TP_1_T1_Brain_To_Resampled_FLAIR} -omat {self.TP_1_T1_Brain_To_Resampled_FLAIR_mat} {self.registration_parameters}")

    def register_t1_to_flair_2(self):
        x = os.system(
            f"flirt -in {self.TP_2_T1_Brain} -ref {self.registered_FLAIR_TP2} -out {self.TP_2_T1_Brain_To_Registered_FLAIR} -omat {self.TP_2_T1_Brain_To_Registered_FLAIR_mat} {self.registration_parameters}")

    def generate_masterfile(self):
        file = open(self.TP_1_Masterfile, 'w')
        file.write(self.resampled_FLAIR_TP1 + ' ')
        file.write(self.TP_1_T1_Brain_To_Resampled_FLAIR + ' ')
        file.write(self.resampled_FLAIR_TP1_To_MNI_mat + ' ')
        file.write(self.FLAIR_Lesion_Mask + ' ')

    def generate_masterfile_2(self):
        file = open(self.TP_2_Masterfile, 'w')
        file.write(self.registered_FLAIR_TP2 + ' ')
        file.write(self.TP_2_T1_Brain_To_Registered_FLAIR + ' ')
        file.write(self.registered_FLAIR_TP2_To_MNI_mat + ' ')
        file.write(self.FLAIR_Lesion_Mask_2 + ' ')

    def run_bianca(self):
        x = os.system(
            f"bianca --singlefile={self.TP_1_Masterfile} --loadclassifierdata={self.Classifer} --querysubjectnum=1 --brainmaskfeaturenum=1 --featuresubset=1,2 --matfeaturenum=3 -o {self.Bianca_output} -v")

    def run_bianca_2(self):
        x = os.system(
            f"bianca --singlefile={self.TP_2_Masterfile} --loadclassifierdata={self.Classifer} --querysubjectnum=1 --brainmaskfeaturenum=1 --featuresubset=1,2 --matfeaturenum=3 -o {self.Bianca_output_2} -v")

    def bianca_binary(self):
        fslmaths(self.Bianca_output).thr(0.9).bin().run(self.Bianca_output_bin)

    def bianca_binary_2(self):
        fslmaths(self.Bianca_output_2).thr(0.9).bin().run(self.Bianca_output_bin_2)

    def bianca_open(self):
        x = os.system(f"fslmaths {self.Bianca_output_bin} -kernel box 2 -ero -dilM {self.Bianca_output_bin_ero_dilM}")

    def bianca_open_2(self):
        x = os.system(
            f"fslmaths {self.Bianca_output_bin_2} -kernel box 2 -ero -dilM {self.Bianca_output_bin_ero_dilM_2}")

    def run_all_bianca(self):
        self.bet()
        self.resample_flair()
        self.register_to_MNI()
        self.register_t1_to_flair()
        self.generate_masterfile()
        self.run_bianca()
        self.bianca_binary()
        self.bianca_open()

    def run_all_bianca_2(self):
        self.bet_2()
        self.register_tp2_to_tp1()
        self.register_to_MNI_2()
        self.register_t1_to_flair_2()
        self.generate_masterfile_2()
        self.run_bianca_2()
        self.bianca_binary_2()
        self.bianca_open_2()

    def subtract_lesions(self):
        x = os.system(
            f"fslmaths {self.Bianca_output_bin_ero_dilM_2} -sub {self.Bianca_output_bin_ero_dilM} New_lesion_mask.nii.gz")

    def lost_lesions(self):
        x = os.system(
            f"fslmaths {self.Bianca_output_bin_ero_dilM} -sub {self.Bianca_output_bin_ero_dilM_2} Old_lesion_mask.nii.gz")

    def total_lesions(self):
        x = os.system(
            f"fslmaths {self.Bianca_output_bin_ero_dilM_2} -add {self.Bianca_output_bin_ero_dilM} Total_lesion_mask.nii.gz")

    def open_in_bianca(self):
        x = os.system(f"fsleyes {self.Bianca_output_bin_ero_dilM_2} -add {self.Bianca_output_bin_ero_dilM} Total_lesion_mask.nii.gz")
# TP2/reg_FLAIR_TP2_test_to_sample.nii.gz New_lesion_mask.nii.gz -dr 0 1 -cm red-yellow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
