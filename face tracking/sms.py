from twilio.rest import Client
import twilio

a_sid="ACda563b7eace2430d839e5946b9961151"    # Twilio SID number
a_token= "48c5ca876209392924865cf6eb3a6193" # Twilio Token number 
to_no= '+916303285040' # mobile number
my_no= '+17162614950'  # Twilio number


client =Client(a_sid, a_token)

f=open('/home/pi/log.txt','r')
my_msg= f.read()
f.close

msg=client.messages.create(to=to_no, from_=my_no, body=my_msg)

print ("your msg has been sent")
