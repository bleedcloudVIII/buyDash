from PySide6.QtWidgets import QApplication
from front.file_design import MainWindow

app = QApplication([])
window = MainWindow()
window.show()

app.exec()