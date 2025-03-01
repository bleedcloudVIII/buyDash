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
        pass


class FileWorker:

    def __init__(self,file_path):
        self.file_path=file_path
        self.data={}
        self.company_names=[]
        pass   

    def file_read(self):
        all_lists=pd.read_excel(self.file_path,sheet_name=None)
        
        for sheet_name, list in all_lists.items():
            index_row=3
            monthly_data=[]
            for count in range(len(list)-3):
                row_data=list.loc[index_row]
                index_row+=1
                monthly_data.append(RowData(row_data[0],row_data[1],row_data[2],row_data[3],
                row_data[4],row_data[5],row_data[6],row_data[7]))
     
            self.data[sheet_name] = monthly_data
            name_comp=sheet_name.split('_')
            if name_comp[0] not in self.company_names:
                self.company_names.append(name_comp[0])           
        pass
    

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

file_workers=FileWorker('C:/Users/Grey/Desktop/buyDashBack/buyDash/data.xlsx')

file_workers.file_read()
file_workers.view_data()
file_workers.view_company()
