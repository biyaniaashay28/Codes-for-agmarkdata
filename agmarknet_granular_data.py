import datetime
import pandas as pd
import os
from pathlib import Path

path_backup = Path.cwd()/Path('Backup')
path_data = Path.cwd()/Path('Data')

if(path_backup.exists()==False):
    os.mkdir('Backup')
if(path_data.exists()==False):
    os.mkdir('Data')
    
month_dict = {'04':'Apr', '05':'May', '06':'Jun', '07':'Jul', '08':'Aug', '09':'Sep', '10':'Oct', '11':'Nov', '12':'Dec', '01':'Jan', '02':'Feb', '03':'Mar'}

commodity = input("Enter Commodity Name (Press Enter to use Default Maize):")
if(len(commodity)<=2):
    commodity = 'Maize'
commodity1 = commodity[0].upper()
commodity1 = commodity1 + commodity[1:].lower()
commodity = commodity1

from_date = input("Enter From Date (Press Enter to use the default date (01-04-2015))")
if(len(from_date)==0):
    from_date = "01-04-2015"
start = datetime.datetime.strptime(from_date, "%d-%m-%Y")

to_date = input("Enter From Date (Press Enter to use the default date (31-03-2020))")
if(len(to_date)==0):
    to_date = "31-03-2020"
end = datetime.datetime.strptime(to_date, "%d-%m-%Y") + datetime.timedelta(days=1)

date_array = (start + datetime.timedelta(days=x) for x in range(0, (end-start).days))
date_ar= []
for date_object in date_array:
    date_ar.append(date_object.strftime("%d-%m-%Y"))

date_list = []
for i in range(len(date_ar)):
    day = date_ar[i][:3]
    year = date_ar[i][5:]
    month = date_ar[i][3:5]
    date = str(day + month_dict[month] + year)
    date_list.append(date)

del month_dict
del date_array
del date_ar
del start
del end

master_df = pd.DataFrame()
file_name = commodity + '_granular_data_'+from_date+'_'+to_date
n = len(date_list)
for i in range(n):
    try:
        if(i%500==0):
            master_df.to_pickle(str(path_backup/Path(file_name+'_backup.pkl')))
        fr_date = date_list[i]
        url = 'http://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity=4&Tx_State=0&Tx_District=0&Tx_Market=0&DateFrom='+fr_date+'&DateTo='+to_date+'&Fr_Date='+fr_date+'&To_Date='+to_date+'&Tx_Trend=2&Tx_CommodityHead='+commodity+'&Tx_StateHead=--Select--&Tx_DistrictHead=--Select--&Tx_MarketHead=--Select--'
        dfs = pd.read_html(url)
        df = dfs[0]
        master_df = pd.concat([master_df,df])
        print("Done with the index: "+str(i+1) + ' of ' + str(n) + " Date: " + fr_date)
    except:
        print("Problem with index: " +str(i)+ " Date: " + fr_date)
master_df = master_df[master_df['State Name']!='-']
master_df = master_df.reset_index(drop = True)

master_df.to_excel(str(path_data/Path(file_name+'.xlsx')))
print('File Saved as ' + file_name + 'at ' + os.getcwd())  
master_df.to_pickle(str(path_backup/Path(file_name+'_backup.pkl')))