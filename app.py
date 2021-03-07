from PyQt5.QtGui import QIcon, QFont, QCursor, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QRadioButton, QLabel, QLineEdit, QPushButton, \
    QDesktopWidget, QComboBox, QFileDialog, QTextEdit
from PyQt5.QtCore import Qt
import webbrowser
from PIL import Image


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.sources = []

        self.title = 'Image Compressor v1.0.0'
        self.left = 0
        self.top = 10
        self.width = 500
        self.height = 800
        self.style = ''
        # !LOADING CUSTOM STYLESHEET
        with open("static/style.qss", "r") as stylesheet:
            self.style = stylesheet.read()
        self.setStyleSheet(self.style)

        self.setWindowIcon(QIcon("static/icon196x196.png"))
        self.setObjectName("main_window")
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.center()

        # !RADIO BOX FRAME
        self.radio_frame = QFrame(self)
        self.radio_frame.setObjectName("radio_frame")
        self.radio_frame.move(20, 20)

        single_file = QRadioButton(self.radio_frame)
        single_file.setText("Select File")
        single_file.setObjectName("single_file")
        single_file.setFont(QFont('Merienda', 14))
        single_file.setCursor(QCursor(Qt.PointingHandCursor))
        single_file.move(10, 0)
        single_file.setChecked(True)
        single_file.toggled.connect(lambda: self.display_frame(single_file))

        multi_file = QRadioButton(self.radio_frame)
        multi_file.setText("Select Directory")
        multi_file.setObjectName("multi_file")
        multi_file.setFont(QFont('Merienda', 14))
        multi_file.setCursor(QCursor(Qt.PointingHandCursor))
        multi_file.move(230, 0)
        multi_file.toggled.connect(lambda: self.display_frame(multi_file))

        # !SINGLE FILE FRAME
        self.single_file_frame = QFrame(self)
        self.single_file_frame.setObjectName("single_file_frame")
        self.single_file_frame.move(20, 70)

        img_src_lbl = QLabel(self.single_file_frame)
        img_src_lbl.setText("Choose Image:")
        img_src_lbl.setObjectName("img_src_lbl")
        img_src_lbl.setFont(QFont("Poppins", 12))
        img_src_lbl.move(10, 10)

        self.img_src = QLineEdit(self.single_file_frame)
        self.img_src.setObjectName("img_src")
        self.img_src.setFont(QFont("Poppins", 10))
        self.img_src.move(10, 50)

        open_file_src = QPushButton(self.single_file_frame)
        open_file_src.setObjectName("open_file")
        open_file_src.setIcon(QIcon("static/folder.svg"))
        open_file_src.move(410, 50)
        open_file_src.setCursor(QCursor(Qt.PointingHandCursor))
        open_file_src.clicked.connect(lambda: self.get_file_path("singleImg", self.img_src))

        img_dest_lbl = QLabel(self.single_file_frame)
        img_dest_lbl.setText("Save Image at:")
        img_dest_lbl.setObjectName("img_dest_lbl")
        img_dest_lbl.setFont(QFont("Poppins", 12))
        img_dest_lbl.move(10, 100)

        self.img_dest = QLineEdit(self.single_file_frame)
        self.img_dest.setObjectName("img_dest")
        self.img_dest.setFont(QFont("Poppins", 10))
        self.img_dest.move(10, 140)

        open_file_dest = QPushButton(self.single_file_frame)
        open_file_dest.setObjectName("open_file")
        open_file_dest.setIcon(QIcon("static/folder.svg"))
        open_file_dest.move(410, 140)
        open_file_dest.setCursor(QCursor(Qt.PointingHandCursor))
        open_file_dest.clicked.connect(lambda: self.get_file_path("destDir", self.img_dest))

        save_as_lbl = QLabel(self.single_file_frame)
        save_as_lbl.setText("Save Image as:")
        save_as_lbl.setObjectName("save_as_lbl")
        save_as_lbl.setFont(QFont("Poppins", 12))
        save_as_lbl.move(10, 180)

        self.save_as = QLineEdit(self.single_file_frame)
        self.save_as.setObjectName("save_as")
        self.save_as.setFont(QFont("Poppins", 12))
        self.save_as.move(10, 210)

        quality_lbl = QLabel(self.single_file_frame)
        quality_lbl.setText("Select Image Quality:")
        quality_lbl.setFont(QFont("Poppins", 12))
        quality_lbl.setObjectName("quality_lbl")
        quality_lbl.move(10, 260)

        self.quality = QComboBox(self.single_file_frame)
        self.quality.setFont(QFont("Poppins", 12))
        self.quality.addItem("High")
        self.quality.addItem("Medium")
        self.quality.addItem("Low")
        self.quality.setObjectName("quality")
        self.quality.move(240, 260)

        compress = QPushButton(self.single_file_frame)
        compress.setFont(QFont("Poppins", 12))
        compress.setText("Compress")
        compress.setObjectName("compress")
        compress.move(25, 320)
        compress.setCursor(QCursor(Qt.PointingHandCursor))
        compress.clicked.connect(lambda: self.single_compress(self.img_src.text(), self.img_dest.text(),
                                                              self.save_as.text(), self.quality.currentText()))

        # !ALERT ERROR FRAME
        self.alert_frame = QFrame(self)
        self.alert_frame.setObjectName("alert_frame")
        self.alert_frame.move(20, 50)
        self.alert_frame.setVisible(False)

        # *ALERT LABEL
        self.alert_info = QLabel(self.alert_frame)
        self.alert_info.setText("Image Not Found!")
        self.alert_info.setFont(QFont("Poppins", 12))
        self.alert_info.move(60, 5)
        self.alert_info.setObjectName("alert_info")
        warning = QLabel(self.alert_frame)
        warning.setPixmap(QPixmap("static/warning.svg"))
        warning.move(15, 5)

        self.single_file_frame.setVisible(True)

        # !DIRECTORY FRAME
        self.dir_frame = QFrame(self)
        self.dir_frame.setObjectName("dir_frame")
        self.dir_frame.move(20, 70)

        dir_src_lbl = QLabel(self.dir_frame)
        dir_src_lbl.setText("Choose Image Directory:")
        dir_src_lbl.setObjectName("img_src_lbl")
        dir_src_lbl.setFont(QFont("Poppins", 12))
        dir_src_lbl.move(10, 10)

        self.dir_src = QLineEdit(self.dir_frame)
        self.dir_src.setObjectName("img_src")
        self.dir_src.setFont(QFont("Poppins", 10))
        self.dir_src.move(10, 50)

        open_file_src = QPushButton(self.dir_frame)
        open_file_src.setObjectName("open_file")
        open_file_src.setIcon(QIcon("static/folder.svg"))
        open_file_src.move(410, 50)
        open_file_src.setCursor(QCursor(Qt.PointingHandCursor))
        open_file_src.clicked.connect(lambda: self.get_file_path("srcDir", self.dir_src))

        img_dest_lbl = QLabel(self.dir_frame)
        img_dest_lbl.setText("Save Images at:")
        img_dest_lbl.setObjectName("img_dest_lbl")
        img_dest_lbl.setFont(QFont("Poppins", 12))
        img_dest_lbl.move(10, 100)

        self.dir_dest = QLineEdit(self.dir_frame)
        self.dir_dest.setObjectName("img_dest")
        self.dir_dest.setFont(QFont("Poppins", 10))
        self.dir_dest.move(10, 140)

        open_file_dest = QPushButton(self.dir_frame)
        open_file_dest.setObjectName("open_file")
        open_file_dest.setIcon(QIcon("static/folder.svg"))
        open_file_dest.move(410, 140)
        open_file_dest.setCursor(QCursor(Qt.PointingHandCursor))
        open_file_dest.clicked.connect(lambda: self.get_file_path("destDir", self.dir_dest))

        suffix_as_lbl = QLabel(self.dir_frame)
        suffix_as_lbl.setText("Suffix image name as:")
        suffix_as_lbl.setObjectName("save_as_lbl")
        suffix_as_lbl.setFont(QFont("Poppins", 12))
        suffix_as_lbl.move(10, 180)

        self.suffix_as = QLineEdit(self.dir_frame)
        self.suffix_as.setObjectName("save_as")
        self.suffix_as.setFont(QFont("Poppins", 12))
        self.suffix_as.move(10, 210)

        quality_lbl = QLabel(self.dir_frame)
        quality_lbl.setText("Select Image Quality:")
        quality_lbl.setFont(QFont("Poppins", 12))
        quality_lbl.setObjectName("quality_lbl")
        quality_lbl.move(10, 260)

        self.quality_dir = QComboBox(self.dir_frame)
        self.quality_dir.setFont(QFont("Poppins", 12))
        self.quality_dir.addItem("High")
        self.quality_dir.addItem("Medium")
        self.quality_dir.addItem("Low")
        self.quality_dir.setObjectName("quality")
        self.quality_dir.move(240, 260)

        compress = QPushButton(self.dir_frame)
        compress.setFont(QFont("Poppins", 12))
        compress.setText("Compress")
        compress.setObjectName("compress")
        compress.move(25, 320)
        compress.setCursor(QCursor(Qt.PointingHandCursor))
        compress.clicked.connect(lambda: self.dir_compress(self.dir_src.text(), self.dir_dest.text(),
                                                           self.suffix_as.text(), self.quality_dir.currentText()))

        self.dir_frame.setVisible(False)

        # !STATUS FRAME
        self.status_frame = QFrame(self)
        self.status_frame.setObjectName("status_frame")
        self.status_frame.move(20, 480)

        self.status = QTextEdit(self.status_frame)
        self.status.setObjectName("status")
        self.status.setReadOnly(True)
        self.status.acceptRichText()
        self.status.move(10, 10)
        self.status.setFont(QFont("Poppins", 10))

        # ----- ATTR
        attr_frame = QFrame(self)
        attr_frame.setObjectName("attr_frame")
        attr_frame.move(20, 780)
        attr = QPushButton(attr_frame)
        attr.setObjectName("attr")
        attr.setText("Created by Darshaan Aghicha©")
        attr.move(120, 0)
        attr.setCursor(QCursor(Qt.PointingHandCursor))
        attr.clicked.connect(show_attr)

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # * FUNC TOGGLE FRAMES
    def display_frame(self, btn):
        if btn.text() == "Select File" and btn.isChecked():
            self.single_file_frame.setVisible(True)
            self.dir_frame.setVisible(False)
        elif btn.text() == "Select Directory" and btn.isChecked():
            self.single_file_frame.setVisible(False)
            self.dir_frame.setVisible(True)
        self.status.setText("")

    # *FUNC OPEN FILE DIALOG BOX
    def get_file_path(self, request, e):
        if request == "singleImg":
            file_name, _ = QFileDialog.getOpenFileName(self, "Choose an Image:", "", "Image Files(*.jpg, *.png);; All "
                                                                                     "files(*)",
                                                       options=QFileDialog.Options())
            if file_name:
                self.sources.append(file_name)
                self.save_as.setText(file_name.split('/')[-1].split('.')[0])

                e.setText(file_name)
        elif request == 'destDir':
            file_title = "Choose a directory to save image(s) into:"
            file_name = QFileDialog.getExistingDirectory(self, file_title)
            if file_name:
                self.sources.append(file_name)
                e.setText(file_name)
        elif request == 'srcDir':
            file_title = "Choose directory that contains image:"
            file_name = QFileDialog.getExistingDirectory(self, file_title)
            if file_name:
                self.sources.append(file_name)
                e.setText(file_name)

    # *FUNC DIR IMG(S) COMPRESS
    def dir_compress(self, src, dest, suffix, quality):
        import os
        if src == "" or dest == "":
            self.status.append("<p style='color:rgb(255,0,0)'>Please provide the necessary info!</p>")
        else:
            self.status.append(f"Fetching images from {src}")
            temp = os.listdir(src)
            files = []
            for file in temp:
                if file.endswith(".png") or file.endswith(".jpg") or file.endswith("jpeg"):
                    img = file.split(".")
                    files.append(img)
            if len(files) == 0:
                self.status.append("<p style='color:rgb(255,0,0)'>Unable to find any Image file in the given "
                                   "directory!</p>")
            for images in files:
                r_src = src + "\\" + (".".join(images))
                if suffix == '':
                    r_dest = dest + "/" + images[0] + "_compressed." + images[1]
                else:
                    r_dest = dest + "/" + images[0] + suffix + "." + images[1]
                try:
                    print(r_src, quality, r_dest)
                    self.compressing(r_src, quality, r_dest)
                except Exception as err:
                    self.status.append(f"<p style='color:rgb(255,0,0)'>Could not complete the task! {err}</p>")

        # !CLEARING ALL the FIELDS
        self.dir_src.setText("")
        self.dir_dest.setText("")
        self.suffix_as.setText("")

    # *FUNC SINGLE IMG COMPRESS
    def single_compress(self, src, dest, save, quality):
        if src == "" or dest == "" or save == "":
            self.status.append("<p style='color:rgb(255,0,0)'>Please provide the necessary info!</p>")
        else:
            self.status.append(f"Fetching image from: <br>{src}")
            try:
                extension = src.split(".")[1]
                dest += '/' + save + '.' + extension
                self.compressing(src, quality, dest)
            except Exception as err:
                self.status.append(f"<p style='color:rgb(255,0,0)'>Could not complete the task! {err}</p>")

        # !CLEARING ALL the FIELDS
        self.img_src.setText("")
        self.img_dest.setText("")
        self.save_as.setText("")

    def compressing(self, src, quality, dest):
        width = 0
        img = Image.open(src)
        original_width = img.width
        if quality == "High":
            width = original_width
            self.status.append("<p style='color: #FFF'>Processing High Quality Image...</p>")
        if quality == "Medium":
            width = int(original_width / 2)
            self.status.append("<p style='color: #FFF'>Processing Medium Quality Image...</p>")
        elif quality == "Low":
            width = int(original_width / 4)
            self.status.append("<p style='color: #FFF'>Processing Low Quality Image...</p>")
        self.status.append(f"<p style='color:rgb(255,255,0)'>Compressing<br>{dest}</p>")
        w_percent = (width / float(img.size[0]))
        h_percent = int(float(img.size[1]) * float(w_percent))
        img = img.resize((width, h_percent), Image.ANTIALIAS)
        img.save(dest)
        self.status.append(f"<p style='color:rgb(0,255,0)'>File compressed and saved as<br>{dest}</p>")


def show_attr():
    webbrowser.open("https://github.com/DSAghicha", new=2)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
