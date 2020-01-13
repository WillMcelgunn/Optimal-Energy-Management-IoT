from network import LoRa
from machine import ADC, SD
import socket
import time
import ubinascii
import pycom

#Create instance of battery voltage class
adc = ADC()

# Output Vref of P22
adc.vref_to_pin('P22')
adc.vref(1100)

# Check calibration by reading a known voltage
adc_c = adc.channel(pin='P16', attn=ADC.ATTN_11DB)

#Mount SD card for writing
sd = SD()
os.mount(sd, '/sd')
os.listdir('/sd')
file = open('/sd/output_pysense_battery.csv', 'a')
file.write('Voltage:\n')

#Set LoRa mode and join
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
#Infinite loop to repeatedly send data to TTN, and record data to SD card
while True:
    while not lora.has_joined():
        time.sleep(0.5)
        print('Not yet joined...')
    # create a LoRa socket
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    file.write('{}\r\n'.format(adc_c.voltage()))
    # set the LoRaWAN data rate
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

    # make the socket blocking
    # (waits for the data to be sent and for the 2 receive windows to expire)
    s.setblocking(True)
    print(adc_c.voltage())
    # send some data
    s.send(bytes([0x01, 0x02, 0x03]))
    data = [1, 2, 3]
    bdata = bytes(data)
    print(bdata)
    s.send(bdata)
    # make the socket non-blocking
    # (because if there's no data received it will block forever...)
    s.setblocking(False)

    # get any data received (if any...)
    data = s.recv(64)
    print(data)
    time.sleep(3)
#close file
file.close()
'''try:
    print(pycom.nvs_get('init'))
    lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
    lora.nvram_restore()
    while not lora.has_joined():
        time.sleep(0.5)
        print('Not yet joined...')
    # create a LoRa socket
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    file.write('{}\r\n'.format(adc_c.voltage()))
    # set the LoRaWAN data rate
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

    # make the socket blocking
    # (waits for the data to be sent and for the 2 receive windows to expire)
    s.setblocking(True)
    print(adc_c.voltage())
    # send some data
    s.send(bytes([0x01, 0x02, 0x03]))
    data = [1, 2, 3]
    bdata = bytes(data)
    print(bdata)
    s.send(bdata)
    # make the socket non-blocking
    # (because if there's no data received it will block forever...)
    s.setblocking(False)

    # get any data received (if any...)
    data = s.recv(64)
    print(data)
    lora.nvram_save()
    deepsleep(100)
except:
    pycom.nvs_set('init', 1)
    # Initialise LoRa in LORAWAN mode.
    # Please pick the region that matches where you are using the device:
    # Asia = LoRa.AS923
    # Australia = LoRa.AU915
    # Europe = LoRa.EU868
    # United States = LoRa.US915
    lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

    # create an OTAA authentication parameters
    app_eui = ubinascii.unhexlify('70B3D57ED001CB1E')
    app_key = ubinascii.unhexlify('51E9D188DC56DEA976357200D367914A')

    # join a network using OTAA (Over the Air Activation)
    lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

    # wait until the module has joined the network
    while not lora.has_joined():
        time.sleep(0.5)
        print('Not yet joined...')

    # create a LoRa socket
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    file.write('{},{}\r\n'.format(adc_c.voltage(),time.time()))
    print(adc_c.voltage())
    # set the LoRaWAN data rate
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

    # make the socket blocking
    # (waits for the data to be sent and for the 2 receive windows to expire)
    s.setblocking(True)

    # send some data
    s.send(bytes([0x01, 0x02, 0x03]))
    data = [1, 2, 3]
    bdata = bytes(data)
    print(bdata)
    s.send(bdata)
    # make the socket non-blocking
    # (because if there's no data received it will block forever...)
    s.setblocking(False)

    # get any data received (if any...)
    data = s.recv(64)
    print(data)
    lora.nvram_save()
    deepsleep(100)'''
