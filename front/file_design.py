import json
import os
import pandas as pd
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QStackedWidget, QLabel, QScrollArea, QGroupBox, QFileDialog, QDialog, QComboBox,
)
from PySide6.QtGui import QPainter
from PySide6.QtCharts import QChart, QChartView, QBarSet, QStackedBarSeries, QBarCategoryAxis, QPieSeries
from PySide6.QtCore import Qt

from back.file_worker import FileWorker


class MonthDialog(QDialog):
    """
    Диалоговое окно для выбора месяца.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("""
                    QDialog {
                        background-color: #f0f0f0;  /* Светло-серый фон */
                        font-family: Arial;
                        font-size: 16px;
                    }
                    QLabel {
                        font-size: 18px;
                        font-weight: bold;
                        color: #333333;  /* Темно-серый текст */
                    }
                    QComboBox {
                        background-color: white;
                        border: 2px solid #cccccc;  /* Серая рамка */
                        border-radius: 5px;
                        padding: 8px;
                        font-size: 16px;
                        color: #333333;
                    }
                    QPushButton {
                        background-color: #4CAF50;  /* Зеленый цвет */
                        color: white;
                        font-size: 16px;
                        font-weight: bold;
                        padding: 10px 20px;
                        border: none;
                        border-radius: 5px;
                    }
                    QPushButton:hover {
                        background-color: #45a049;  /* Темно-зеленый при наведении */
                    }
                """)

        self.setWindowTitle("Выбор периода")
        self.setFixedSize(450, 350)

        layout = QVBoxLayout(self)

        self.label = QLabel("Выберите промежуток времени:", self)
        layout.addWidget(self.label)

        self.first_month_combo = QComboBox(self)
        self.first_month_combo.addItems([
            "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
            "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
        ])
        layout.addWidget(QLabel("Первый месяц:"))
        layout.addWidget(self.first_month_combo)

        self.second_month_combo = QComboBox(self)
        self.second_month_combo.addItems([
            "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
            "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
        ])
        layout.addWidget(QLabel("Второй месяц:"))
        layout.addWidget(self.second_month_combo)

        ok_button = QPushButton("ОК")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

    def get_selected_month(self):
        """
        Возвращает номер выбранного месяца (1-12).
        """
        months_dict = {
            "Январь": 1, "Февраль": 2, "Март": 3, "Апрель": 4, "Май": 5, "Июнь": 6,
            "Июль": 7, "Август": 8, "Сентябрь": 9, "Октябрь": 10, "Ноябрь": 11, "Декабрь": 12
        }
        print([months_dict.get(self.first_month_combo.currentText()), months_dict.get(self.second_month_combo.currentText())])
        return [months_dict.get(self.first_month_combo.currentText()), months_dict.get(self.second_month_combo.currentText())]



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.side_panel_buttons = {
            "Открыть файл": self.open_file_dialog,
            "Выбрать месяц": self.select_month,
            "Главная": None
        }

        self.fw = None

        self.setWindowTitle("Мое приложение с боковой панелью")
        self.showFullScreen()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QHBoxLayout(central_widget)
        self.stacked_widget = QStackedWidget()
        
        # Для кнопки "Главная"
        page = QWidget()  
        self.general_layout = QVBoxLayout(page)
        self.create_general_page(self.general_layout)
        self.stacked_widget.addWidget(page)
        func = lambda checked, idx=0: self.stacked_widget.setCurrentIndex(idx)
        self.side_panel_buttons["Главная"] = func

        self.create_side_panel()
        self.create_exit_button()
        
        
    def create_exit_button(self):
        exit_button = QPushButton("×")
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: gray;
                font-size: 20px;
                font-weight: bold;
                border-radius: 15px;
                padding: 5px 10px;
                border: 2px solid gray;  /* Серая обводка */
            }
            QPushButton:hover {
                background-color: darkgray;
                border: 2px solid gray;  /* Темно-серая обводка при наведении */
            }
        """)
        exit_button.setFixedSize(30, 30)
        exit_button.clicked.connect(self.close)
        exit_button_container = QWidget()
        exit_button_layout = QHBoxLayout(exit_button_container)
        exit_button_layout.addStretch()
        exit_button_layout.addWidget(exit_button)
        exit_button_layout.setContentsMargins(0, 0, 10, 0)
        self.main_layout.addWidget(exit_button_container, alignment=Qt.AlignTop | Qt.AlignRight)
        
    def create_button_side_panel(self, layout, text, func):
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
                    border: 2px solid white;  /* Серая обводка */
                }
                QPushButton:hover {
                    background-color: darkgreen;
                    color: white;
                }
            """)
        
        button.clicked.connect(func)
            
        layout.addWidget(button)
        
    def create_side_panel(self):
        self.side_panel = QWidget()
        self.side_panel.setStyleSheet("background-color: PaleGreen;")
        self.side_panel_layout = QVBoxLayout(self.side_panel)
        self.side_panel.setFixedWidth(250)

        self.main_layout.addWidget(self.side_panel)

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
        
        for key, value in self.side_panel_buttons.items():
            self.create_button_side_panel(self.side_panel_layout, key, value)
            
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

        main_scroll_area = QScrollArea()
        main_scroll_area.setWidgetResizable(True)
        
        main_scroll_area.setWidget(self.stacked_widget)
        self.main_layout.addWidget(main_scroll_area)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл Excel", "", "Excel Files (*.xlsx *.xls)")

        if file_path:
            if file_path.endswith(('.xlsx', '.xls')):
                self.fw = FileWorker(file_path)
                self.fw.file_read()
                self.create_buttons_company()
            else:
                print("Выбранный файл не является файлом Excel.")

    def select_month(self):
        dialog = MonthDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.selected_month = dialog.get_selected_month()
            # print(f"Выбран месяц: {self.selected_month}")

    def create_bar_chart_general(self, layout, start_month, end_month):
        data = self.fw.bar_chart(1, 12)
        # TODO ....
        products = ["Товар1", "Товар2"]
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

        chart_view = QChartView(chart)
        
        categories = self.fw.get_company()
        axis = QBarCategoryAxis()
        axis.append(categories)
        chart.createDefaultAxes()
        chart.setAxisX(axis, series)
        
        layout.addWidget(chart_view)
        
    def create_pie_chart_general(self, layout, start_month, end_month):
        series = QPieSeries()
        
        data = self.fw.piechart_expense(1, 12)
        
        for key, value in data.items():
            slice = series.append(key, value)
            slice.setLabelVisible(True)
            slice.setLabel(f"{key} - {value}")

        bar_chart = QChart()
        bar_chart.addSeries(series)

        bar_chart.legend().setVisible(True)
        bar_chart.legend().setAlignment(Qt.AlignRight)

        bar_chart_view = QChartView(bar_chart)
        bar_chart_view.setRenderHint(QPainter.Antialiasing)

        layout.addWidget(bar_chart_view)
        
    def create_table_general(self, layout, start_month, end_month):
        
        table = QTableWidget()
        
        table.setColumnCount(5)
        
        table.setHorizontalHeaderLabels(["Продавец", "Товар", "Количество", "Цена за единицу товара", "Общая стоимость"])
        
        data = self.fw.table_for_companies(start_month, end_month)
        
        table.setRowCount(len(data))
        
        table.setColumnWidth(0, 150)
        table.setColumnWidth(1, 150)
        table.setColumnWidth(2, 100)
        table.setColumnWidth(3, 200)
        table.setColumnWidth(4, 150)
        
        for index, row in enumerate(data):
            table.setItem(index, 0, QTableWidgetItem(str(row['seller'])))
            table.setItem(index, 1, QTableWidgetItem(str(row['product'])))
            table.setItem(index, 2, QTableWidgetItem(str(row['count'])))
            table.setItem(index, 3, QTableWidgetItem(str(row['qty'])))
            table.setItem(index, 4, QTableWidgetItem(str(row['all'])))
            
        layout.addWidget(table)

    def create_general_page(self, layout):
        self.clear_layout(layout)
        if self.fw is None:
            label = QLabel(f"Выберите файл")
            layout.addWidget(label)
            return
        
        hbox_widget = QWidget()
        hbox_layout = QHBoxLayout(hbox_widget)

        self.create_bar_chart_general(hbox_layout, 1, 12)
        self.create_pie_chart_general(hbox_layout, 1, 12)
        
        layout.addWidget(hbox_widget)
        
        self.create_table_general(layout, 1, 12)
        
    def create_company_page(self, layout, company, index):
        self.clear_layout(layout)
        label = QLabel(f"Информация о компании {company} - {index}")
        layout.addWidget(label)

    def create_buttons_company(self):
        companies = self.fw.get_company()
        companies_layout = QVBoxLayout(self.companies_group)
        companies_scroll_area = QScrollArea()
        companies_scroll_area.setWidgetResizable(True)
        companies_container = QWidget()
        companies_scroll_area.setWidget(companies_container)
        companies_container_layout = QVBoxLayout(companies_container)
        companies_layout.addWidget(companies_scroll_area)
        self.side_panel_layout.addWidget(self.companies_group)

        for index, company in enumerate(companies):
            page = QWidget()  
            layout = QVBoxLayout(page)
            self.create_company_page(layout, company, index)
            self.stacked_widget.addWidget(page)
            func = lambda checked, idx=index+1: self.stacked_widget.setCurrentIndex(idx)
            self.create_button_side_panel(companies_container_layout, company, func)
        
        self.create_general_page(self.general_layout)
