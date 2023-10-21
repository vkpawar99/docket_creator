import pandas as pd

def get_info(file_path):
    #reading excel file
    inpt = pd.read_excel(file_path,index_col=False)

    # Specifying columns you want to forward fill
    columns_to_ffill = ['PO Number', 'Chg','Com', 'Type','Conf', 'Order Date','Buyer', 'Account Number','Supplier','Curr']
    inpt[columns_to_ffill] = inpt[columns_to_ffill].fillna(method='ffill')

    # generating dict to have po data with supplierr
    # Creating the dictionary
    result_dict = {}
    for po, sup in zip(inpt['PO Number'],inpt['Supplier']):
        
        if result_dict.get(sup) and po not in result_dict.get(sup)  :
            result_dict[sup].append(po)
        else:
            result_dict[sup] = [po]

    return result_dict

        
if __name__ == "__main__":
    get_info(r'C:\Users\vpawar\OneDrive - Congruex\Desktop\Automation 2023 (1)\2023 Tool Folder\docesign2\export29913.xlsx')