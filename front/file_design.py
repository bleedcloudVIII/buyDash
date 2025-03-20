import json
import os
import pandas as pd
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QLabel, QScrollArea, QGroupBox, QFileDialog, QDialog, QComboBox
)
from PySide6.QtCore import Qt

from back.file_worker import FileWorker


class MonthDialog(QDialog):
    """
    Диалоговое окно для выбора месяца.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выберите месяц")
        self.setFixedSize(300, 150)
        # Устанавливаем стиль для окна
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
                    QComboBox:hover {
                        border-color: #999999;  /* Темно-серая рамка при наведении */
                    }
                    QComboBox::drop-down {
                        subcontrol-origin: padding;
                        subcontrol-position: top right;
                        width: 30px;
                        border-left: 1px solid #cccccc;
                        background-color: #e0e0e0;  /* Серый фон для стрелочки */
                        border-radius: 0 5px 5px 0;  /* Скругление справа */
                    }
                    QComboBox::down-arrow {
                        width: 16px;
                        height: 16px;
                    }
                    QComboBox QAbstractItemView {
                        background-color: white;
                        selection-background-color: #e0e0e0;  /* Цвет выделения */
                        font-size: 16px;
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

        layout = QVBoxLayout(self)

        # Выпадающий список для выбора месяца
        self.month_combo = QComboBox()
        self.month_combo.addItems([
            "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
            "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
        ])
        layout.addWidget(self.month_combo)

        # Кнопка "ОК"
        self.ok_button = QPushButton("ОК")
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)

    def get_selected_month(self):
        """
        Возвращает номер выбранного месяца (1-12).
        """
        return self.month_combo.currentIndex() + 1  # Индексация с 0, поэтому +1


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Мое приложение с боковой панелью")  # заголовок окна
        self.showFullScreen()  # окно на весь экран
        central_widget = QWidget()  # Создаем главный виджет
        self.setCentralWidget(central_widget)  # устанавливаем его в центральную область
        self.main_layout = QHBoxLayout(central_widget)  # основной горизонтальный layout

        # Создаем боковую панель (зеленую)
        self.side_panel = QWidget()
        self.side_panel.setStyleSheet("background-color: PaleGreen;")
        self.side_panel_layout = QVBoxLayout(self.side_panel)
        self.side_panel.setFixedWidth(250)  # Фиксированная ширина

        self.main_layout.addWidget(self.side_panel)

        # Добавляем название приложения в верхнюю часть боковой панели
        app_name_label = QLabel("BuyDash")
        app_name_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 45px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        app_name_label.setAlignment(Qt.AlignCenter)  # текст по центру
        app_name_label.setFixedHeight(80)  # Фиксированная высота для надписи
        self.side_panel_layout.addWidget(app_name_label)  # Добавляем название в layout

        # Кнопки для основных действий
        self.buttons = []
        button_texts = ["Открыть файл", "Выбрать месяц", "Главная"]
        for text in button_texts:
            button = QPushButton(text)  # Устанавливаем текст кнопки
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
            self.buttons.append(button)
            self.side_panel_layout.addWidget(button)

        # Группа для кнопок компаний
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

        main_scroll_area = QScrollArea()  # QScrollArea для основной области
        main_scroll_area.setWidgetResizable(True)  # Разрешаем изменение размера содержимого
        self.stacked_widget = QStackedWidget()  # виджет для отображения вкладок
        main_scroll_area.setWidget(self.stacked_widget)  # Добавляем stacked_widget в QScrollArea
        self.main_layout.addWidget(main_scroll_area)  # QScrollArea в основной layout

        # Создаем вкладки
        for i in range(len(button_texts)):
            page = QWidget()
            layout = QVBoxLayout(page)
            self.stacked_widget.addWidget(page)

        for i, button in enumerate(self.buttons):
            button.clicked.connect(lambda checked, idx=i: self.stacked_widget.setCurrentIndex(idx))

        # Создаем кнопку "Выход" с крестиком
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
        exit_button_container = QWidget()  # контейнер для кнопки "Выход" и размещаем её в верхнем правом углу
        exit_button_layout = QHBoxLayout(exit_button_container)
        exit_button_layout.addStretch()
        exit_button_layout.addWidget(exit_button)
        exit_button_layout.setContentsMargins(0, 0, 10, 0)  # Отступы для кнопки
        self.main_layout.addWidget(exit_button_container,
                              alignment=Qt.AlignTop | Qt.AlignRight)  # Добавляем контейнер с кнопкой "Выход" в главный layout

        # Подключаем обработчики для кнопок
        self.buttons[0].clicked.connect(self.open_file_dialog)  # Открыть файл
        self.buttons[1].clicked.connect(self.select_month)  # Выбрать месяц

        # Переменные для хранения данных
        self.file_path = None  # Путь к файлу Excel
        self.selected_month = None  # Выбранный месяц

    def open_file_dialog(self):
        # Открываем диалог выбора файла
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл Excel", "", "Excel Files (*.xlsx *.xls)")

        if file_path:
            # Проверяем, что файл имеет расширение .xlsx или .xls
            if file_path.endswith(('.xlsx', '.xls')):
                self.fw = FileWorker(file_path)
                self.fw.file_read()
                self.create_buttons_company()
            else:
                print("Выбранный файл не является файлом Excel.")

    def select_month(self):
        # Проверяем, что файл был выбран
        if not self.file_path:
            print("Сначала выберите файл Excel.")
            return

        # Создаем диалоговое окно для выбора месяца
        dialog = MonthDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.selected_month = dialog.get_selected_month()
            print(f"Выбран месяц: {self.selected_month}")

            # Фильтруем данные по выбранному месяцу
            self.filter_data_by_month()

    def filter_data_by_month(self):
        # Фильтрация данных по выбранному месяцу
        if not self.selected_month:
            print("Месяц не выбран.")
            return

        try:
            # Читаем файл Excel
            df = pd.read_excel(self.file_path)

            # Фильтруем данные по выбранному месяцу (вторая строка, второй столбец)
            # Предполагаем, что месяц указан во второй строке и втором столбце
            month_column = df.iloc[1, 1]  # Вторая строка, второй столбец
            filtered_data = df[df.iloc[:, 1] == self.selected_month]

            # Сохраняем отфильтрованные данные в JSON
            self.save_filtered_data_to_json(filtered_data)

        except Exception as e:
            print(f"Ошибка при фильтрации данных: {e}")

    def create_buttons_company(self):
        # Пример данных из бэкенда: список компаний
        companies = self.fw.get_company()
        companies_layout = QVBoxLayout(self.companies_group)
        companies_scroll_area = QScrollArea()
        companies_scroll_area.setWidgetResizable(True)  # Разрешаем изменение размера содержимого
        companies_container = QWidget()  # Контейнер для кнопок компаний
        companies_scroll_area.setWidget(companies_container)  # Устанавливаем контейнер в QScrollArea
        companies_container_layout = QVBoxLayout(companies_container)
        companies_layout.addWidget(companies_scroll_area)  # QScrollArea в layout группу компаний
        self.side_panel_layout.addWidget(self.companies_group)  # группа компаний на боковой панели
        self.main_layout.addWidget(self.side_panel)  # боковая панель в основной layout

        # Динамическое создание кнопок для компаний
        self.company_buttons = []
        for company in companies:
            button = QPushButton(company)
            button.setStyleSheet("""
                        QPushButton {
                            background-color: lightgreen;
                            color: white;
                            font-size: 18px;
                            padding: 15px;
                            font-weight: bold;  
                            border: none;
                            text-align: left;
                            text-align: center;
                            border: 2px solid white;  /* Серая обводка */
                        }
                        QPushButton:hover {
                            background-color: darkgreen;
                            color: white;
                        }
                    """)
            self.company_buttons.append(button)
            companies_container_layout.addWidget(button)

            # # Создаем вкладки
            for i in range(len(companies)):
                page = QWidget()
                layout = QVBoxLayout(page)
                self.stacked_widget.addWidget(page)

            for i, button in enumerate(self.buttons + self.company_buttons):
                button.clicked.connect(lambda checked, idx=i: self.stacked_widget.setCurrentIndex(idx))

    def save_filtered_data_to_json(self, data):
        # Сохраняем отфильтрованные данные в JSON файл
        json_file_path = os.path.join("..", "back", "filtered_data.json")
        try:
            # Преобразуем DataFrame в словарь и сохраняем в JSON
            data_dict = data.to_dict(orient="records")
            with open(json_file_path, "w", encoding="utf-8") as json_file:
                json.dump(data_dict, json_file, indent=4, ensure_ascii=False)
            print(f"Данные сохранены в {json_file_path}")
        except Exception as e:
            print(f"Ошибка при сохранении данных в JSON: {e}")


app = QApplication([])
window = MainWindow()
window.show()

app.exec()
