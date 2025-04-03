import network
import socket
from time import sleep
import machine
import rp2
import sys
from HTTPRequest import HttpRequest
from web_server import WebServer

ssid = 'BTWholeHome-X8T'
password = 'EDwA7XDup9t3'

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        if rp2.bootsel_button() == 1:
            sys.exit()
        print('Waiting for connection...')
        pico_led.on()
        sleep(0.5)
        pico_led.off()
        sleep(0.5)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    pico_led.on()
    return ip

import libcamera
camera = libcamera.

ip = connect()

# === Video API Handler ===
def handle_control(request):
    """Handles /api/video POST requests."""
    
    if request.method != "GET":
        return WebServer.http_response(405, {"error": "Method Not Allowed"})

    try:
        
        return WebServer.http_response(200, {"status": "success"})
    except Exception as e:
        print(f"Exception: {e}")
        return WebServer.http_response(500, {"error": "Internal Server Error"})

# === Static HTML Handler ===
def handle_index(request):
    """Handles serving the index page."""
    try:
        with open("index.html") as fd:
            html = fd.read()
            return f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{html}"
    except Exception:
        return WebServer.http_response(500, {"error": "Could not load index.html"})

# === Initialize Web Server ===
server = WebServer(ip, 80)
server.add_route("GET", "/api/video", handle_control)
server.add_route("GET", "/", handle_index)

# === Start the server ===
server.serve()
