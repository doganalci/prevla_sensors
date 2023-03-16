import ntplib
import time

# NTP sunucusu adresi
ntp_server = "time.google.com"

# NTP sunucusuna bağlanma
client = ntplib.NTPClient()
def differ():
    
    while True:
        try:
            print("Connection Establish")
            return client.request(ntp_server).tx_time-time.time()   
        except:
            print("Time Stamp Connection Error\nRestablish connection")
        

dif = differ()

def getTime():
    return time.time() + dif

print(client.request(ntp_server).tx_time - time.time())
print(time.time()-client.request(ntp_server).tx_time)