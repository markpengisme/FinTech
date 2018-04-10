import os
def warning_notice(music_control):
	if music_control=='1':
		os.system('open 1.mp3')
	elif music_control=='2':
		os.system('open 2.mp3')
	elif music_control=='0':
		print("不播音樂")
	else :
		print("無此音樂")

