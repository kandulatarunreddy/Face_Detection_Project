int alarm = 12;
int door = 13;
int data;
void setup()
{
  Serial.begin(9600);
  pinMode(door, OUTPUT);
  pinMode(alarm, OUTPUT);
  digitalWrite(alarm, LOW);
}
void loop()
{
  while(Serial.available())
  {
    data = Serial.read();
  }
  if(data == '1')
  {
    digitalWrite(door, HIGH);
    delay(300);
    digitalWrite(door, LOW);
  }
  else if(data == '0')
  {
    digitalWrite(alarm, LOW);
  }
  else if(data == '2')
  {
    digitalWrite(alarm, HIGH);
  }
}
