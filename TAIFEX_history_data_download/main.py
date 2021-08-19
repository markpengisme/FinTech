from bs4 import BeautifulSoup
import requests,pandas,os,csv
import datetime, dateutil

'''
TODILIST(1):註解
'''


def download_report(url, data, export_csv, method = 'w'):
    print(data)
    res = requests.post(url,data=data)
    res.encoding='Big5'
    try:
        if "HTML" not in res.text:
            with open("downloads/" + export_csv, method) as f:
                f.write(res.text)
        else:
            raise Exception()
        print("寫檔完成\n")
    except Exception as e:
        print(e)
        print("寫檔錯誤\n")

def legal_person(commodity_type):
    while(1):
        print("輸入兩次空白為離開")
        start = input("請輸入開始年月日(YYYY/MM/DD):")
        end = input("請輸入結束年月日(YYYY/MM/DD):")
        try:
            date_start = datetime.datetime(int(start[0:4]),int(start[5:7]),int(start[8:10]))
            date_end = datetime.datetime(int(end[0:4]),int(end[5:7]),int(end[8:10]))
            today = datetime.datetime.today()
            three_years_ago=today.replace(year=today.year-3,day=today.day-1)
        except:
            if start=="" and end=="":
                return
            print("日期輸入錯誤，請重新輸入")
            continue
        if date_start < three_years_ago or date_end > today:
            print("!!結束入期不能超過今天\n!!只能下載3年內的資料")
        elif date_start > date_end :
            print("開始日期大於結束日期，請重新輸入")
        else:
            break

    if commodity_type=="TXF":
        url={"TXF": "https://www.taifex.com.tw/cht/3/futContractsDateDown"}
    elif commodity_type=="MXF":
        url={"MXF": "https://www.taifex.com.tw/cht/3/futContractsDateDown"}
    elif commodity_type=="TXO":
        url={"TXO": "https://www.taifex.com.tw/cht/3/optContractsDateDown"}
    elif commodity_type=="all":
        urls={"future":"https://www.taifex.com.tw/cht/3/futContractsDateDown",
              "option":"https://www.taifex.com.tw/cht/3/optContractsDateDown"}
    else:
        print('url error')
        return


    for type_name, url in urls.items():
        data = {'queryStartDate': start,
                'queryEndDate': end,
                'commodityId': commodity_type}
        if data["commodityId"] == "all":
            del data["commodityId"]
        export_csv= type_name + "_三大法人(" + \
                    start.replace("/", "") + "~" + \
                    end.replace("/", "") + ").csv"
        download_report(url, data, export_csv)
       
def dayily_report(commodity_type):
    while(1):
        print("輸入兩次空白為離開")
        start = input("請輸入開始年月日(YYYY/MM/DD)，最早為1998/08/01: ")
        end = input("請輸入結束年月日(YYYY/MM/DD)，最晚為今天: ")
        try:
            date_start = datetime.datetime(int(start[0:4]),int(start[5:7]),int(start[8:10]))
            date_end = datetime.datetime(int(end[0:4]),int(end[5:7]),int(end[8:10]))
            today=datetime.datetime.today()
            earliest=datetime.datetime(1998,8,1)
        except:
            if start == "" and end == "":
                return
            print("日期輸入錯誤，請重新輸入")
            continue
        if date_start < earliest or date_end > today:
            print("!!結束入期不能超過今天\n!!只能下載1998/08/01以後")
        elif date_start > date_end :
            print("開始日期大於結束日期，請重新輸入")
        else:
            break

    if commodity_type=="TX":
        urls={"TX": "https://www.taifex.com.tw/cht/3/futDataDown"}
    elif commodity_type=="MTX":
        urls={"MTX": "https://www.taifex.com.tw/cht/3/futDataDown"}
    elif commodity_type=="TXO":
        urls={"TXO": "https://www.taifex.com.tw/cht/3/optDataDown"}
    elif commodity_type=="all":
        urls={"future": "https://www.taifex.com.tw/cht/3/futDataDown",
              "option": "https://www.taifex.com.tw/cht/3/optDataDown"}
    else:
        print('url error')
        return
    
    ds = date_start
    for type_name, url in urls.items():
        date_start = ds
        export_csv = type_name + "_每日交易行情(" + \
            start.replace("/", "") + "~" + \
            end.replace("/", "") + ").csv"

        data = {'down_type': 1,
                'commodity_id': commodity_type}

        with open("downloads/" + export_csv,'w') as f:
            pass
        
        while True:
            nm = date_start + datetime.timedelta(days=28)
            if nm < date_end:
                data['queryStartDate'] = date_start.strftime("%Y/%m/%d")
                data['queryEndDate'] = nm.strftime("%Y/%m/%d")
                download_report(url, data, export_csv, 'a')
                date_start = nm + datetime.timedelta(days=1)
            elif nm > date_end:
                nm = date_end
                data['queryStartDate'] = date_start.strftime("%Y/%m/%d")
                data['queryEndDate'] = nm.strftime("%Y/%m/%d")
                download_report(url, data, export_csv, 'a')
                break
            else:
                break


   

    
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
        elif feature=='7':
            legal_person("all")
            dayily_report("all")
        else:
            print("輸入錯誤，請輸入0~6")
