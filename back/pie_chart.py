import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTableWidget, QTableWidgetItem, QWidget
from PySide6.QtCharts import QChart, QChartView, QPieSeries
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt


# Диаграмма товаров
class PieChartWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        series = QPieSeries()
        
        series.append("Товар 1", 10)
        series.append("Товар 2", 20)
        series.append("Товар 4", 30)

        chart = QChart()
        chart.addSeries(series)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignRight)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        
        self.setCentralWidget(chart_view)
        self.resize(800, 600)

# Диаграмма затрат компаний
# class PieChartWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         series = QPieSeries()
        
#         series.append("Google", 500)
#         series.append("Amazon", 200)
#         series.append("Apple", 300)

#         chart = QChart()
#         chart.addSeries(series)

#         chart.legend().setVisible(True)
#         chart.legend().setAlignment(Qt.AlignRight)

#         chart_view = QChartView(chart)
#         chart_view.setRenderHint(QPainter.Antialiasing)
        
#         table = QTableWidget()
#         table.setRowCount(3)
#         table.setColumnCount(2)
        
#         table.setHorizontalHeaderLabels(["Компания", "Затраты"])
        
#         data = {"Google": 500, "Amazon": 200, "Apple": 300}
        
#         for index, (key, value) in enumerate(data.items()):
#             print(value)
#             table.setItem(index, 0, QTableWidgetItem(key))
#             table.setItem(index, 1, QTableWidgetItem(str(value)))
        
#         total = sum(data.values())
            
#         table.setItem(index, 0, QTableWidgetItem("Общие затраты"))
#         table.setItem(index, 1, QTableWidgetItem(str(total)))
        
#         layout = QVBoxLayout()
#         # layout.addWidget(chart_view)
#         layout.addWidget(table)

#         chart.set(layout)

#         # main_widget = QWidget()
#         # main_widget.setLayout(layout)
        
#         self.setCentralWidget(chart)
#         self.resize(800, 600)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PieChartWindow()
    window.show()
    sys.exit(app.exec())