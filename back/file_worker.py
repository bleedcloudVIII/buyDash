import pandas as pd


class RowData:
    def __init__(self, seller, date, product, qty, count, unit, all, remark):
        self.seller = seller
        self.date = date
        self.product = product
        self.qty = qty
        self.count = count
        self.unit = unit
        self.all = all
        self.remark = remark


class FileWorker:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = {}
        self.company_names = []

    def file_read(self):
        try:
            all_lists = pd.read_excel(self.file_path, sheet_name=None)

            for sheet_name, list_file in all_lists.items():
                index_row = 3
                monthly_data = []
                for count in range(len(list_file) - 3):
                    row_data = list_file.iloc[index_row]
                    index_row += 1
                    monthly_data.append(RowData(
                        row_data.iloc[0], row_data.iloc[1], row_data.iloc[2], row_data.iloc[3],
                        row_data.iloc[4], row_data.iloc[5], row_data.iloc[6], row_data.iloc[7]
                    ))

                self.data[sheet_name] = monthly_data
                name_comp = sheet_name.split('_')
                if name_comp and name_comp[0] not in self.company_names:
                    self.company_names.append(name_comp[0])

        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            raise

    def view_data(self):
        for company, rows in self.data.items():
            print(f"\nСтраница {company}:")
            for row in rows:
                data = vars(row)
                for key, value in data.items():
                    print(f"{key}: {value}")

    def get_company(self):
        return self.company_names

    def table_for(self, first_month, last_month, table, company):
        count_month = first_month
        while count_month <= last_month:
            for company_month, rows in self.data.items():
                name_company = company_month.split('_')
                if len(name_company) >= 2:  # Проверяем, что есть и компания, и месяц
                    if name_company[0] == company and int(name_company[1]) == count_month:
                        for row in rows:
                            if table:
                                is_has_same = any(
                                    d["seller"] == row.seller and
                                    d["product"] == row.product and
                                    d["qty"] == row.qty
                                    for d in table
                                )
                                if is_has_same:
                                    for d in table:
                                        if (d["seller"] == row.seller and
                                                d["product"] == row.product and
                                                d["qty"] == row.qty):
                                            d["count"] += row.count
                                            d["all"] += row.all
                                else:
                                    row_for_res = vars(row).copy()
                                    del row_for_res["remark"]
                                    del row_for_res["date"]
                                    table.append(row_for_res)
                            else:
                                row_for_res = vars(row).copy()
                                del row_for_res["remark"]
                                del row_for_res["date"]
                                table.append(row_for_res)
                        count_month += 1
        return table

    def table_for_companies(self, first_month, last_month):
        result_table = []
        for company in self.company_names:
            result_table = self.table_for(first_month, last_month, result_table, company)
        return result_table


    def piechart_one_company(self, first_month, last_month, company):
        result = {}
        count_month = first_month

        while count_month <= last_month:
            for company_month, rows in self.data.items():
                name_company = company_month.split('_')
                if len(name_company) >= 2 and name_company[0] == company and int(name_company[1]) == count_month:
                    for row in rows:
                        if row.product in result:
                            result[row.product] += int(row.count)
                        else:
                            result[row.product] = int(row.count)
                    count_month += 1
        return result

    def piechart_expense(self, first_month, last_month):
        result = {}
        for company in self.company_names:
            count_month = first_month
            total = 0
            while count_month <= last_month:
                for company_month, rows in self.data.items():
                    name_company = company_month.split('_')
                    if len(name_company) >= 2 and name_company[0] == company and int(name_company[1]) == count_month:
                        for row in rows:
                            total += int(row.all)
                        count_month += 1
            if total > 0:
                result[company] = total
        return result

    def bar_chart_data(self, first_month, last_month):
        result = {}
        for company in self.company_names:
            count_month = first_month
            company_data = {}
            while count_month <= last_month:
                for company_month, rows in self.data.items():
                    name_company = company_month.split('_')
                    if len(name_company) >= 2 and name_company[0] == company and int(name_company[1]) == count_month:
                        for row in rows:
                            if row.product in company_data:
                                company_data[row.product] += int(row.count)
                            else:
                                company_data[row.product] = int(row.count)
                        count_month += 1
            if company_data:
                result[company] = company_data
        return result

    def get_company_products(self, company, month):
        result = {}
        for company_month, rows in self.data.items():
            name_parts = company_month.split('_')
            if len(name_parts) >= 2 and name_parts[0] == company and int(name_parts[1]) == month:
                for row in rows:
                    if row.product in result:
                        result[row.product] += int(row.count)
                    else:
                        result[row.product] = int(row.count)
        return result

    def get_company_expenses(self, company, month):
        total = 0
        for company_month, rows in self.data.items():
            name_parts = company_month.split('_')
            if len(name_parts) >= 2 and name_parts[0] == company and int(name_parts[1]) == month:
                for row in rows:
                    total += int(row.all)
        return total

    def get_all_companies_data(self, month):
        result = {
            'products': {},  # {company: {product: count}}
            'expenses': {},  # {company: total_expense}
            'sales': {}  # {company: total_sales}
        }

        for company_month, rows in self.data.items():
            name_parts = company_month.split('_')
            if len(name_parts) >= 2 and int(name_parts[1]) == month:
                company = name_parts[0]

                # Инициализируем структуры данных для компании
                if company not in result['products']:
                    result['products'][company] = {}
                    result['expenses'][company] = 0
                    result['sales'][company] = 0

                for row in rows:
                    # Данные по продуктам
                    if row.product in result['products'][company]:
                        result['products'][company][row.product] += int(row.count)
                    else:
                        result['products'][company][row.product] = int(row.count)

                    # Общие расходы
                    result['expenses'][company] += int(row.all)

                    # Общие продажи (можно использовать count или другую метрику)
                    result['sales'][company] += int(row.count)

        return result

    def get_products_by_companies(self, month):
        result = {}
        for company_month, rows in self.data.items():
            name_parts = company_month.split('_')
            if len(name_parts) >= 2 and int(name_parts[1]) == month:
                company = name_parts[0]
                if company not in result:
                    result[company] = {}

                for row in rows:
                    if row.product in result[company]:
                        result[company][row.product] += int(row.count)
                    else:
                        result[company][row.product] = int(row.count)
        return result

    def get_expenses_by_companies(self, month):
        result = {}
        for company_month, rows in self.data.items():
            name_parts = company_month.split('_')
            if len(name_parts) >= 2 and int(name_parts[1]) == month:
                company = name_parts[0]
                total = 0
                for row in rows:
                    total += float(row.all)
                result[company] = total
        return result
    # Удалите или закомментируйте следующие строки:
    # file_workers = FileWorker("C:/Users/Anastasia/Downloads/Telegram Desktop/Таблицы.xlsx")
    # file_workers.file_read()
    # print(file_workers.table_for_companies(1, 3))