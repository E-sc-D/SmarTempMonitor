#include <WiFi.h>
#include <PubSubClient.h>

#define GREEN_LED 6
#define RED_LED 7
#define TEMP_SENS 4

#define WIFI_NOT_CONNECTED 0
#define WIFI_RECONNECT 1
#define MQTT_NOT_CONNECTED 2
#define OPERATING 3

const float VOLTAGE_REF = 3.3; // ESP32 reference voltage
const int ADC_RESOLUTION = 4095; // 12-bit ADC resolution

// WiFi credentials
const char* ssid = "Vodafone-A88608562";
const char* password = "6h7waw6tllpabakv";

// MQTT info
const char* mqttServer = "192.168.1.5";
const int mqttPort = 1883;

int greenLedStatus = LOW;
int redLedStatus = LOW;
int state = WIFI_NOT_CONNECTED;
int frequency = 1000;
float temp = 0.0;
char tempS[5];

WiFiClient espClient;
PubSubClient client(espClient);

void callback(char* topic, byte* payload, unsigned int length) {
  char message[length + 1];  // Array di caratteri per contenere il payload più il terminatore null '\0'
  memcpy(message, payload, length);
  message[length] = '\0';
  frequency = atoi(message);
}

void setup() {
  Serial.begin(9600);

  WiFi.begin(ssid, password);
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
  client.setKeepAlive(60);

  pinMode(GREEN_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
}

void loop() {
  Serial.println(frequency);
  temp = ((analogRead(TEMP_SENS) / (float)ADC_RESOLUTION) * VOLTAGE_REF - 0.5) * 100.0;
  setLed();

  switch (state)
  {
    case WIFI_NOT_CONNECTED:
      if (WiFi.status() != WL_CONNECTED) {
        delay(500);
        if (redLedStatus == LOW) {
            redLedStatus = HIGH;
            greenLedStatus = LOW;
        }
      } else {
        Serial.println("Connected to WiFi");
        state = MQTT_NOT_CONNECTED;
      }
      break;

    case WIFI_RECONNECT:
      WiFi.disconnect();
      WiFi.reconnect();
      state = WIFI_NOT_CONNECTED;
      break;

    case MQTT_NOT_CONNECTED:
      if (WiFi.status() != WL_CONNECTED) {
        state = WIFI_RECONNECT;
      }

      if (!client.connected()) {
        Serial.println("Connecting to MQTT...");
        if (client.connect("esp32")) {
          Serial.println("Connected to MQTT broker");
          // Subscribe to a topic
          client.subscribe("CU/frequency");
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
      if (WiFi.status() != WL_CONNECTED) {
        state = WIFI_RECONNECT;
      }

      client.loop();

      if (greenLedStatus == LOW) {
        greenLedStatus = HIGH;
        redLedStatus = LOW;
      }
      
      if (!client.connected()) {
        Serial.println("MQTT disconnesso! Riconnessione...");
        state = MQTT_NOT_CONNECTED;
      } else {
        dtostrf(temp, 3, 2, tempS);
        client.publish("esp32/temperature", tempS);
        delay(frequency);
      }
      break;
    
    default:
      break;
  }
}

void setLed() {
  digitalWrite(GREEN_LED, greenLedStatus);
  digitalWrite(RED_LED, redLedStatus);
}
