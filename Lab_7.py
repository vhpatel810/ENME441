import socket 
import RPi.GPIO as GPIO

s =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 8080))
s.listen(1)
GPIO.setmode(GPIO.BCM)
led_GPIO_pins = [14,15,18]
pwmfreq=100
pwms = []
for p in led_GPIO_pins:
	GPIO.setup(p,GPIO.OUT)
	pwm = GPIO.PWM(p, pwmfreq)
	pwm.start(0)
	pwms.append(pwm)
brightness = [0,0,0]
def parsePOSTdata(data):
	data_dict = {}
	idx = data.find('\r\n\r\n') + 4
	data = data[idx:]
	data_pairs = data.split('&')
	for pair in data_pairs:
		key_val = pair.split('=')
		if len(key_val) ==2:
			data_dict[key_val[0]] = key_val[1]
	return data_dict

def html():
	return """<html>
<form action="/" method="POST">
Brightness:<br>
<input type="range" name="brightness" min="0" max="100"><br>
<input type="radio" name="led" value="0"> LED1<br>
<input type="radio" name="led" value="1"> LED2<br>
<input type="radio" name="led" value="2"> LED3<br>
<input type="submit" value="Submit">
</form>
</html>"""

def send_webpage(conn,html):
	conn.send(b'HTTP/1.1 200 OK\r\n')
	conn.send(b'Content-type: text/html\r\n')
	conn.send(b'Connection: close\r\n\r\n')
	conn.sendall(html.encode())
try:
	while True: 
		conn, (client_ip,client_port) = s.accept()
		data = conn.recv(1024).decode()

		if not data: 
			conn.close()
			continue
		if "POST" in data:
			post = parsePOSTdata(data)
			try:
				led = int(post.get('led', '0'))
				val = int(post.get('brightness', '0'))
			except ValueError:
				led, val = 0, 0

			val = max(0, min(100,val))
			pwms[led].ChangeDutyCycle(val)
			brightness[led] = val
			send_webpage(conn, html())
		else:
			send_webpage(conn, html())

		conn.close()
except KeyboardInterrupt:
	print("\nStop server")
finally:
	for p in pwms:
		p.stop()
	GPIO.cleanup()
	s.close()
	print("GPIO cleaned")






