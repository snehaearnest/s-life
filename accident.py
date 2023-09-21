#define buttonPin 7
int buttonState = HIGH; 

unsigned long previousMillis = 0; 
const long interval = 30000;

String smsString="",stringnum,msg,changemsg="You have assigned the Admin previlage. TEAM IVANIOS";
String stringmsg,permnum="7994141617",emnum1="7994141617",emnum2="1234567890",tempnum,newnumber;    
char message[20],number[10],nwnumber[10];

int address = 0;
byte value;
#include <EEPROM.h>

static int i=0,j=0,count=0,flag=0,len=0;
char a;


#define echoPin 2
#define trigPin 3
long duration;
int distance;

#include <DHT.h>
#define DHTPIN A0
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

int temp;
String temperature,humidity;

#include <TinyGPS.h>
float lat, lon;
TinyGPS gps;
String resultlink;


void setup() 
{
  pinMode(trigPin, OUTPUT);
  pinMode(buttonPin, INPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
  Serial.println("setup.......");
  Serial1.begin(9600);
  dht.begin();
  Serial2.begin(9600);
  gsm_init();
  
  Read();
  len=tempnum.length();
  if(len >= 9)
  {
    permnum = tempnum;
  }
}

void gsm_init()
{
  Serial.println("gsminit...............");
  boolean at_flag=1;
  while(at_flag)
  {
    Serial2.println("AT");
    while(Serial2.available()>0)
    {
      if(Serial2.find("OK"))
      at_flag=0;
    }
    delay(400);
  }
  delay(1000);
  boolean echo_flag=1;
  while(echo_flag)
  {
    Serial2.println("ATE0");
    while(Serial2.available()>0)
    {
      if(Serial2.find("OK"))
      echo_flag=0;
    }
    delay(400);
  }
  delay(1000);

  boolean net_flag=1;
  while(net_flag)
  {
    Serial2.println("AT+CPIN?");
    while(Serial2.available()>0)
    {
      if(Serial2.find("+CPIN: READY"))
      net_flag=0;
    }
    delay(400);
  }
  Serial2.println("AT+CMGF=1");
  delay(400);
}

void loop() 
{
  Serial.println("loop......................");
  receiveSMS();
  temperature = String(dht.readTemperature());
  humidity = String(dht.readHumidity());
  temp=(dht.readTemperature());;

  if(flag==1)
  {
    Serial.println("flag=1..............");
    Serial.println(stringmsg);
    Serial.println(stringnum);
    delay(6000);
    locationlink();
    if(stringnum==permnum)
    {
      msg = "Location : " + resultlink + "\n Temperature : " + temperature + " \nHumidity : " + humidity;
      SendMessage(msg, stringnum);
    }
    else
    {
      msg = "Location : " + resultlink;
      SendMessage(msg, stringnum);
    }
    Serial.println(msg);
    delay(1000);
    flag=0;
  }

  if(temp>37)
  {
    Serial.println("temp exceeds................");
    msg = "Temperature exceeds limit \n Temperature : " + temperature + " \nHumidity : " + humidity;
    SendMessage(msg, permnum);
    Serial.println(msg);
    delay(1000);
  }
  int d = distancemeas(); 
  if (d <= 5) 
  {
    Serial.println("d less than 5.......................");
    Serial.println(d);
    terminate();
  }  
  
  delay(2000);
}

void crashed()
{
  Serial.println("crashed.........................");
    locationlink();
    String msg = "Car crashed!!\nLocation : " + resultlink + " \nTemperature : " + temperature + " \nHumidity : " + humidity;
    SendMessage(msg, emnum1);  //sending message to the emergency responce team1
    delay(5000);
    SendMessage(msg, emnum2);  //sending message to the emergency responce team2
    delay(5000);
    SendMessage(msg, permnum); //sending message to the family member
    Serial.println(msg);
    delay(1000);
}

int distancemeas()
{
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;
  Serial.println(distance);
   return distance;  
}
void receiveSMS()
{
  Serial.println("recievesms....................");
  message[0]='\0';
  number[0]='\0';
  Serial2.println("AT+CMGR=1");  
  smsString = Serial2.readString(); 
  Serial.println(smsString);
  for(i=0 ;  ; i++)
  {
    a = smsString[i];
    if(a == '\0')
    break;
    if(smsString[i]=='9')
    {
      if(smsString[i+1]=='1')
      {
        i+=2;
        break;
      }
    }
  }
  for(j=0 ; j<10 ; j++)
  {
    number[j] = smsString[i];
    i++;
  }
  number[j] = '\0';
stringnum=String(number);
Serial.println(stringnum);
Serial.println(permnum);
if(stringnum==permnum)
  {
  for(i=0 ; smsString[i] != '*' ; i++)
  {
    a = smsString[i];
    if(a == '\0')
    break;
  }
  
  i++;
  
  for(j=0 ; j<3 ; j++)
  {
    message[j] = smsString[i];
    i++;
  }
  message[j]='\0';
  stringmsg=String(message);
  Serial.println(stringmsg);
  
  for(j=0 ; j<10 ; j++)
    {
      nwnumber[j] = smsString[i];
      i++;
    }
    nwnumber[j]='\0';
    newnumber=String(nwnumber);
    Serial.println(newnumber);
    
    if(stringmsg=="CHG")
    {
      Clear();
      delay(400);
      permnum=newnumber;
      Serial.println("update............");
      Update();
      SendMessage(changemsg, permnum);
    }
    else if(stringmsg=="TRK")
    {
      flag=1;
    }
  }
  
  else
  {
    for(i=0 ; smsString[i] != '*' ; i++)
    {
      a = smsString[i];
      if(a == '\0')
      break;
    }
    
    i++;
    
    for(j=0 ; j<3 ; j++)
    {
      message[j] = smsString[i];
      i++;
    }
    message[j]='\0';
    stringmsg=String(message);
    Serial.println(stringmsg);

    if(stringmsg=="TRK")
    {
      flag=1;
    }
  }

  Serial2.println("AT+CMGD=1");
  delay(1000);
}

void Update()
{
  byte len = permnum.length();
  EEPROM.update(address, len);
  for(i = 0; i < len; i++)
  {
    EEPROM.update(address + 1 + i, permnum[i]);
  }
}

void Read()
{
  int len = EEPROM.read(address);
  char dat[len + 1];
  for(i = 0; i < len; i++)
  {
    dat[i] = EEPROM.read(address + 1 + i);
  }
  dat[len]='\0';
  tempnum=String(dat);
  Serial.println(tempnum);
}

void Clear() 
{
  for (i = 0 ; i < EEPROM.length() ; i++) 
  {
    EEPROM.write(i, 0);
  }
}

void SendMessage(String message, String n)
{
  Serial.println("sendsms..........................");
  boolean at_flag=1;
  while(at_flag)
  {
    Serial2.println("AT");
    while(Serial2.available()>0)
    {
      if(Serial2.find("OK"))
      at_flag=0;
    }
    delay(1000);
  }
  Serial2.print("AT+CMGS=");     // Send the SMS number. To whome message to send.
  String sg = "\"num\"";
  sg.replace("num", n);
  Serial2.print(sg);
  Serial2.println();
  delay(1000);
  Serial2.print(message); // SMS-Message body
  delay(1000);
  Serial2.println();
  Serial2.write(26);                //CTRL+Z key combination to send message
  Serial.println("COMPLETED.");
}

int locationlink() 
{
  
  while (true) 
  {
    while (Serial1.available()) 
    {
      if (gps.encode(Serial1.read()))
      {
        gps.f_get_position(&lat, &lon);
        resultlink = "http://www.google.com/maps/place/" + String(lat, 6) + "," + String(lon, 6);
        return 1;
      }
    }
  }
  
  Serial.println("locationlink");
}

void terminate() 
{
  Serial.println("terminate.....................");
  int flag1=0;
  delay(1000);
  while(1)
  {
    unsigned long currentMillis = millis();
    buttonState = digitalRead(buttonPin);
    if (buttonState == LOW) 
      {
        Serial.println("button pressed");
        break;
      }

    if (currentMillis - previousMillis >= interval) 
      {
        Serial.println("button not pressed");
        previousMillis = currentMillis;
        flag1=1;
        break;
      }
  }
  if(flag1 == 1)
  {
    crashed();
    flag1=0;
  }
}
