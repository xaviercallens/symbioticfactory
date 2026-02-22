#ifndef FIRE_PID_CONTROLLER_H
#define FIRE_PID_CONTROLLER_H

#include <Arduino.h>
#include <DallasTemperature.h>
#include <OneWire.h>
#include <PID_v1.h>

// MODULE IV (FIRE) - Clostridium Fermentation Control
#define TEMP_WIRE_BUS 15
#define PH_SENSOR_PIN 34
#define HEATER_RELAY_PIN 18
#define ACID_PUMP_PIN 19
#define BASE_PUMP_PIN 21

// --- Temperature Control ---
OneWire oneWire(TEMP_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// Target 37°C for C. autoethanogenum
double tempSetpoint = 37.0;
double currentTemp = 0;
double heaterOutput = 0;

// Conservative PID tuning for thermal mass
double Kp_t = 2.0, Ki_t = 0.5, Kd_t = 0.1;
PID tempPID(&currentTemp, &heaterOutput, &tempSetpoint, Kp_t, Ki_t, Kd_t,
            DIRECT);

// --- pH Control ---
// Target 5.8 (Ethanol) or 6.4 (Butanol)
double phSetpoint = 5.8;
double currentPh = 0;
double phOutput = 0; // Negative means pump Acid, Positive means pump Base

double Kp_ph = 1.0, Ki_ph = 0.2, Kd_ph = 0.05;
PID phPID(&currentPh, &phOutput, &phSetpoint, Kp_ph, Ki_ph, Kd_ph, DIRECT);

void initFIREControllers() {
  sensors.begin();

  pinMode(HEATER_RELAY_PIN, OUTPUT);
  pinMode(ACID_PUMP_PIN, OUTPUT);
  pinMode(BASE_PUMP_PIN, OUTPUT);

  // Safety off
  digitalWrite(HEATER_RELAY_PIN, LOW);
  digitalWrite(ACID_PUMP_PIN, LOW);
  digitalWrite(BASE_PUMP_PIN, LOW);

  tempPID.SetMode(AUTOMATIC);
  // Limit relay PWM to prevent sudden boiling
  tempPID.SetOutputLimits(0, 255);

  phPID.SetMode(AUTOMATIC);
  // Acid/Base flow limits (-255 for max acid flow, 255 for max base flow)
  phPID.SetOutputLimits(-255, 255);

  Serial.println(
      "[FIRE] Subcritical Fermentation PID Controllers Initialized.");
}

void processFIREControllers() {
  // 1. Temperature Control
  sensors.requestTemperatures();
  currentTemp = sensors.getTempCByIndex(0);

  if (currentTemp > -100) { // Valid reading
    tempPID.Compute();
    analogWrite(HEATER_RELAY_PIN, heaterOutput);
  }

  // 2. pH Control
  int sensorValue = analogRead(PH_SENSOR_PIN);
  // Linear approximation for demonstration: 0-4095 mapped to pH 0-14
  currentPh = map(sensorValue, 0, 4095, 0, 140) / 10.0;

  phPID.Compute();

  // Actuate peristaltic pumps
  if (phOutput > 10) { // Needs Base
    analogWrite(BASE_PUMP_PIN, abs(phOutput));
    digitalWrite(ACID_PUMP_PIN, LOW);
  } else if (phOutput < -10) { // Needs Acid
    analogWrite(ACID_PUMP_PIN, abs(phOutput));
    digitalWrite(BASE_PUMP_PIN, LOW);
  } else {
    // Within deadband
    digitalWrite(ACID_PUMP_PIN, LOW);
    digitalWrite(BASE_PUMP_PIN, LOW);
  }
}

// AI Hook to dynamically shift metabolism (e.g., from Ethanol to Butanol path)
void updatePhSetpoint(double newPh) {
  phSetpoint = newPh;
  Serial.print("[FIRE] Target pH shifted to: ");
  Serial.println(phSetpoint);
}

#endif // FIRE_PID_CONTROLLER_H
