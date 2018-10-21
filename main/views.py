# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.http import JsonResponse
from django.utils.cache import add_never_cache_headers
import serial
import time
import os
import pygame

def comSerial_read(request):
	pygame.mixer.init()
	print("播放音乐")
	track1=pygame.mixer.music.load("./main/static/music/raceStart.mp3")
	pygame.mixer.music.play()


	print("read start...")
	com=serial.Serial('/dev/tty.usbserial',115200, timeout=5, writeTimeout=7)
	# com=serial.Serial('/dev/tty.usbserial',115200)
	print (com.portstr)

	# hexStr = bytes.fromhex('ef fe 93 04 01 05 04 00 00 ff')
	# com.write(hexStr)
	# time.sleep(1)	
	# str = com.read(10)
	# time.sleep(3)
	
	
	print("before read")
	com.flush()
	com.flush()
	str = com.read(10)

	if com.isOpen():
		com.close()

	print("after read")
	print("len:",len(str))

	if len(str) == 0 :
		str = "0123456789"

	print(str)	

	# for i in str:
	# 	print(i)
	


	if str[5] == 51 :
		Setnum = 3
		settings.TEAM_NO = 2
		track1=pygame.mixer.music.load("./main/static/music/raceSuccess2.mp3")
		pygame.mixer.music.play()
	elif str[5] == 52 :
		Setnum = 4	
		settings.TEAM_NO = 3
		track1=pygame.mixer.music.load("./main/static/music/raceSuccess3.mp3")
		pygame.mixer.music.play()
	elif str[5] == 48 :
		Setnum = 0
		settings.TEAM_NO = 1
		track1=pygame.mixer.music.load("./main/static/music/raceSuccess1.mp3")
		pygame.mixer.music.play()
	else :
	    Setnum  = 0	
	    settings.TEAM_NO = 0

	subject = settings.FRONT_SUBJECT    
 	
	teamNum = settings.TEAM_NUM	
	teamNo  = settings.TEAM_NO
	
	team1_score =  settings.TEAM1_SCORE
	team2_score =  settings.TEAM2_SCORE
	team3_score =  settings.TEAM3_SCORE
	subject = subject-1
	if subject == 0 :
		subject = 3

	answer = settings.ANSWER[subject-1]

	print("subject\n",subject)

	return render(request, 'front_next.html', 
		{'subject':subject,'teamNum':teamNum,'teamNo':teamNo,
		"team1_score":team1_score,"team2_score":team2_score,"team3_score":team3_score,
		'answer':answer})    
	# print("teamNo:",teamNo) 
	# msg = {'rst':'yes','teamNo':teamNo}
	# response = JsonResponse(msg)

	# add_never_cache_headers(response)
	# print("before")
	# return response


def comSerial_write(request):
	result = request.GET.get('result')
	teamNo = request.GET.get('teamNo')

	result = int(result)
	print(result,type(result))

	teamNo = int(teamNo)
	print(teamNo,type(teamNo))

	initStr = 'ef fe 84 04 00 00 00 ff ff ff'
	sendList = list(initStr)

	if(teamNo == 1):
		chTeamNo = "0"
	if(teamNo == 2):
		chTeamNo = "3"
	if(teamNo == 3):
		chTeamNo = "4"		

	if(result == 1):
		settings.TOTAL_SCORE[teamNo-1] = settings.TOTAL_SCORE[teamNo-1]+10
		sendList[10] = chTeamNo
		scoreStr = str(settings.TOTAL_SCORE[teamNo-1])
		sendList[16] = scoreStr[0]
		finalStr = ''.join(sendList)
		
	print ("write start...")	
	com=serial.Serial('/dev/tty.usbserial',115200, timeout=5, writeTimeout=7)
	print (com.portstr)
	# 根据 抢答器编号和分数 来决定具体写入的数字

	print("finalStr:")
	print(finalStr)
	hexStr = bytes.fromhex(finalStr)

	print(hexStr)

	ret = 0
	index = 1
	while ret != 10:
		tt = "index:%d"%(index)
		print(tt)
		ret = com.write(hexStr)	
		tt = "after write,ret=%d"%ret
		print(tt)
		com.flush()
		index=index+1

	if com.isOpen():
		com.close()
	
	print(request.GET.get('result'))
	print(request.GET.get('teamNo'))
    
	msg = {'rst':'yes','teamNo':3,'teamScore':10}
	response = JsonResponse(msg)

	add_never_cache_headers(response)

	return response

# Create your views here. ,timeout=10
def front(request):
	settings.FRONT_SUBJECT = 1
	settings.TOTAL_SCORE=[0,0,0]

	subject = settings.FRONT_SUBJECT
	return render(request, 'front.html', {'subject':subject})

def front_next(request):
	subject = settings.FRONT_SUBJECT
	settings.FRONT_SUBJECT = (settings.FRONT_SUBJECT+1)
	if(settings.FRONT_SUBJECT > settings.FRONT_SUBJECT_CNT):
		settings.FRONT_SUBJECT = 1

	settings.TEAM_NO = 0	
	teamNum = settings.TEAM_NUM	
	teamNo = settings.TEAM_NO
	
	# team1_score =  settings.TEAM1_SCORE
	# team2_score =  settings.TEAM2_SCORE
	# team3_score =  settings.TEAM3_SCORE

	team1_score =  settings.TOTAL_SCORE[0]
	team2_score =  settings.TOTAL_SCORE[1]
	team3_score =  settings.TOTAL_SCORE[2]

	answer = settings.ANSWER[subject-1]

	return render(request, 'front_next.html', 
		{'subject':subject,'teamNum':teamNum,'teamNo':teamNo,
		"team1_score":team1_score,"team2_score":team2_score,"team3_score":team3_score,
		'answer':answer})

def background(request):
	settings.BACKGROUND_SUBJECT = 1
	subject = settings.BACKGROUND_SUBJECT
	return render(request, 'background.html', {'subject':subject})

def background_next(request):
	subject = settings.BACKGROUND_SUBJECT
	settings.BACKGROUND_SUBJECT = (settings.BACKGROUND_SUBJECT+1)
	if(settings.BACKGROUND_SUBJECT > settings.BACKGROUND_SUBJECT_CNT):
		settings.BACKGROUND_SUBJECT = 1
	return render(request, 'background_next.html', {'subject':subject})



