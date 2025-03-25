from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem
from PySide6.QtCharts import QChart, QChartView, QPieSeries
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt


class PieChartWindow(QMainWindow):
    def __init__(self, data, title="Диаграмма"):
        super().__init__()
        self.setWindowTitle(title)

        series = QPieSeries()
        for name, value in data.items():
            series.append(name, value)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(title)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignRight)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(chart_view)
        self.resize(800, 600)