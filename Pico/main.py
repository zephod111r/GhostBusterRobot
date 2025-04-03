import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import QuaternionRobot
import machine
import rp2
import sys
from HTTPRequest import HttpRequest
import json
from web_server import WebServer
from Config import get_config_default


wlan = network.WLAN(network.STA_IF)
try:
    wlan.active(True)

    def connect():
        
        config = get_config_default("./config.json")
        #Connect to WLAN
        wlan.connect(config["ssid"], config["password"])
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

    ip = connect()

    # === Robot Control API Handler ===
    import PicoRobotics
    robot = PicoRobotics.KitronikPicoRobotics()

    def handle_motors(request):
        """Handles /api/control POST requests."""
        
        if request.method != "POST":
            return WebServer.http_response(405, {"error": "Method Not Allowed"})

        q = request.body_to_json()
        
        if isinstance(q, list):
            q = q[0]
        print(f"q: {q}")
        
        if not q:
            return WebServer.http_response(400, {"error": "Invalid JSON"})

        try:
            QuaternionRobot.quaternion_to_movement(robot, q)
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
    server.add_route("POST", "/api/motors", handle_motors)
    server.add_route("GET", "/", handle_index)

# === Start the server ===

    server.serve()
except Exception as e:
    print(f"Exception: {e}")
finally:
    print("Exiting")
    wlan.disconnect()
    while wlan.isconnected():
        print('Disconnecting...')
        pico_led.on()
        sleep(0.5)
        pico_led.off()
        sleep(0.5)
    print('Disconnected')
    pico_led.off()
    sys.exit()
