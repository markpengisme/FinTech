from bs4 import BeautifulSoup
import requests,pandas,os,csv
import datetime
#import traceback,sys  #debug

df_header=['日期','契約','到期月份(週別)','開盤價','最高價','最低價','最後成交價','漲跌價','漲跌%',
 '*盤後交易時段成交量','*一般交易時段成交量','*合計成交量','結算價','*未沖銷契約量',
 '最後最佳買價','最後最佳賣價','歷史最高價','歷史最低價']
url="http://www.taifex.com.tw/chinese/3/3_1_1.asp"

def  main():
    print("爬台指期近月基本資料(從輸入日期爬到現在)")
    today=datetime.datetime.today()
    date_input=input("請輸入年月日(YYYYMMDD)，預設為3年: ") or \
    today.replace(year=today.year-3).strftime('%Y%m%d')
    #判斷輸入正確並做一個空的csv
    try:
        date = datetime.datetime(int(date_input[0:4]),int(date_input[4:6]),int(date_input[6:8]))
        print("準備爬{}~{}的資料".format(date_input,today.strftime('%Y%m%d')))
        export_csv="TX_"+date_input+"~"+today.strftime('%Y%m%d')+".csv"
        try:
            os.remove(export_csv)
        except OSError:
            pass
    except:
        return print("輸入錯誤")
    

    #寫入header
    with open(export_csv, 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(df_header)
        
    #算出與今天差距並做迴圈
    diff=today-date
    for i in range(diff.days):
        
        #爬蟲的post request 參數由期交所分析得來
        res=requests.post(url, data = {'syear':date.year,'smonth':date.month,'sday':date.day,'COMMODITY_ID':"TX"})
        res.encoding='utf-8'
        
        #找到第一個table第二行(為台指近一月資料)並插入日期在寫入csv
        try:
            df1=pandas.read_html(res.text, attrs={'class': 'table_f'})[0]
            df1=df1.iloc[[1],:]
            df1.insert(loc=0,column='date',value=date)
            #display(df1)  for debug
            df1.to_csv(export_csv, mode='a+',header=False,index=False)
            
        #debug    
        except:
            #exc_type, exc_value, exc_traceback = sys.exc_info()
            #lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            #print (''.join('!! ' + line for line in lines) ) # Log it or whatever here
            pass
        
        #date++
        print("以爬完{}的資料{}".format(date.strftime('%Y%m%d'),'.'*(i%3+1)))
        date += datetime.timedelta(days=1)


if __name__ == '__main__':
    main()