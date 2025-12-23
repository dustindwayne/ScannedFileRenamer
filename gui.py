import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton,
    QTextEdit, QFileDialog, QInputDialog, QLineEdit
)
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from pdf_processor import process_pdf, scan_directory


class WorkerSignals(QObject):
    log = pyqtSignal(str)
    verify_address = pyqtSignal(str)


class DirectoryWorker(QThread):
    def __init__(self, directory):
        super().__init__()
        self.directory = directory
        self.signals = WorkerSignals()
        self._pending_address = None

    def run(self):
        for message in scan_directory(self.directory, self.address_callback):
            self.signals.log.emit(message)

    def address_callback(self, address):
        self.signals.verify_address.emit(address)
        while self._pending_address is None:
            self.msleep(50)
        confirmed = self._pending_address
        self._pending_address = None
        return confirmed


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ScannedFileRenamer")
        self.resize(700, 450)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        buttons = QHBoxLayout()
        self.file_btn = QPushButton("Process Single PDF")
        self.dir_btn = QPushButton("Watch Directory")
        buttons.addWidget(self.file_btn)
        buttons.addWidget(self.dir_btn)

        self.console = QTextEdit()
        self.console.setReadOnly(True)

        layout.addLayout(buttons)
        layout.addWidget(self.console)

        self.file_btn.clicked.connect(self.process_file)
        self.dir_btn.clicked.connect(self.watch_directory)

        self.worker = None

    def process_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select PDF", "", "PDF Files (*.pdf)"
        )
        if path:
            result = process_pdf(path, self.verify_address_dialog)
            self.console.append(result)

    def watch_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Scan Folder")
        if directory:
            self.worker = DirectoryWorker(directory)
            self.worker.signals.log.connect(self.console.append)
            self.worker.signals.verify_address.connect(self.verify_address_dialog_async)
            self.worker.start()

    def verify_address_dialog(self, address):
        new, ok = QInputDialog.getText(
            self, "Verify Address",
            "Confirm or correct assigned address:",
            QLineEdit.Normal, address
        )
        return new if ok else address

    def verify_address_dialog_async(self, address):
        new, ok = QInputDialog.getText(
            self, "Verify Address",
            "Confirm or correct assigned address:",
            QLineEdit.Normal, address
        )
        self.worker._pending_address = new if ok else address


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
