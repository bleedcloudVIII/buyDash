from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCharts import QChart, QChartView, QBarSet, QStackedBarSeries, QBarCategoryAxis
from PySide6.QtGui import QPainter


class BarChartWindow(QMainWindow):
    def __init__(self, data, title="Столбчатая диаграмма"):
        super().__init__()
        self.setWindowTitle(title)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Получаем все уникальные продукты
        products = set()
        for company_data in data.values():
            products.update(company_data.keys())
        products = sorted(products)

        series = QStackedBarSeries()

        for product in products:
            bar_set = QBarSet(product)
            for company in data:
                bar_set.append(data[company].get(product, 0))
            series.append(bar_set)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(title)
        chart.legend().setVisible(True)

        axis = QBarCategoryAxis()
        axis.append(list(data.keys()))
        chart.createDefaultAxes()
        chart.setAxisX(axis, series)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        layout.addWidget(chart_view)

        self.resize(800, 600)