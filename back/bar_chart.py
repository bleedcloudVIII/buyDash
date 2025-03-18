import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtCharts import QChart, QChartView, QBarSet, QStackedBarSeries, QBarCategoryAxis

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # Типа данные пришли с бэка
        data = {
            "Google": {"Product1": 20, "Product2" : 2, "Product3": 1,"Product4": 6},
            "X": {"Product1": 22, "Product2": 3, "Product5": 10},
            "Amazon": {"Product1": 10, "Product4": 30, "Product3": 21},
            "Apple": {"Product1": 6, "Product2": 23, "Product5": 1},
        }

        # Тут мб будет с бека получаться список продуктов
        products = ["Product1", "Product2", "Product3", "Product4", "Product5"]
        series = QStackedBarSeries()
        
        for p in products:
            prod_series = QBarSet(p)
            
            for company_spending in data.values():
                is_append = False
                for key, value in company_spending.items():
                    if (key == p):
                        prod_series.append(value)
                        is_append = True
            
                if not is_append:
                    prod_series.append(0)

            series.append(prod_series)
        
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Столбчатая диаграмма с наложением")

        categories = ["Google", "X", "Amazon", "Apple"]
        axis = QBarCategoryAxis()
        axis.append(categories)
        chart.createDefaultAxes()
        chart.setAxisX(axis, series)

        self.chart_view = QChartView(chart)
        main_layout.addWidget(self.chart_view)
        self.resize(800, 600)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())