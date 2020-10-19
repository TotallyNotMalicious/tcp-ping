# looks a lil sloppy but I dont give a fuck :)
import sys
import socket
import time
import signal
import requests
from timeit import default_timer as timer

host = None
port = 80 # set the port to 80 default

maxCount = 999999 # I dont think you'll ever need more... however you can change this to your liking
count = 0

try:
    host = sys.argv[1]
except IndexError:
    print("Usage: python3 tcp-ping.py (ip) (port)")
    sys.exit(1)

try:
    port = int(sys.argv[2])
except ValueError:
    print("Error, Port Entered Incorrectly. Exiting Now")
    sys.exit(1)
except IndexError:
    pass

iplookup = requests.get(f"https://geolocation-db.com/json/{host}&position=true").json()
print("")
print("Host Info")
print("")
for key, value in iplookup.items():
        print(key, ' : ', value)
print("")
print("Starting Ping In 5 Secs")
print("")
time.sleep(5)

passed = 0
failed = 0

def signal_handler(signal, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

while count < maxCount:

    count += 1

    success = False

    s = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    s_start = timer()
    try:
        s.connect((host, int(port)))
        s.shutdown(socket.SHUT_RD)
        success = True
    except socket.timeout:
        print("Connection Down, No Response.")
        failed += 1
    except OSError as oserror:
        print("Error, OS Error - ", oserror)
        failed += 1

    s_stop = timer()
    s_runtime = "%.2f" % (1000 * (s_stop - s_start))

    if success:
        print("Connected To %s On Port %s Time %sms" % (host, port, s_runtime))
        passed += 1

    if count < maxCount:
        time.sleep(1)
