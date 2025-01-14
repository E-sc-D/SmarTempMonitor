#define GREEN_LED 6
#define RED_LED 7
#define TEMP_SENS 4

int greenLedStatus = LOW;
int redLedStatus = LOW;
int state = 0;
int temp = 0;

void setup() {
  pinMode(GREEN_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  pinMode(TEMP_SENS, INPUT);

  state = 1;
}

void loop() {
  temp = (int)((analogRead(TEMP_SENS) * 0.00488 ) / 0.01);

  switch (state)
  {
    case 1:
      if (greenLedStatus == LOW) {
        greenLedStatus = HIGH;
        redLedStatus = LOW;
      }
      break;
    case 2:
      if (redLedStatus == LOW) {
        redLedStatus = HIGH;
        greenLedStatus = LOW;
      }
      break;
    
    default:
      break;
  }

  digitalWrite(GREEN_LED, greenLedStatus);
  digitalWrite(RED_LED, redLedStatus);
  Serial.println(temp);
  delay(200);
}
