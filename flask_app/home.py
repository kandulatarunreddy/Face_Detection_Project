from flask import Flask, redirect, url_for, flash
import serial as s 
import time 
app = Flask("tarun")
app.secret_key = 'dont tell no'
arduino = s.Serial('/dev/ttyUSB0', 9600)
# t.sleep(5)
# print('done waiting')
# arduino.write(b'1')
# t.sleep(3)
# arduino.write(b'0')
# print("written")
@app.route("/")
def hello():
	return """<!doctype html>
	<html>
	<body>
	<form action="/onclick",method = "POST">
	<input type = "submit" name = "button" value = "OPEN DOOR"><br> 
	<input type = "submit" name = "button" value = "CLOSE DOOR"><br>
	<input type = "submit" name = "button" value = "ALERT"><br>
	</form>
	</body>
	</html>
	"""
x=0
@app.route('/onclick', methods = ['GET', 'POST'])
def onclick():
	global x
	if request.method == 'POST':
		if request.form['button'] == "OPEN DOOR":
			#arduino.write(b'1')
		elif request.form['button'] == "CLOSE DOOR":
			#arduino.write(b'0')
		elif request.form['button'] == "ALERT":
			#arduino.write(b'2')
	return redirect(url_for('hello'))



#arduino.write(b'0')

if __name__ == '__main__':
	url = 'abcdfg.iot:5000'
	#app.config['SERVER_NAME'] = url
	app.run(host='0.0.0.0',debug = True)
	print(x)
