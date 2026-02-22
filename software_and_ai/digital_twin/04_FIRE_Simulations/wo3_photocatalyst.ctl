; ============================================================================
; Symbiotic Factory — MIT MEEP: Ag/WO3 Z-Scheme Photocatalyst Simulation
; ============================================================================
; Module: 04_FIRE_Simulations / wo3_photocatalyst.ctl
; License: GNU GPLv3
;
; FDTD simulation of the Z-scheme heterojunction between Silver (Ag)
; nanoparticles and Tungsten Trioxide (WO3) semiconductor. Models the
; photon absorption and electron-hole pair generation under UV/Visible
; light for CO2 → CO photoreduction.
;
; Requires: MEEP (MIT Electromagnetic Equation Propagation)
; Run: meep wo3_photocatalyst.ctl
; ============================================================================

; --- Simulation Parameters ---
(define-param ag-diameter 0.040)   ; Ag NP diameter (μm) — 40nm
(define-param wo3-thickness 0.200) ; WO3 film thickness (μm) — 200nm
(define-param pad 0.300)
(define-param dpml 0.150)
(define-param resolution 200)

; --- Tungsten Trioxide (WO3) Optical Model ---
; Bandgap: ~2.7 eV (absorbs UV and blue light < 460nm)
; Refractive index: n ≈ 2.2 in visible range
(define WO3
  (make medium
    (epsilon 4.84)  ; n² = 2.2²
    (E-susceptibilities
      ; Interband absorption above bandgap (UV)
      (make lorentzian-susceptibility
        (frequency 1.10)     ; ~2.7 eV resonance
        (gamma 0.15)
        (sigma 3.5))
      ; Sub-bandgap tail
      (make lorentzian-susceptibility
        (frequency 0.80)
        (gamma 0.30)
        (sigma 0.8))
    )))

; --- Silver (Ag) Drude Model (same as SUN module) ---
(define Ag
  (make medium
    (epsilon 3.7)
    (E-susceptibilities
      (make drude-susceptibility
        (frequency 1.0)
        (gamma 0.0023)
        (sigma 9.17))
      (make lorentzian-susceptibility
        (frequency 0.816)
        (gamma 0.0852)
        (sigma 1.14))
    )))

; --- Geometry: Ag nanoparticle on WO3 thin film ---
; This models the heterojunction interface where SPR-enhanced hot electrons
; from Ag transfer into the WO3 conduction band (Z-scheme mechanism)
(define host (make medium (epsilon 1.77)))  ; Water/glass host (n=1.33)

(set! geometry-lattice
  (make lattice (size (+ wo3-thickness pad (* 2 dpml))
                       (+ 0.400 (* 2 dpml))
                       (+ 0.400 (* 2 dpml)))))

(set! geometry
  (list
    ; Glass/water host
    (make block (center 0 0 0) (size infinity infinity infinity)
      (material host))
    ; WO3 thin film
    (make block (center 0 0 0) (size wo3-thickness infinity infinity)
      (material WO3))
    ; Ag nanoparticle sitting on the WO3 surface
    (make sphere
      (center (+ (/ wo3-thickness 2) (/ ag-diameter 2)) 0 0)
      (radius (/ ag-diameter 2))
      (material Ag))
  ))

; --- PML Boundary ---
(set! pml-layers (list (make pml (thickness dpml))))

; --- Source: UV-Visible broadband pulse (300nm - 700nm) ---
(set! sources
  (list
    (make source
      (src (make gaussian-src
        (frequency 1.8)     ; Center in UV-blue
        (fwidth 1.5)))      ; Wide bandwidth
      (component Ex)
      (center (- (/ (+ wo3-thickness pad) -2) (/ dpml 1)) 0 0)
      (size 0 0.400 0.400))))

; --- Flux monitors ---
; Transmitted flux (through the WO3 + Ag system)
(define transmitted-flux
  (add-flux 1.8 1.5 100
    (make flux-region
      (center (+ (/ wo3-thickness 2) (/ ag-diameter 1) 0.05) 0 0)
      (size 0 0.400 0.400))))

; Reflected flux
(define reflected-flux
  (add-flux 1.8 1.5 100
    (make flux-region
      (center (- (/ wo3-thickness -2) 0.05) 0 0)
      (size 0 0.400 0.400))))

; --- Run ---
(set! resolution resolution)
(run-until 80
  (at-beginning output-epsilon))

; Post-processing: Absorption = 1 - T - R
; The absorption in the WO3 + Ag system quantifies the photocatalytic
; potential for CO2 → CO reduction via the Z-scheme mechanism
(print "MEEP WO3/Ag Z-Scheme Simulation Complete\n")
(print "Ag NP diameter: " ag-diameter " μm\n")
(print "WO3 film: " wo3-thickness " μm\n")
(print "Post-process: Absorption = 1 - T - R from flux data\n")
