import json
import time
import paho.mqtt.client as mqtt
import numpy as np

# Edge AI Configuration
MQTT_BROKER = "192.168.1.100"
MQTT_PORT = 1883
TELEMETRY_TOPIC = "symbiotic/telemetry/state"
WATER_COMMAND_TOPIC = "symbiotic/water/set_hz"

class WaterYieldOptimizer:
    """
    Predictive edge-AI agent for the WATER module (Algal Cycloreactors).
    Listens to OD (Optical Density) or incoming state telemetry from the ESP32.
    Adjusts the LED pulse frequency dynamically to bypass photoinhibition using Monod-Haldane kinetics.
    """
    def __init__(self):
        self.current_hz = 25.0
        
    def optimal_hz_prediction(self, current_algae_density: float) -> float:
        """
        Simplified ML mockup:
        As culture gets denser, the "flashing-light effect" needs to be faster 
        to ensure cells cycling through the dark zone are stimulated correctly.
        """
        # Baseline: 10Hz to 50Hz range based on OD
        # For this prototype, a simple linear scaling mapping density to frequency
        predicted_hz = np.interp(current_algae_density, [0.0, 5.0], [10.0, 50.0])
        return round(float(predicted_hz), 1)

def on_connect(client, userdata, flags, rc):
    print(f"[EDGE-AI] Connected to Symbiotic Factory Core Gateway (Result: {rc})")
    client.subscribe(TELEMETRY_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode('utf-8'))
        print(f"[RX] Node State: {payload}")
        
        # If we had real Optical Density (OD) sensors parsing via the payload
        # mock a rising density here just for the optimizer demonstration
        mock_density = np.random.uniform(0.5, 4.5) 
        
        optimizer = WaterYieldOptimizer()
        optimal_hz = optimizer.optimal_hz_prediction(mock_density)
        
        if optimal_hz != optimizer.current_hz:
            optimizer.current_hz = optimal_hz
            print(f"[OPTIMIZER] Publishing new Plastoquinone turnover frequency match: {optimal_hz} Hz")
            client.publish(WATER_COMMAND_TOPIC, str(optimal_hz))

    except Exception as e:
        print(f"[ERROR] Telemetry Parse Failure: {e}")

if __name__ == "__main__":
    print("Initializing Module II Cybernetic Optimizer...")
    
    # Initialize MQTT client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        # In a real deployed edge node, ping the local ESP32 router.
        # client.connect(MQTT_BROKER, MQTT_PORT, 60)
        # client.loop_forever()
        print(f"MQTT Client configured to connect to {MQTT_BROKER}:{MQTT_PORT}")
        print("Bypassing actual connection block for test dry-run.")
        
        # Test dry run
        opt = WaterYieldOptimizer()
        test_od = 3.2
        print(f"Dry-run: At OD {test_od}, optimal L/D pulse frequency is {opt.optimal_hz_prediction(test_od)} Hz")
        
    except KeyboardInterrupt:
        print("Optimizer Shutdown.")
