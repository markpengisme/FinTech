import requests, pandas, csv, time, datetime,os
import mail,music
url1="http://info512.taifex.com.tw/Future/FusaQuote_Norl.aspx"
url2="http://info512ah.taifex.com.tw/Future/FusaQuote_Norl.aspx"

def main():
	price=setting_price()
	mail_times=0
	#init
	url=init_parm()
	#Every 5 secs check
	while 1:
		vartime=time.localtime()
		url=check_regular_or_after_hour(url,vartime)
		mail_times=check_price(url,vartime,price,mail_times)
		time.sleep(0.6)

def init_parm():

	if ((time.localtime().tm_hour*60+time.localtime().tm_min>=8*60+45) and 
		(time.localtime().tm_hour*60+time.localtime().tm_min<=13*60+45)):
		url=url1
	else:
		url=url2
	return url

def check_regular_or_after_hour(url,vartime):
	'''
		Check contract is day or night
	'''
	if ((vartime.tm_hour==5 and vartime.tm_min==0 and vartime.tm_sec==5) or 
		(vartime.tm_hour==13 and vartime.tm_min==45 and vartime.tm_sec==5)):
		print("睡覺覺時間")
		#sleep two day if today is Saturday
		if datetime.date.today().isoweekday()==6:
			time.sleep(86400*2)		


		while(1):
			if ((time.localtime().tm_hour==8 and time.localtime().tm_min==44 and time.localtime().tm_sec==55) or 
				(time.localtime().tm_hour==14 and time.localtime().tm_min==59 and time.localtime().tm_sec==55)):
				print("開盤啦")
				break
			time.sleep(0.9)
			
	if vartime.tm_hour==8 and vartime.tm_min==45 and vartime.tm_sec==0:
		url=url1
	
	if vartime.tm_hour==15 and vartime.tm_min==0 and vartime.tm_sec==0:	
		count=1
		url=url2

	return url

def check_price(url,vartime,price,mail_times):
	res=requests.post(url)
	res.encoding='utf-8'
	df=pandas.read_html(res.text, attrs={'class':'custDataGrid'})[0].iloc[2][2]
	print(time.strftime('%Y/%m/%d %H:%M:%S',vartime)+'\t即時報價'+df)
	## 寄信
	if float(df)<=price[0] and mail_times<=10:
		print("觸低價")
		mail.test(str(price[0]))
		mail_times+=1
		music.warning_notice()
	if float(df)>=price[1] and mail_times<=10:
		print("觸高價")
		mail.test(str(price[1]))
		mail_times+=1
		music.warning_notice()
	return mail_times

def setting_price():
	##TODO價格相等就寄信
	while(1):
		low_price = input("低價位：")
		high_price = input("高價位：")
		if low_price.isnumeric() and high_price.isnumeric():
			price=[float(low_price),float(high_price)]
			break;
		print("輸入錯誤，請重新輸入")
	return price



if __name__ == '__main__':
	main()


