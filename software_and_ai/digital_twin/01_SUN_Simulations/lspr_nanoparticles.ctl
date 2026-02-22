; ============================================================================
; Symbiotic Factory — MIT MEEP LSPR Nanoparticle Simulation
; ============================================================================
; Module: 01_SUN_Simulations / lspr_nanoparticles.ctl
; License: GNU GPLv3
;
; FDTD simulation of Localized Surface Plasmon Resonance (LSPR) in Silver (Ag)
; nanoparticles embedded in the PAC biochar matrix. Sweeps nanoparticle diameter
; from 20nm to 100nm to find peak broadband solar absorption.
;
; Requires: MEEP (MIT Electromagnetic Equation Propagation)
; Run: meep lspr_nanoparticles.ctl
; ============================================================================

; --- Simulation Parameters ---
(define-param dp 0.050)      ; Nanoparticle diameter in μm (50nm default)
(define-param pad 0.200)     ; Padding around particle
(define-param dpml 0.100)    ; PML absorber thickness
(define-param resolution 200) ; Grid points per μm

; --- Silver (Ag) Drude-Lorentz Model ---
; Fitted to Johnson & Christy experimental data for Ag
; ε(ω) = ε_∞ - ω_p² / (ω² + iγω) + Σ Lorentzians
(define Ag
  (make medium
    (epsilon 3.7)
    (E-susceptibilities
      ; Drude term
      (make drude-susceptibility
        (frequency 1.0)        ; Normalized plasma frequency
        (gamma 0.0023)         ; Damping
        (sigma 9.17))
      ; Lorentz interband transitions
      (make lorentzian-susceptibility
        (frequency 0.816)
        (gamma 0.0852)
        (sigma 1.14))
      (make lorentzian-susceptibility
        (frequency 1.659)
        (gamma 0.388)
        (sigma 0.452))
    )))

; --- Geometry: Single Ag sphere in a dielectric host ---
; The host represents the PVA-biochar matrix (n ≈ 1.6)
(define host-medium (make medium (epsilon 2.56)))  ; n = 1.6

(set! geometry-lattice
  (make lattice (size (+ dp (* 2 pad) (* 2 dpml))
                       (+ dp (* 2 pad) (* 2 dpml))
                       (+ dp (* 2 pad) (* 2 dpml)))))

(set! geometry
  (list
    ; Background host medium
    (make block (center 0 0 0) (size infinity infinity infinity)
      (material host-medium))
    ; Silver nanoparticle
    (make sphere (center 0 0 0) (radius (/ dp 2))
      (material Ag))))

; --- PML Boundary Layers ---
(set! pml-layers (list (make pml (thickness dpml))))

; --- Source: Broadband pulse (300nm - 800nm ≈ AM1.5G solar spectrum) ---
(set! sources
  (list
    (make source
      (src (make gaussian-src
        (frequency 1.5)    ; Center frequency (in MEEP units: c/a)
        (fwidth 1.2)))     ; Bandwidth to cover solar spectrum
      (component Ex)
      (center (- (/ (+ dp (* 2 pad)) -2) (/ dpml 1)) 0 0)
      (size 0 (+ dp (* 2 pad)) (+ dp (* 2 pad))))))

; --- Monitors: Absorption cross-section ---
; Flux monitors surrounding the particle to measure scattered + absorbed power
(define near-flux
  (add-flux 1.5 1.2 100
    (make flux-region (center 0 0 0)
      (size (+ dp 0.02) (+ dp 0.02) (+ dp 0.02)))))

; --- Run simulation ---
(set! resolution resolution)
(run-until 50
  (at-beginning output-epsilon)
  (to-appended "flux" (at-every 1 output-flux)))

; --- Output: Print absorption efficiency ---
; Q_abs = σ_abs / (π * r²)
; Post-process with: meep-flux-to-absorption script
(print "MEEP LSPR Simulation Complete\n")
(print "Particle diameter: " dp " μm\n")
(print "Post-process flux data to extract Q_abs vs wavelength\n")
