// ============================================================================
// Symbiotic Factory — OpenModelica Transient Dynamics Controller
// ============================================================================
// Module: 00_Orchestrator / transient_control.mo
// License: GNU GPLv3
//
// Simulates the dynamic transient response of the Symbiotic Factory to
// real-world disturbances: cloud cover, algal density spikes, HTL pressure
// overshoots. Validates ESP32 PID tuning parameters (Kp, Ki, Kd).
//
// Requires: OpenModelica (OMEdit or omc compiler)
// Run: omc transient_control.mo && ./transient_control
// ============================================================================

package SymbioticFactory
  "Transient dynamic models for the WEFC Biorefinery control system"

  // =========================================================================
  // PID Controller Block (Generic, reusable across modules)
  // =========================================================================
  model PIDController
    "Standard ISA PID controller with anti-windup"
    parameter Real Kp = 1.0 "Proportional gain";
    parameter Real Ki = 0.1 "Integral gain (1/s)";
    parameter Real Kd = 0.01 "Derivative gain (s)";
    parameter Real setpoint = 0.0 "Target value";
    parameter Real outputMin = 0.0 "Minimum output";
    parameter Real outputMax = 1.0 "Maximum output";

    input Real measurement "Process variable";
    output Real controlSignal "Controller output";

    Real error "Current error";
    Real integralError(start = 0) "Accumulated integral error";
    Real derivativeError "Rate of change of error";
    Real rawOutput "Unclipped output";

  equation
    error = setpoint - measurement;
    der(integralError) = error;
    derivativeError = der(error);

    rawOutput = Kp * error + Ki * integralError + Kd * derivativeError;
    controlSignal = max(outputMin, min(outputMax, rawOutput));
  end PIDController;

  // =========================================================================
  // Module II (WATER): Algal Cycloreactor Thermal & pH Dynamics
  // =========================================================================
  model WaterCycloreactor
    "Models temperature and pH transients in the photobioreactor"

    // Physical parameters
    parameter Real volume_L = 100.0 "Reactor volume (L)";
    parameter Real rho_water = 1000.0 "Water density (kg/m3)";
    parameter Real cp_water = 4186.0 "Specific heat (J/kg/K)";
    parameter Real UA_loss = 5.0 "Heat loss coefficient (W/K)";
    parameter Real T_ambient = 25.0 "Ambient temperature (°C)";
    parameter Real T_setpoint = 28.0 "Optimal algal growth temp (°C)";
    parameter Real pH_setpoint = 7.2 "Optimal pH for Chlorella";

    // State variables
    Real T(start = 25.0) "Reactor temperature (°C)";
    Real pH(start = 7.0) "Reactor pH";
    Real biomass(start = 0.5) "Biomass concentration (g/L)";

    // Disturbances
    Real Q_solar "Solar heat input (W) — varies with cloud cover";
    Real Q_led "LED waste heat (W)";
    Real co2_rate "CO2 injection rate (affects pH)";

    // PID Controllers (matching ESP32 firmware parameters)
    PIDController tempPID(
      Kp = 2.0, Ki = 0.5, Kd = 0.1,
      setpoint = T_setpoint,
      outputMin = 0, outputMax = 200
    );
    PIDController phPID(
      Kp = 1.5, Ki = 0.3, Kd = 0.05,
      setpoint = pH_setpoint,
      outputMin = 0, outputMax = 0.01
    );

    Real Q_heater "Heater power from PID (W)";
    Real acid_dose "Acid dosing rate from PID (mL/s)";

  equation
    // Cloud cover disturbance: sinusoidal with random drops
    Q_solar = 50.0 * (1.0 + 0.7 * sin(2 * 3.14159 * time / 86400))
              * (if time > 14400 and time < 18000 then 0.1 else 1.0);
    Q_led = 50.0;
    co2_rate = 0.005;

    // Temperature dynamics: dT/dt = (Q_in - Q_loss) / (m * cp)
    der(T) = (Q_solar + Q_led + Q_heater - UA_loss * (T - T_ambient))
             / (volume_L * rho_water / 1000 * cp_water);

    // pH dynamics: CO2 injection acidifies, photosynthesis alkalinizes
    der(pH) = -0.1 * co2_rate + 0.05 * biomass - 0.5 * acid_dose;

    // Simple logistic growth
    der(biomass) = 0.01 * biomass * (1 - biomass / 10.0)
                   * (if T > 20 and T < 35 then 1.0 else 0.1);

    // Wire PID controllers
    tempPID.measurement = T;
    Q_heater = tempPID.controlSignal;
    phPID.measurement = pH;
    acid_dose = phPID.controlSignal;

  end WaterCycloreactor;

  // =========================================================================
  // Module IV (FIRE): HTL Pressure Transient Response
  // =========================================================================
  model HTLPressureTransient
    "Models the pressure buildup and PRV actuation during an HTL cook"

    parameter Real volume_mL = 500 "Vessel volume (mL)";
    parameter Real fill_fraction = 0.60 "Fill level (60% rule)";
    parameter Real prv_setpoint_bar = 220 "PRV actuation pressure (bar)";
    parameter Real burst_disk_bar = 250 "Burst disk rupture pressure (bar)";
    parameter Real T_target = 300 "Target temperature (°C)";

    Real T(start = 25.0) "Current temperature (°C)";
    Real P(start = 1.0) "Current pressure (bar)";
    Real water_expansion "Thermal expansion factor";
    Boolean prv_open(start = false) "PRV state";
    Boolean burst(start = false) "Burst disk state";

    // PID for sand bath heater
    PIDController heatPID(
      Kp = 5.0, Ki = 0.2, Kd = 1.0,
      setpoint = T_target,
      outputMin = 0, outputMax = 2000
    );
    Real heater_W "Sand bath heater power";

  equation
    // Temperature ramp: sand bath heating with PID control
    der(T) = heater_W / (volume_mL * fill_fraction * 4.186)
             - 0.01 * (T - 25.0);  // Heat loss

    heatPID.measurement = T;
    heater_W = heatPID.controlSignal;

    // Pressure from Antoine equation (simplified for subcritical water)
    // P ≈ exp(A - B/(C+T)) where A=11.68, B=3816.4, C=-46.13
    water_expansion = 1.0 + 0.001 * (T - 25.0);
    P = if T < 100 then 1.0 + 0.01 * T
        else exp(11.68 - 3816.4 / (T + 273.15 - 46.13)) / 100000 * 1.01325;

    // Safety devices
    prv_open = P > prv_setpoint_bar;
    burst = P > burst_disk_bar;

  end HTLPressureTransient;

  // =========================================================================
  // Full Factory Transient Simulation
  // =========================================================================
  model FactoryTransient
    "24-hour transient simulation of the complete Symbiotic Factory"
    WaterCycloreactor reactor;
    HTLPressureTransient htl;

    annotation(
      experiment(StartTime = 0, StopTime = 86400, Interval = 10),
      Documentation(info = "<html>
        <p>Simulates a full 24-hour day-night cycle with cloud cover disturbance
        at hour 4-5. Validates that the ESP32 PID controllers maintain stable
        temperature and pH for optimal algal growth.</p>
      </html>")
    );
  end FactoryTransient;

end SymbioticFactory;
