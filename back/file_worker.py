import pandas as pd

class RowData:

    def __init__(self, seller,date,product,qty,count,unit,all,remark):
        self.seller=seller
        self.date=date
        self.product=product
        self.qty=qty
        self.count=count
        self.unit=unit
        self.all=all
        self.remark=remark


class FileWorker:

    def __init__(self,file_path):
        self.file_path=file_path
        self.data={}
        self.company_names=[]  

    def file_read(self):
        all_lists=pd.read_excel(self.file_path,sheet_name=None)
        
        for sheet_name, list_file in all_lists.items():
            index_row=3
            monthly_data=[]
            for count in range(len(list_file)-3):
                row_data=list_file.loc[index_row]
                index_row+=1
                monthly_data.append(RowData(row_data[0],row_data[1],row_data[2],row_data[3],
                row_data[4],row_data[5],row_data[6],row_data[7]))
     
            self.data[sheet_name] = monthly_data
            name_comp=sheet_name.split('_')
            if name_comp[0] not in self.company_names:
                self.company_names.append(name_comp[0])           
    

    def view_data(self):
        for company, rows in self.data.items():
            print()
            print(f"Страница {company}:")
            print()
            for row in rows:
                data = vars(row)
                for key, value in data.items():
                    print(f"{key}: {value}")

    def view_company(self):
        for name in self.company_names:
            print(name)

    def get_company(self):
        return self.company_names
    
    # Мб не понадобится
    def get_month(self):
        data = {}
        for company_month, rows in self.data.items():
            list_data = company_month.split('_')
            try:
                data[list_data[0]].append(list_data[1])
            except:
                data[list_data[0]] = []
                data[list_data[0]].append(list_data[1])
        
        for key, value in data.items():
            min_month = min(value)
            max_month = max(value)
            data[key] = [min_month, max_month]
        return data

    def piechart_one_company(self,first_month,last_month,kompany):
        count_month = first_month
        if first_month>last_month:
            count_month=last_month
            last_month=first_month
        result_products = {}
        for company, rows in self.data.items():
            name_company = company.split('_')
            if count_month<=last_month:
                if name_company[0]==kompany and int(name_company[1])==count_month:
     
                    for row in rows:
                        if row.product in result_products:
                            result_products[row.product]+=int(row.count)
                        else:
                            result_products[row.product]=int(row.count)
                count_month+=1
        return result_products
    
    def table_for(self,first_month,last_month,table,company):
        count_month= first_month
        for company_month, rows in self.data.items():
            name_company = company_month.split('_')
            if count_month<=last_month and name_company[0]==company and int(name_company[1])==count_month:
                for row in rows:
                    if table:
                        name_seller = any(d.get("seller") == row.seller for d in table)
                        name_product = any(d.get("product") == row.product for d in table)
                        name_qty = any(d.get("qty") == row.qty for d in table)
                        if name_seller and name_product and name_qty:
                            for dict in table:
                                if dict.get("seller")==row.seller and dict.get("product")==row.product and dict.get("qty")==row.qty:
                                    dict["count"]+=row.count
                                    dict["all"]+=row.all
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
                count_month+=1
        return table
        
    def table_for_companies(self,first_month,last_month):
        result_table = []
        for company in self.company_names:
            result_table = self.table_for(first_month,last_month,result_table,company)
        return result_table
       
    def bar_chart(self,first_month,last_month):
        result = {}
        for company in self.company_names:
            count_month = first_month
            for company_month, rows in self.data.items():
                name_company = company_month.split('_')
                if count_month<=last_month and name_company[0]==company and int(name_company[1])==count_month:
                    for row in rows:
                        if company in result:
                            if row.product in result[company]:
                                result[company][row.product]+=int(row.count)
                            else:
                                result[company][row.product]=int(row.count)
                        else:
                            dict = {}
                            dict[row.product]=int(row.count)
                            result[company] = dict
                    count_month+=1
        return result
    def piechart_expense(self,first_month,last_month):
        result = {}
        for company in self.company_names:
            count_month = first_month
            for company_month, rows in self.data.items():
                name_company = company_month.split('_')
                if count_month<=last_month and name_company[0]==company and int(name_company[1])==count_month:
                    for row in rows:
                        if company in result:
                            result[company]+=int(row.all)
                        else:
                            result[company]=int(row.all)
                    count_month+=1
        return result
    
    def table_for_company(self,first_month,last_month,company):
        result_table = []
        return self.table_for(first_month,last_month,result_table,company)

file_workers=FileWorker('C:/Users/Юрий/Desktop/buyDash/data.xlsx')
file_workers.file_read()

print(file_workers.get_month())

# file_workers.view_data()
# file_workers.view_company()
# piechart = file_workers.piechart_one_company(2,1,"Гугл")
# for key, value in piechart.items():
#     print(f"Key: {key}, Value: {value}")

# table_companies=file_workers.table_for_companies(1,2)
# for dict in table_companies:
#     for key, value in dict.items():
#         print(f"Key: {key}, Value: {value}")

# bar_chart = file_workers.bar_chart(1,2)
# for key, dict in bar_chart.items():
#     print(f"company: {key}")
#     for key1, value in dict.items():
#         print(f"Key: {key1}, Value: {value}")

# piechart_expense = file_workers.piechart_expense(1,2)
# for key, value in piechart_expense.items():
#     print(f"Key: {key}, Value: {value}")

# table_company=file_workers.table_for_company(1,2,"Гугл")
# for dict in table_company:
#     for key, value in dict.items():
#         print(f"Key: {key}, Value: {value}")