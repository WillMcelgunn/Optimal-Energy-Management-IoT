from network import LoRa
import socket
import machine
import time
from machine import SD

# initialise LoRa in LORA mode
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
# more params can also be given, like frequency, tx power and spreading factor
lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)

# create a raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

#Mount SD card
sd = SD()
os.mount(sd, '/sd')
os.listdir('/sd')

#initialise data counter
counter = 1
while True:
    # get any data received...
    s.setblocking(False)
    data = s.recv(64)
    #If no data is received from node, set dataBool to false
    if not data:
        dataBool = False
    else:
        dataBool = True
    #If an error code if received, set dataBool to false
    if str(data) == 'b\'\\x10\'':
        dataBool = False
    #If dataBool is true, write that data to an SD card and send a confirmation to the sending node
    if dataBool:
        print(data)
        file = open('/sd/output.csv', 'a')
        file.write('{},{},{}\n'.format(counter, data, lora.stats()))
        file.close()
        time.sleep(2)
        #Set socket to sending mode
        s.setblocking(True)
        s.send(data)
        print('Data sent: ' + str(counter))
        #Increment data counter
        counter += 1
