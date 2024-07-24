from flask import Flask, request, redirect, url_for
import time
import serial as s
#arduino = s.Serial("/dev/ttyUSB0")
x=0
app = Flask("karthik")
@app.route("/")
def homee():
	return """
	<!DOCTYPE HTML>
	<html>
	<head>
	<p> press the following buttons for the action to be done</p>
	</head>
	<body>
	<form action="/action" method = "post">
	<input type = "submit" name = "button" value = "OPEN DOOR"><br> 
	<input type = "submit" name = "button" value = "ALERT"><br>
	<input type = "submit" name = "button" value = "STOP ALERT"><br>
	</body>
	</html>
	"""
@app.route("/action", methods = ["GET", "POST"])
def action():
	global x
	if request.method == 'POST':
		if request.form['button'] == "OPEN DOOR":
			#arduino.write(b'1')
	
                        return redirect(url_for("homee"))

if __name__ == '__main__':
	x=0
	app.run(host= '0.0.0.0',debug= True)
	print(x)
