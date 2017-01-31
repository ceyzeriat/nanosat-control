

frame = ctrl.kiss.Frame()

frame.source = ctrl.kiss.Callsign(b'\xe0\x60')
frame.destination = ctrl.kiss.Callsign(b'\x82\x98\x98')

frame.path = []

frame.text = b'\x18\x00\xC0\x01\x00\x08\xE0\x08\x00\x00\x00\x00\x61\x62'

frame.encode_kiss()


host = socket.gethostbyname(socket.gethostname())
k = kiss.TCPKISS(host=host, port=3211)
k.start()
k.write(frame.encode_kiss())




import socket
from threading import Thread
import select
import time


port = 3211
timeout = 1
l = 999

host = socket.gethostbyname(socket.gethostname())
port = int(port)
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
soc.connect((host, port))

data = []
while 1:
    ready = select.select([soc], [], [], timeout)
    if ready[0]:
        data.append(soc.recv(int(l)))
        print(data)
    else:
        print('maybe next time')




[Wed Jan 25 15:50:04 CET 2017]
Frame received FROM: PICSAT-1   TO: PICSAT-0    FCS: GOOD   RSSI: -66.2 dBm
 08 00 C0 08 00 06 2A CD 00 2C 35 EA 
|00|01|02|03|04|05|06|07|08|09|10|11|

[Wed Jan 25 15:50:04 CET 2017]
Frame received FROM: PICSAT-1   TO: PICSAT-0    FCS: GOOD   RSSI: -65.9 dBm
 08 01 C0 09 00 0A 2A CD 00 2C 35 FD 00 01 40 00 
|00|01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|

[Wed Jan 25 15:50:04 CET 2017]
Frame received FROM: PICSAT-1   TO: PICSAT-0    FCS: GOOD   RSSI: -65.9 dBm
 08 03 C0 0A 00 08 2A CD 00 2C 36 11 61 62 
|00|01|02|03|04|05|06|07|08|09|10|11|12|13|

[Wed Jan 25 15:50:05 CET 2017]
Frame received FROM: PICSAT-1   TO: PICSAT-0    FCS: GOOD   RSSI: -65.9 dBm
 08 02 C0 0B 00 0A 2A CD 00 2C 36 25 00 00 00 00 
|00|01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|
