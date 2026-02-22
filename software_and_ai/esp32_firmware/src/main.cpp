#include <Arduino.h>
#include <PubSubClient.h>
#include <WiFi.h>

#include "fire_pid_controller.h"
#include "water_led_pulsing.h"

// --- Telemetry Configuration ---
const char *ssid = "YOUR_WIFI_SSID";
const char *password = "YOUR_WIFI_PASSWORD";
const char *mqtt_server = "192.168.1.100"; // Local Edge AI Server

WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastTelemetryTime = 0;
const long telemetryInterval = 5000; // Publish every 5 seconds

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  // Default to offline mode if Wi-Fi fails to allow local PID loops to continue
  int retries = 0;
  while (WiFi.status() != WL_CONNECTED && retries < 20) {
    delay(500);
    Serial.print(".");
    retries++;
  }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi connected");
  } else {
    Serial.println("\nWiFi failed. Operating offline.");
  }
}

void mqttCallback(char *topic, byte *payload, unsigned int length) {
  String message;
  for (int i = 0; i < length; i++)
    message += (char)payload[i];

  // Edge AI commands route here
  if (String(topic) == "symbiotic/water/set_hz") {
    updatePulseFrequency(message.toFloat());
  } else if (String(topic) == "symbiotic/fire/set_ph") {
    updatePhSetpoint(message.toDouble());
  }
}

void reconnect() {
  if (WiFi.status() == WL_CONNECTED && !client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("SymbioticFactory_Node1")) {
      Serial.println("connected");
      client.subscribe("symbiotic/water/set_hz");
      client.subscribe("symbiotic/fire/set_ph");
    } else {
      Serial.print("failed, rc=");
      Serial.println(client.state());
    }
  }
}

void setup() {
  Serial.begin(115200);
  Serial.println("--- Booting Symbiotic Factory Core (OS-WEFC v1.0) ---");

  initLEDPulsing();
  initFIREControllers();

  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(mqttCallback);
}

void loop() {
  if (!client.connected() && WiFi.status() == WL_CONNECTED) {
    reconnect();
  }
  client.loop();

  // 1. Execute microsecond/millisecond real-time edge control
  processLEDPulsing();
  processFIREControllers();

  // 2. Publish telemetry to Edge AI
  unsigned long currentMillis = millis();
  if (currentMillis - lastTelemetryTime >= telemetryInterval) {
    lastTelemetryTime = currentMillis;

    if (client.connected()) {
      char telemetryPayload[128];
      // Send FIRE module thermodynamic state
      snprintf(telemetryPayload, 128,
               "{\"temp\":%.2f, \"ph\":%.2f, \"hz\":%.2f}", currentTemp,
               currentPh, currentPulseFrequencyHz);
      client.publish("symbiotic/telemetry/state", telemetryPayload);
      Serial.printf("[TX] %s\n", telemetryPayload);
    }
  }
}
