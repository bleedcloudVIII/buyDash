from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QLabel, QScrollArea, QGroupBox,
    QFileDialog, QDialog, QComboBox, QSizePolicy
)
from PySide6.QtCharts import QChart, QChartView, QPieSeries, QBarSet, QStackedBarSeries, QBarCategoryAxis
from PySide6.QtGui import QPainter

from back.file_worker import FileWorker


class MonthDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выберите месяц")
        self.setFixedSize(300, 150)
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                font-family: Arial;
                font-size: 16px;
            }
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #333333;
            }
            QComboBox {
                background-color: white;
                border: 2px solid #cccccc;
                border-radius: 5px;
                padding: 8px;
                font-size: 16px;
                color: #333333;
            }
            QComboBox:hover {
                border-color: #999999;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border-left: 1px solid #cccccc;
                background-color: #e0e0e0;
                border-radius: 0 5px 5px 0;
            }
            QComboBox::down-arrow {
                width: 16px;
                height: 16px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                selection-background-color: #e0e0e0;
                font-size: 16px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        layout = QVBoxLayout(self)
        self.month_combo = QComboBox()
        self.month_combo.addItems([
            "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
            "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
        ])
        layout.addWidget(self.month_combo)

        self.ok_button = QPushButton("ОК")
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)

    def get_selected_month(self):
        return self.month_combo.currentIndex() + 1


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.expenses_pie_view = None
        self.companies_scroll = None
        self.buttons = None
        self.side_panel_layout = None
        self.side_panel = None
        self.companies_group = None
        self.setWindowTitle("BuyDash Analytics")
        self.showFullScreen()

        # Основные переменные
        self.file_path = None
        self.selected_month = None
        self.selected_company = None
        self.file_worker = None
        self.company_pages = {}  # Словарь для хранения страниц компаний

        # главный виджет и layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QHBoxLayout(central_widget)

        # боковая панель
        self.create_side_panel()

        # основная область с вкладками
        self.create_main_area()

    def create_side_panel(self):
        """Создает боковую панель с кнопками"""
        self.side_panel = QWidget()
        self.side_panel.setStyleSheet("background-color: PaleGreen;")
        self.side_panel_layout = QVBoxLayout(self.side_panel)
        self.side_panel.setFixedWidth(250)
        self.main_layout.addWidget(self.side_panel)

        # Название приложения
        app_name_label = QLabel("BuyDash")
        app_name_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 45px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        app_name_label.setAlignment(Qt.AlignCenter)
        app_name_label.setFixedHeight(80)
        self.side_panel_layout.addWidget(app_name_label)

        # Кнопки действий
        self.buttons = []
        button_texts = ["Открыть файл", "Выбрать месяц", "Главная"]
        for text in button_texts:
            button = QPushButton(text)
            button.setStyleSheet("""
                QPushButton {
                    background-color: lightgreen;
                    color: white;
                    font-size: 18px;
                    padding: 20px;
                    font-weight: bold;
                    border: none;
                    text-align: center;
                    border: 2px solid white;
                }
                QPushButton:hover {
                    background-color: darkgreen;
                }
            """)
            self.buttons.append(button)
            self.side_panel_layout.addWidget(button)

        # Группа компаний
        self.companies_group = QGroupBox("Компании")
        self.companies_group.setStyleSheet("""
            QGroupBox {
                color: white;
                font-size: 18px;
                font-weight: bold;
                border: 2px solid white;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
        """)

        self.companies_scroll = QScrollArea()
        self.companies_scroll.setWidgetResizable(True)
        self.companies_container = QWidget()
        self.companies_layout = QVBoxLayout(self.companies_container)
        self.companies_scroll.setWidget(self.companies_container)

        self.companies_group_layout = QVBoxLayout(self.companies_group)
        self.companies_group_layout.addWidget(self.companies_scroll)
        self.side_panel_layout.addWidget(self.companies_group)

        # Кнопка выхода
        exit_button = QPushButton("×")
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: gray;
                font-size: 20px;
                font-weight: bold;
                border-radius: 15px;
                padding: 5px 10px;
                border: 2px solid gray;
            }
            QPushButton:hover {
                background-color: darkgray;
            }
        """)
        exit_button.setFixedSize(30, 30)
        exit_button.clicked.connect(self.close)

        exit_container = QWidget()
        exit_layout = QHBoxLayout(exit_container)
        exit_layout.addStretch()
        exit_layout.addWidget(exit_button)
        exit_layout.setContentsMargins(0, 0, 10, 0)
        self.main_layout.addWidget(exit_container, alignment=Qt.AlignTop | Qt.AlignRight)

        # Подключаем кнопки
        self.buttons[0].clicked.connect(self.open_file_dialog)
        self.buttons[1].clicked.connect(self.select_month)
        self.buttons[2].clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))

    def create_main_area(self):
        """Создает основную область с вкладками"""
        self.stacked_widget = QStackedWidget()

        # Вкладка 1: Открыть файл (пустая)
        tab1 = QWidget()
        tab1_layout = QVBoxLayout(tab1)
        tab1_layout.addWidget(QLabel("Используйте кнопку 'Открыть файл' для загрузки данных"))
        self.stacked_widget.addWidget(tab1)

        # Вкладка 2: Выбрать месяц (пустая)
        tab2 = QWidget()
        tab2_layout = QVBoxLayout(tab2)
        tab2_layout.addWidget(QLabel("Выберите месяц для анализа данных"))
        self.stacked_widget.addWidget(tab2)

        # Вкладка 3: Главная (с диаграммами)
        self.main_tab = QWidget()
        self.main_tab_layout = QVBoxLayout(self.main_tab)

        # виджеты для диаграмм на главной вкладке
        self.create_main_tab_charts()

        self.stacked_widget.addWidget(self.main_tab)

        # Добавляем в главный layout
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.stacked_widget)
        self.main_layout.addWidget(scroll)

    def create_main_tab_charts(self):
        """Создает диаграммы для главной вкладки"""
        self.bar_chart_view = QChartView()
        self.bar_chart_view.setRenderHint(QPainter.Antialiasing)
        self.bar_chart_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Круговая диаграмма затрат по компаниям
        self.expenses_pie_view = QChartView()
        self.expenses_pie_view.setRenderHint(QPainter.Antialiasing)
        self.expenses_pie_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Добавляем на главную вкладку
        self.main_tab_layout.addWidget(QLabel("Столбчатая диаграмма по всем компаниям и товарам:"))
        self.main_tab_layout.addWidget(self.bar_chart_view)
        self.main_tab_layout.addWidget(QLabel("Круговая диаграмма затрат по компаниям:"))
        self.main_tab_layout.addWidget(self.expenses_pie_view)

    def create_company_page(self, company_name):
        """Создает страницу для конкретной компании с круговой диаграммой"""
        page = QWidget()
        layout = QVBoxLayout(page)

        # Круговая диаграмма для компании
        chart_view = QChartView()
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout.addWidget(chart_view)

        # Сохраняем ссылку на chart_view для обновления
        self.company_pages[company_name] = {
            'page': page,
            'chart_view': chart_view,
            'index': self.stacked_widget.count()  # Сохраняем индекс страницы
        }

        self.stacked_widget.addWidget(page)

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл Excel", "", "Excel Files (*.xlsx *.xls)"
        )

        if file_path and file_path.endswith(('.xlsx', '.xls')):
            self.file_path = file_path
            try:
                self.file_worker = FileWorker(file_path)
                self.file_worker.file_read()
                print("Файл успешно загружен")
                self.create_company_pages()
                self.stacked_widget.setCurrentIndex(2)  # Переключаем на главную вкладку
            except Exception as e:
                print(f"Ошибка загрузки файла: {e}")

    def create_company_pages(self):
        """Создает страницы и кнопки для всех компаний"""
        for i in reversed(range(self.companies_layout.count())):
            widget = self.companies_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for company in list(self.company_pages.keys()):
            page_info = self.company_pages[company]
            self.stacked_widget.removeWidget(page_info['page'])
            page_info['page'].deleteLater()
            del self.company_pages[company]

        # Создаем новые страницы и кнопки
        companies = self.file_worker.get_company()
        for company in companies:
            # Создаем страницу компании
            self.create_company_page(company)

            # Создаем кнопку компании
            btn = QPushButton(company)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: lightgreen;
                    color: white;
                    font-size: 18px;
                    padding: 15px;
                    font-weight: bold;
                    border: none;
                    text-align: center;
                    border: 2px solid white;
                }
                QPushButton:hover {
                    background-color: darkgreen;
                }
            """)
            btn.clicked.connect(lambda checked, c=company: self.show_company_page(c))
            self.companies_layout.addWidget(btn)

    def show_company_page(self, company_name):
        """Показывает страницу с диаграммой для выбранной компании"""
        if company_name in self.company_pages:
            self.selected_company = company_name
            page_info = self.company_pages[company_name]
            self.stacked_widget.setCurrentIndex(page_info['index'])

            # Обновляем диаграмму компании, если выбран месяц
            if self.selected_month:
                self.update_company_chart(company_name)

    def select_month(self):
        """Открывает диалог выбора месяца"""
        if not self.file_worker:
            print("Сначала загрузите файл")
            return

        dialog = MonthDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.selected_month = dialog.get_selected_month()
            print(f"Выбран месяц: {self.selected_month}")
            self.update_all_charts()

    def update_all_charts(self):
        """Обновляет все диаграммы (главные и компаний)"""
        if not self.file_worker or not self.selected_month:
            return

        # Обновляем главные диаграммы
        self.update_main_charts()

        # Обновляем диаграммы компаний
        if self.selected_company:
            self.update_company_chart(self.selected_company)

    def update_main_charts(self):
        """Обновляет диаграммы на главной вкладке"""
        bar_data = self.file_worker.get_products_by_companies(self.selected_month)
        self.update_bar_chart(bar_data)

        expenses_data = self.file_worker.get_expenses_by_companies(self.selected_month)
        self.update_expenses_pie_chart(expenses_data)

    def update_company_chart(self, company_name):
        products_data = self.file_worker.get_company_products(company_name, self.selected_month)

        series = QPieSeries()
        for product, count in products_data.items():
            series.append(f"{product} ({count})", count)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(f"Товары компании {company_name}")
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignRight)

        self.company_pages[company_name]['chart_view'].setChart(chart)

    def update_bar_chart(self, products_data):
        """Обновляет столбчатую диаграмму"""
        all_products = set()
        for company_data in products_data.values():
            all_products.update(company_data.keys())
        all_products = sorted(all_products)

        series = QStackedBarSeries()

        for product in all_products:
            bar_set = QBarSet(product)
            for company in products_data:
                bar_set.append(products_data[company].get(product, 0))
            series.append(bar_set)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Продажи товаров по компаниям")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        axis = QBarCategoryAxis()
        axis.append(list(products_data.keys()))
        chart.createDefaultAxes()
        chart.setAxisX(axis, series)

        self.bar_chart_view.setChart(chart)

    def update_expenses_pie_chart(self, expenses_data):
        """Обновляет круговую диаграмму затрат по компаниям"""
        if not expenses_data:
            print("Нет данных для круговой диаграммы затрат")
            return

        series = QPieSeries()
        for company, amount in expenses_data.items():
            # Добавляем сектор с названием компании и суммой
            slice_ = series.append(f"{company} ({amount})", amount)
            # Можно настроить внешний вид секторов
            slice_.setLabelVisible(True)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Затраты по компаниям")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignRight)

        self.expenses_pie_view.setChart(chart)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
