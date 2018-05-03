from bs4 import BeautifulSoup
import requests,pandas,os,csv
import datetime
'''
TODILIST(1):註解
TODILIST(2):分割function
'''
def legal_person(futures_type):
    while(1):
        print("輸入兩次空白為離開")
        start = input("請輸入開始年月日(YYYYMMDD):")
        end = input("請輸入結束年月日(YYYYMMDD):")
        try:

            date_start = datetime.datetime(int(start[0:4]),int(start[4:6]),int(start[6:8]))
            date_end = datetime.datetime(int(end[0:4]),int(end[4:6]),int(end[6:8]))
            today=datetime.datetime.today()
            three_years_ago=today.replace(year=today.year-3,day=today.day-1)
        except:
            if start=="" and end=="":
                return
            print("日期輸入錯誤，請重新輸入")
            continue
        if(date_start<three_years_ago or date_end>today):
            print("!!結束入期不能超過今天\n!!只能下載3年內的資料")
        elif date_start>date_end :
            print("開始日期大於結束日期，請重新輸入")
        else:
            break

    
    if futures_type=="TXF" or futures_type=="MXF":
        url="http://www.taifex.com.tw/chinese/3/7_12_8dl.asp"
    elif futures_type=="TXO":
        url="http://www.taifex.com.tw/chinese/3/7_12_10dl.asp"
    else:
        print('url error')
        return

    #data_test={'syear':'2018','smonth':'4','sday':'18','eyear':'2018','emonth':'4','eday':'18','COMMODITY_ID':'TXF'}
    data={'syear':date_start.year,'smonth':date_start.month,'sday':date_start.day,
           'eyear':date_end.year,'emonth':date_end.month,'eday':date_end.day,
           'COMMODITY_ID':futures_type}
    res=requests.post(url,data=data)
    res.encoding='Big5'
    export_csv=futures_type+"_三大法人("+start+"~"+end+").csv"
    with open(export_csv, 'w') as f:
        f.write(res.text)
    print("寫檔完成\n")

def dayily_report(futures_type):
    while(1):
        print("輸入兩次空白為離開")
        start = input("請輸入開始年月日(YYYYMMDD)，最早為19980801:")
        end = input("請輸入結束年月日(YYYYMMDD)，最晚為今天:")
        try:
            date_start = datetime.datetime(int(start[0:4]),int(start[4:6]),int(start[6:8]))
            date_end = datetime.datetime(int(end[0:4]),int(end[4:6]),int(end[6:8]))
            today=datetime.datetime.today()
            earliest=datetime.datetime(1998,8,1)
        except:
            if start=="" and end=="":
                return
            print("日期輸入錯誤，請重新輸入")
            continue
        if(date_start<earliest or date_end>today):
            print("!!結束入期不能超過今天\n!!只能下載1998/08/01以後")
        elif date_start>date_end :
            print("開始日期大於結束日期，請重新輸入")
        else:
            break

    
    if futures_type=="TX" or futures_type=="MTX":
        url="http://www.taifex.com.tw/chinese/3/3_1_2dl.asp"
    elif futures_type=="TXO":
        url="http://www.taifex.com.tw/chinese/3/3_2_3_b.asp"
    else:
        print('url error')
        return
    
    export_csv=futures_type+"_每日交易行情("+start+"~"+end+").csv"
    with open(export_csv,'w') as f:
        pass
        
    
    while True:
        data={'DATA_DATE' :date_start.strftime("%Y/%m/%d"),
              'DATA_DATE1' :date_start.strftime("%Y/%m/%d"),
              'datestart': date_start.strftime("%Y/%m/%d"),
              'dateend': date_start.strftime("%Y/%m/%d"),
              'COMMODITY_ID':futures_type}
        diff=date_end-date_start
        if diff.days<0:
            break
        else:
            date_start=date_start+datetime.timedelta(days=1)
        try:
            print("還剩"+str(diff.days)+"天")
            res=requests.post(url,data=data)
            res.encoding='big5'
            if "HTML"  not in res.text:
                with open(export_csv, 'a') as f:
                    f.write(res.text)  
        except:
            print("寫檔錯誤")
             
    print("寫檔完成\n")
    


    
if __name__ == '__main__':
    while(1):
        print("=================================")
        print("||1.三大法人大台日資料\t\t||")
        print("||2.三大法人小台日資料\t\t||")
        print("||3.三大法人選擇權日資料\t||")
        print("||4.大台指每日行情\t\t||")
        print("||5.小台指每日行情\t\t||")
        print("||6.台指選每日行情\t\t||")
        print("||0.離開\t\t\t||") 
        print("=================================")
            
        
        feature = input("請輸入需要功能:")
        if feature=='0':
            break
        elif feature=='1':
            legal_person("TXF")
        elif feature=='2':
            legal_person("MXF")
        elif feature=='3':
            legal_person("TXO")
        elif feature=='4':
            dayily_report("TX")
        elif feature=='5':
            dayily_report("MTX")
        elif feature=='6':
            dayily_report("TXO")
        else:
            print("輸入錯誤，請輸入0~6")
