# -*- coding: utf-8 -*-
from gtts import gTTS
import RPi.GPIO as GPIO
import requests
import os
from dweet import Dweet
#from ExemploGTTS import External
import time
#import subprocess

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(16,GPIO.OUT)

dweetEnvia = "https://dweet.io/dweet/for/"
nome = "fla"
var1 = "Temperatura"
var2 = "led"
var3 = "SistemaDesligado"
dweetRecebe = 'http://dweet.io/get/lastest/dweet/for/fla?led'
aux1 = 0
aux2 = 0

dweet = Dweet()

valorLed = 0
valorSistemaDesligado = 0

tempC = []      

def printcomum():
    print('***********************************************')
    print(temp)
    print('Led raspberry: '+ str(valorLed))
    print('SistemaDesligado raspberry: '+ str(valorSistemaDesligado))
    print('***********************************************')

for i in range(0,26):
    tempC.append(0)

while True:
    ostemp = os.popen('vcgencmd measure_temp').readline()
    temp = (ostemp.replace("temp=", "").replace("'C\n", ""))
    tempC.append(temp)
    tempC.pop(0)

    rqsString = dweetEnvia+nome+'?'+var1+'='+str(temp)+'&'+var2+'='+str(valorLed)+'&'+var3+'='+str(valorSistemaDesligado)
    
    enviaDweet = requests.get(rqsString)

    resposta = dweet.latest_dweet(name="fla")
    print ('Led DWEET: ' + str(resposta['with'][0]['content']['led']))
    #print ('SistemaDesligado DWEET: ' + str(resposta['with'][0]['content']['SistemaDesligado']))

    if valorLed == resposta['with'][0]['content']['led']:
        printcomum()  
    else:
        valorLed = resposta['with'][0]['content']['led']

    if int(resposta['with'][0]['content']['led']) == 0:
        GPIO.output(16,0)

        
        if aux1 == 0:
            audio = gTTS(text='LED verde desligado',lang='pt')
            audio.save("/tmp/audio.mp3")
            os.system("mpg321 /tmp/audio.mp3")
            aux1 = 1
            aux2 = 0
    else:
        GPIO.output(16,1)

        if aux2 == 0:
            audio = gTTS(text='LED verde ligado',lang='pt')
            audio.save("/tmp/audio.mp3")
            os.system("mpg321 /tmp/audio.mp3")
            aux2 = 1
            aux1 = 0
        

    #GPIO.output(16,0)
        
    """
    if valorSistemaDesligado == resposta['with'][0]['content']['SistemaDesligado']:
        printcomum()
    else:
        valorSistemaDesligado = resposta['with'][0]['content']['SistemaDesligado']
    """
    time.sleep(0.3)



