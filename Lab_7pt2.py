import socket 
import RPi.GPIO as GPIO

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 8080))
s.listen(1)

GPIO.setmode(GPIO.BCM)
led_GPIO_pins = [14, 15, 18]
pwmfreq = 500
pwms = []
for p in led_GPIO_pins:
    GPIO.setup(p, GPIO.OUT)
    pwm = GPIO.PWM(p, pwmfreq)
    pwm.start(0)
    pwms.append(pwm)

brightness = [0, 0, 0]

def parsePOSTdata(data):
    data_dict = {}
    idx = data.find('\r\n\r\n') + 4
    data = data[idx:]
    data_pairs = data.split('&')
    for pair in data_pairs:
        key_val = pair.split('=')
        if len(key_val) == 2:
            data_dict[key_val[0]] = key_val[1]
    return data_dict

def html():
    return f"""<html>
<div style="width:260px;border:1px solid #999;padding:10px;border-radius:6px;font-family:sans-serif;">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
    <label>LED1</label>
    <span id="val0">{brightness[0]}</span>
  </div>
  <input id="s0" type="range" min="0" max="100" value="{brightness[0]}" style="width:100%;">

  <div style="display:flex;justify-content:space-between;align-items:center;margin:10px 0 6px;">
    <label>LED2</label>
    <span id="val1">{brightness[1]}</span>
  </div>
  <input id="s1" type="range" min="0" max="100" value="{brightness[1]}" style="width:100%;">

  <div style="display:flex;justify-content:space-between;align-items:center;margin:10px 0 6px;">
    <label>LED3</label>
    <span id="val2">{brightness[2]}</span>
  </div>
  <input id="s2" type="range" min="0" max="100" value="{brightness[2]}" style="width:100%;">
</div>

<script>
  function sendUpdate(ledIndex, value) {{
    fetch("/", {{
      method: "POST",
      headers: {{ "Content-Type": "application/x-www-form-urlencoded" }},
      body: "led=" + encodeURIComponent(ledIndex) + "&brightness=" + encodeURIComponent(value)
    }}).catch(() => {{ }});
  }}

  const sliders = [document.getElementById("s0"), document.getElementById("s1"), document.getElementById("s2")];
  const labels  = [document.getElementById("val0"), document.getElementById("val1"), document.getElementById("val2")];

  sliders.forEach((el, i) => {{
    el.addEventListener("input", (e) => {{
      const v = e.target.value;
      labels[i].textContent = v;
      sendUpdate(i, v);
    }});
  }});
</script>
</html>"""

def send_webpage(conn, htmlpage):
    conn.send(b'HTTP/1.1 200 OK\r\n')
    conn.send(b'Content-type: text/html\r\n')
    conn.send(b'Connection: close\r\n\r\n')
    conn.sendall(htmlpage.encode())

def send_ok(conn, text=b'OK'):
    conn.send(b'HTTP/1.1 200 OK\r\n')
    conn.send(b'Content-type: text/plain\r\n')
    conn.send(b'Connection: close\r\n\r\n')
    conn.sendall(text)

try:
    while True: 
        conn, (client_ip, client_port) = s.accept()
        data = conn.recv(2048).decode()

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

            val = max(0, min(100, val))
            if 0 <= led < len(pwms):               # <-- use spaces only
                pwms[led].ChangeDutyCycle(val)     # <-- aligned with the if
                brightness[led] = val              # <-- aligned with the if

            send_ok(conn, b'OK')                   # <-- keep only one send_ok
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



