from pysense import Pysense
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE
from machine import SD, deepsleep
from network import LoRa
from machine import Pin
import struct
import socket
import pycom
import time
import os
import ubinascii

#Time marker started for deepsleep synchronization
progTimeStart = time.time()

#Mount SD card
sd = SD()
os.mount(sd, '/sd')
os.listdir('/sd')

#Intialize Sensor objects and turn off flash
py = Pysense()
mp = MPL3115A2(py,mode=ALTITUDE) # Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascals
si = SI7006A20(py)
lt = LTR329ALS01(py)
pycom.heartbeat(False)

#Initialize button object
button = Pin("P14",mode=Pin.IN, pull=Pin.PULL_UP)

#Flash green to show LoRa has been set
pycom.rgbled(0x001000)  #Green
time.sleep(0.5)
pycom.rgbled(0x000000)
pycom.nvs_set('init', 1)
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

#Set application information
app_eui = ubinascii.unhexlify('70B3D57ED001D022')
app_key = ubinascii.unhexlify('6339F8173F0EFE9F36F4955F826ED327')

#Create connection to loRa network
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet joined...')

#Create new socket for connection
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

#Open file for writing
pycom.heartbeat(False)
file = open('/sd/output_pysense.csv', 'a')
file.write('Temp:,Humidity:,Time:\n')

#Set time for deepsleep synchronization
defaultSleep = 300000

#Set socket for sending only
s.setblocking(True)

#Transmit temperature data as byte-code to TTN
ct = mp.temperature()
byte_val_temp = bytes(struct.pack('f',ct))
s.bind(1)
s.send(byte_val_temp)
print('Sending temp data: {}\r\n'.format(ct))

#Transmit humidity data as byte-code to TTN
ch = si.humidity()
byte_val_hum = bytes(struct.pack('f',ch))
s.bind(2)
s.send(byte_val_hum)
print('Sending humidity data: {}\r\n'.format(ch))

#Transmit humidity data as byte-code to TTN
bl = lt.light()
cl = (bl[0] + bl[1])/2
byte_val_lum = bytes(struct.pack('f',cl))
s.bind(3)
s.send(byte_val_lum)
print('Sending luminosity data: {}\r\n'.format(cl))

#Write to data to SD for backup
pycom.rgbled(0x001000)  #Green
time.sleep(0.5)
file.write('{},{},{},{}\r\n'.format(ct,ch,cl,time.time()))
pycom.rgbled(0x000000)

#Set socket to receiving
s.setblocking(False)

#Receive response from Gateway
data = s.recv(64)
print(data)
file.close()
#lora.nvram_save()

print('Sleeping')
#calculate program run time to keep consitent deepsleep length 
progTime = time.time() - progTimeStart
deepsleep(defaultSleep - progTime -  500)
'''try:
    print(pycom.nvs_get('init'))
    lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
    lora.nvram_restore()

    while not lora.has_joined():
        time.sleep(2.5)
        print('Not yet joined...')

    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

    pycom.heartbeat(False)
    file = open('/sd/output_pysense.csv', 'w')
    file.write('Temp:,Humidity:,Time:\n')

    defaultSleep = 300000

    s.setblocking(True)

    ct = mp.temperature()
    byte_val_temp = bytes(struct.pack('f',ct))
    socket.bind(1)
    s.send(byte_val_temp)
    print('Sending temp data: {}\r\n'.format(ct))

    ch = si.humidity()
    byte_val_hum = bytes(struct.pack('f',ch))
    socket.bind(2)
    s.send(byte_val_hum)
    print('Sending humidity data: {}\r\n'.format(ch))

    cl = lt.light()
    byte_val_lum = bytes(struct.pack('f',cl))
    socket.bind(3)
    s.send(byte_val_lum)
    print('Sending luminosity data: {}\r\n'.format(cl))

    pycom.rgbled(0x001000)  #Green
    time.sleep(0.5)
    file.write('{},{},{},{}\r\n'.format(ct,ch,cl,time.time()))
    pycom.rgbled(0x000000)

    s.setblocking(False)

    data = s.recv(64)
    print(data)
    lora.nvram_save()
    file.close()

    progTime = time.time()
    deepsleep(defaultSleep - progTime -  500)
except:
    while True:
        if button() == 0:'''
