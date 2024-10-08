import network
import socket
from machine import Pin

# motor config
motor1_forward = Pin(32, Pin.OUT)
motor1_backward = Pin(33, Pin.OUT)
motor2_forward = Pin(25, Pin.OUT)
motor2_backward = Pin(26, Pin.OUT)

# Network Connection of Wifi

SSID = 'your_SSID'
PASSWORD = 'your_PASSWORD'

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    while not wlan.isconnected():
        print("Connecting to Network...")
    print("Connected to Network:", wlan.ifconfig())

# web server connection

def web_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print('Listening on', addr)

    while True:
        cl, addr = s.accept()
        print('Client connected from', addr)
        request = cl.recv(1024)
        request = str(request)
        print('Request:', request)

        # motor control

        if 'forward' in request:
            move_forward()
        elif 'backward' in request:
            move_backward()
        elif 'left' in request:
            turn_left()
        elif 'right' in request:
            turn_right()
        elif 'stop' in request:
            stop()

        cl.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
        cl.send('<h1>Remote Control Car</h1>'.encode())
        cl.send('<p><a href="/forward">Forward</a></p>'.encode())
        cl.send('<p><a href="/backward">Backward</a></p>'.encode())
        cl.send('<p><a href="/left">Left</a></p>'.encode())
        cl.send('<p><a href="/right">Right</a></p>'.encode())
        cl.send('<p><a href="/stop">Stop</a></p>'.encode())
        
        cl.close()

def move_forward():
    motor1_forward.on()
    motor1_backward.off()
    motor2_forward.on()
    motor2_backward.off()

def move_backward():
    motor1_forward.off()
    motor1_backward.on()
    motor2_forward.off()
    motor2_backward.on()

def turn_left():
    motor1_forward.off()
    motor1_backward.on()
    motor2_forward.on()
    motor2_backward.off()

def turn_right():
    motor1_forward.on()
    motor1_backward.off()
    motor2_forward.off()
    motor2_backward.on()

def stop():
    motor1_forward.off()
    motor1_backward.off()
    motor2_forward.off()
    motor2_backward.off()


connect_wifi()
web_server()