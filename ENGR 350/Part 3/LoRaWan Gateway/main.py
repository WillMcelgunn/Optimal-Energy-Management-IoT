from network import WLAN
import ubinascii
wl = WLAN()
ubinascii.hexlify(wl.mac())[:6] + 'FFFE' + ubinascii.hexlify(wl.mac())[6:]

import config
from nanogateway import NanoGateway

if __name__ == '__main__':
    nanogw = NanoGateway(
        config.GATEWAY_ID,
        config.LORA_FREQUENCY,
        config.LORA_GW_DR,
        config.WIFI_SSID,
        config.WIFI_PASS,
        config.SERVER,
        config.PORT,
        config.NTP,
        config.NTP_PERIOD_S
        )
    print('starting NanoGateway')
    nanogw.start()
    #nanogw._log('You may now press ENTER to enter the REPL')
    input()
