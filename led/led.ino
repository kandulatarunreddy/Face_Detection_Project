int led = 13;
int data;
void setup()
{
  pinMode(led, OUTPUT);
  Serial.begin(9600);
  //Serial.println('trying to connect');
}
void loop()
{
  if(Serial.available())
  {
    data = Serial.read();
  }
  if (data == '1')
  {
    digitalWrite(led,HIGH);
  }
  else if (data == '0')
  {
    digitalWrite(led, LOW);
  }
}
