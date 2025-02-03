#include <Servo.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);  // 0x27 is a common address for many I2C LCDs
Servo myServo;

const int servoPin = 3;
const int btnPin = 2;
const int potPin = A2;
const double maxAngle = 90.0;
int prevBtn = 0;
int currentBtn = 0;
int mode = -1;

int reqWindow = 0;
double temp = 0.0;

const int BUFFER_SIZE = 50; // Define max buffer size
char serialData[BUFFER_SIZE]; // Buffer to store incoming data
int index = 0;

const long delayTime = 700;
long timeStamp = 0;

//if you use the serial monitor to send the numerical value, be sure to select no line ending,since the terminator
//is considered a char and Serial available will be on for 2 times, and the second time an integer is read, it will return 0
//since no number has been found, hence the servo will go back to 0
void setup() {
  Serial.begin(9600);
  pinMode(btnPin,INPUT_PULLUP);
  pinMode(potPin,INPUT);
  pinMode(servoPin,OUTPUT);
  myServo.attach(servoPin);
  lcd.init();    // Set the LCD dimensions (16 columns, 2 rows)
  resetScreen(); 
  timeStamp=millis();
}

void loop() {
  delay(100);
  currentBtn = digitalRead(btnPin);

  if(prevBtn == 1 && currentBtn == 0){
    mode = mode * -1;
  }

  if (Serial.available()) {
    // Read incoming serial data
    Serial.readBytesUntil('\n', serialData, BUFFER_SIZE - 1);
    serialData[strlen(serialData)] = '\0';  // Null-terminate

    // Use strtok() to split "variable:value"
    char *varName = strtok(serialData, ":");
    char *valueStr = strtok(NULL, ":");

    if (varName != NULL && valueStr != NULL) {
        if (strcmp(varName, "temp") == 0) {
            temp = atof(valueStr);
            Serial.println("temp received: ");
            Serial.println(temp);
        } else if (strcmp(varName, "win") == 0) {
            reqWindow = atoi(valueStr);
            Serial.println("window received: ");
            Serial.println(reqWindow);
        } else {
            Serial.println("Unknown variable");
            Serial.println(serialData);
        }
    } else {
        Serial.println("Invalid format!");
    }
  }
    
  if(mode == 1){
    myServo.write((maxAngle/1020.0)*analogRead(potPin));

    if(millis() - timeStamp > delayTime ) {
      timeStamp = millis();
      resetScreen();
      lcd.setCursor(0, 0);
      lcd.print("Manual");
      lcd.setCursor(0, 1);
      lcd.print(reqWindow);
      lcd.print(" Celsius");
    }
  } else {
    int angle = (int)((maxAngle/100.0)*(reqWindow));
    myServo.write(LimitNum(maxAngle,0,angle));

    if(millis() - timeStamp > delayTime ) {
      timeStamp = millis();
      resetScreen();
      lcd.setCursor(0, 0);
      lcd.print("Automatic");
    }
  }

  prevBtn = currentBtn;
}

int LimitNum(int uplimit,int lowlimit, int value){
  if(value >= uplimit){
    return uplimit;
  }
  if(value <= lowlimit){
    return lowlimit;
  }
  return value;
}

//reset dello schermo
void resetScreen() {
    lcd.backlight();
    lcd.clear();
}
