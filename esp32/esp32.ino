#define GREEN_LED 6
#define RED_LED 7
#define TEMP_SENS 4

const float VOLTAGE_REF = 3.3; // ESP32 reference voltage
const int ADC_RESOLUTION = 4095; // 12-bit ADC resolution

int greenLedStatus = LOW;
int redLedStatus = LOW;
int state = 0;
float temp = 0.0;


void setup() {
  Serial.begin(9600);

  pinMode(GREEN_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);

  state = 1;
}

void loop() {
  temp = ((analogRead(TEMP_SENS) / (float)ADC_RESOLUTION) * VOLTAGE_REF - 0.5) * 100.0;

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
