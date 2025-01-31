#include<Servo.h>

Servo myServo;

const int servoPin = 3;
const int btnPin = 2;
const int potPin = A2;
const double maxAngle = 90.0;
int prevBtn = 0;
int currentBtn = 0;
int mode = -1;
int serialAngle = 0;
/* const long serialDelay = 500;
long timeStamp = 0; */

//if you use the serial monitor to send the numerical value, be sure to select no line ending,since the terminator
//is considered a char and Serial available will be on for 2 times, and the second time an integer is read, it will return 0
//since no number has been found, hence the servo will go back to 0
void setup() {
  Serial.begin(9600);
  pinMode(btnPin,INPUT_PULLUP);
  pinMode(potPin,INPUT);
  pinMode(servoPin,OUTPUT);
  myServo.attach(servoPin);
  
}

void loop() {
  delay(100);
  currentBtn = digitalRead(btnPin);

  if(prevBtn == 1 && currentBtn == 0){
    mode = mode * -1;
  }
  
    
  if(mode == 1){
    myServo.write((maxAngle/1020.0)*analogRead(potPin));
   
  } else if(Serial.available() > 0 /* && ((millis() - timeStamp) > serialDelay) */ ){
    //timeStamp = millis();
    myServo.write(LimitNum(maxAngle,Serial.parseInt()));
    
  }

  prevBtn = currentBtn;
}

int LimitNum(int limit, int value){
  if(value > limit){
    return limit;
  }
  return value;
}
