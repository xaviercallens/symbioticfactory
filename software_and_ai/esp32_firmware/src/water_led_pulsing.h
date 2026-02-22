#ifndef WATER_LED_PULSING_H
#define WATER_LED_PULSING_H

#include <Arduino.h>
#include <Adafruit_NeoPixel.h>

// MODULE II (WATER) - Flashing-Light Effect Configuration
#define LED_PIN         4
#define NUM_LEDS        60

// Instantiating the NeoPixel strip
Adafruit_NeoPixel strip(NUM_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);

// Default pulse frequency (Hz). Can be dynamically updated via MQTT from AI
float currentPulseFrequencyHz = 25.0; 
unsigned long pulseIntervalMs = 1000.0 / currentPulseFrequencyHz;
unsigned long lastPulseTime = 0;
bool ledsOn = false;

// Hardware Timer for precise microsecond pulsing if needed, but using millis() for standard Hz
void initLEDPulsing() {
    strip.begin();
    strip.show(); // Initialize all pixels to 'off'
    Serial.println("[WATER] LED Cycloreactor Initialized. Awaiting pulsing loop.");
}

void processLEDPulsing() {
    unsigned long currentMillis = millis();
    pulseIntervalMs = 1000.0 / currentPulseFrequencyHz;

    // The Flashing-Light effect: rapid L/D cycling to bypass photoinhibition
    if (currentMillis - lastPulseTime >= pulseIntervalMs) {
        lastPulseTime = currentMillis;
        ledsOn = !ledsOn;
        
        if (ledsOn) {
            // Pulse RED (680nm) and BLUE (450nm) optimized for Chlorophyll a/b
            // Here we mix Max Red and Partial Blue
            strip.fill(strip.Color(255, 0, 100));
        } else {
            // Dark Phase
            strip.clear();
        }
        strip.show();
    }
}

// AI Hook to update the flashing frequency dynamically based on OD sensors
void updatePulseFrequency(float newFreqHz) {
    if (newFreqHz > 0 && newFreqHz <= 100) {
        currentPulseFrequencyHz = newFreqHz;
        Serial.print("[WATER] Matrix updated LED Pulse Frequency to: ");
        Serial.print(currentPulseFrequencyHz);
        Serial.println(" Hz");
    }
}

#endif // WATER_LED_PULSING_H
