import requests, pandas, csv, time
import mail,music
url1="http://info512.taifex.com.tw/Future/FusaQuote_Norl.aspx"
url2="http://info512ah.taifex.com.tw/Future/FusaQuote_Norl.aspx"


##TODO(1):line(13) beauty

def main():
	'''
		setting entry,price,mail,music from function
	'''

	entry=setting_entry()
	price=setting_price()
	mail_control={'mail_times_max':setting_mail_times_max(),'mail_times':0}
	music_control=setting_music()
	#Every 5 secs check
	while 1:
		'''
			crawl and check price
		'''

		time.sleep(1)
		vartime=time.localtime()
		url=check_url()
		if not url: 
			print('睡覺')
			continue
		try:
			mail_control=check_price(url,vartime,entry,price,mail_control,music_control)
		except KeyboardInterrupt:
			print("Stop")
		except (IndexError,TypeError):
			print("IndexError or TypeError")
		except ConnectionError:
			print("ConnectionError")
		except:
		 	print("Some Error")
def check_url():
	'''
		check time to change url or sleep
	'''

	if time.localtime().tm_wday==5 and time.localtime().tm_hour==5 :
		print('週末睡兩天')
		while(1):
			time.sleep(60)
			if time.localtime().tm_wday==7 and time.localtime().tm_hour==5 :
				break
	elif ((time.localtime().tm_hour*60+time.localtime().tm_min>=8*60+45) and 
		(time.localtime().tm_hour*60+time.localtime().tm_min<=13*60+45)):
		url=url1
	elif((time.localtime().tm_hour*60+time.localtime().tm_min>=15*60) or
		(time.localtime().tm_hour*60+time.localtime().tm_min<=5*60)):
		url=url2
	else :
		url=''
	return url

def check_price(url,vartime,entry,price,mail_control,music_control):
	'''
		crawl price and caculate profit 
		if touch price , send mail
	'''
	res=requests.post(url)
	res.encoding='utf-8'
	df=pandas.read_html(res.text, attrs={'class':'custDataGrid'})[0].iloc[2][2]

	##crawl price
	if(entry['toggle']=='y'):
		profit=str((float(df)-float(entry['entry_price']))*float(entry['position'])*float(entry['lot'])*50)
		print(time.strftime('%Y/%m/%d %H:%M:%S',vartime)+'\t即時報價'+df+'\t損益金額'+profit+'元')

	else:
		print(time.strftime('%Y/%m/%d %H:%M:%S',vartime)+'\t即時報價'+df)

	##send mail	
	if float(df)<=price[0] and mail_control['mail_times']<mail_control['mail_times_max']:
		print("觸低價")
		mail.reminder_mail(str(price[0]))
		mail_control['mail_times']+=1
		music.warning_notice(music_control)

	if float(df)>=price[1] and mail_control['mail_times']<mail_control['mail_times_max']:
		print("觸高價")
		mail.reminder_mail(str(price[1]))
		mail_control['mail_times']+=1
		music.warning_notice(music_control)

	return mail_control

def setting_entry():
	'''
		setting profit feautre,
		if open ,then setting entry_price,postion,lot
	'''
	while(1):
		toggle = input("是否開啟損益模式(y/n):")
		if toggle=='y':
			while(1):
				entry_price = input("進場價格：")
				position = input("多空(1/-1):")
				lot = input("口數(預設標的為小台，大台請*4)：")
				if entry_price.isnumeric() and (position=='1' or 
					position=='-1') and lot.isnumeric():
					entry={
					'toggle':toggle,
					'entry_price':entry_price,
					'position':position,
					'lot':lot
					}
					return entry
				else:
					print("輸入錯誤，請重新輸入")


		elif toggle=='n':
			entry={
			'toggle':toggle,
			'entry_price':None,
			'position':None,
			'lot':None
			}
			return entry
		else:
			print("輸入錯誤，請重新輸入")		



def setting_price():
	'''
		setting low price, hight price
	'''
	while(1):
		low_price = input("低價位(預設1)：") or '1'
		high_price = input("高價位(預設100000)：") or '100000'
		if low_price.isnumeric() and high_price.isnumeric():
			price=[float(low_price),float(high_price)]
			break;
		print("輸入錯誤，請重新輸入")
	return price

def setting_mail_times_max():
	'''
		setting mail times
	'''
	while(1):
		mail_times_max = input("最多寄幾次信(預設10次)：") or '10'
		if mail_times_max.isnumeric() :
			break;
		print("輸入錯誤，請重新輸入")
	return int(mail_times_max)

def setting_music():
	'''
		setting music feature
	'''
	while(1):
		music_control = input("觸價是否播音樂(y/n，預設n)：") or 'n'
		if music_control=='y':
			return 1
		elif music_control=='n':
			return 0
		else:
			print("輸入錯誤，請重新輸入")




if __name__ == '__main__':
	main()


