#include <WiFi.h>
#include <PubSubClient.h>

#define GREEN_LED 6
#define RED_LED 7
#define TEMP_SENS 4

#define WIFI_NOT_CONNECTED 0
#define OPERATING 1
#define MQTT_NOT_CONNECTED 2

const float VOLTAGE_REF = 3.3; // ESP32 reference voltage
const int ADC_RESOLUTION = 4095; // 12-bit ADC resolution

// WiFi credentials
const char* ssid = "ESP";
const char* password = "pippo123";

// MQTT info
const char* mqttServer = "192.168.141.58";
const int mqttPort = 1883;

int greenLedStatus = LOW;
int redLedStatus = LOW;
int state = WIFI_NOT_CONNECTED;
float temp = 0.0;

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(9600);

  WiFi.begin(ssid, password);
  client.setServer(mqttServer, mqttPort);
  // Subscribe to a topic
  client.subscribe("esp32/temperature");

  pinMode(GREEN_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
}

void loop() {
  client.loop();
  temp = ((analogRead(TEMP_SENS) / (float)ADC_RESOLUTION) * VOLTAGE_REF - 0.5) * 100.0;

  switch (state)
  {
    case WIFI_NOT_CONNECTED:
      if (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.println("Connecting to WiFi...");
      } else {
        Serial.println("Connected to WiFi");
        state = MQTT_NOT_CONNECTED;
      }
      break;
    case MQTT_NOT_CONNECTED:
      if (!client.connected()) {
        Serial.println("Connecting to MQTT...");
        if (client.connect("ESP32Client")) {
          Serial.println("Connected to MQTT broker");
          state = OPERATING;
        } else {
          Serial.print("Failed with state ");
          Serial.println(client.state());
          if (redLedStatus == LOW) {
            redLedStatus = HIGH;
            greenLedStatus = LOW;
          }
          delay(2000);
        }
      }
      break;
    case OPERATING:
      if (greenLedStatus == LOW) {
        greenLedStatus = HIGH;
        redLedStatus = LOW;
      }
      
      if (!client.connected()) {
        state = MQTT_NOT_CONNECTED;
      }

      client.publish("esp32/temperature", temp);
      break;
    
    default:
      break;
  }

  digitalWrite(GREEN_LED, greenLedStatus);
  digitalWrite(RED_LED, redLedStatus);
  Serial.println(temp);
}
