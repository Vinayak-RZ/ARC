# Live A/B blind grading (2026-11-13)

Reference tie convention: P12 positive from area 1 to area 2. Opposite sign accepted if magnitude matches.

## Totals

| Submission | Quantity pass | Fraction |
|------------|---------------|----------|
| X | 24/25 | 0.9600 |
| Y | 21/25 | 0.8400 |

## Per-problem credit

| Problem | X | Y |
|---------|---|---|
| P1 | 1.00 | 1.00 |
| P2 | 1.00 | 1.00 |
| P3 | 1.00 | 1.00 |
| P4 | 1.00 | 1.00 |
| P5 | 1.00 | 0.25 |
| P6 | 1.00 | 1.00 |
| P7 | 1.00 | 1.00 |
| P8 | 0.75 | 0.75 |

## Arc engine gaps and library traps

- P4: `agc_two_area` does not match the sheet beta=21 algebraic model.
- P6: RLC transients are SPICE-only in Arc.
- P8: `drives_study` is not the exact equivalent circuit.
- P5: `control_runner` does not export margins; python-control uses wcp=gain crossover, wcg=phase crossover, and returns gm as a linear ratio (convert to dB with 20 log10).

## Quantity detail

### X
- P1 delta0_deg: PASS (sub=24.9011, ref=24.901062370366965)
- P1 delta_cr_deg: PASS (sub=78.3172, ref=78.31719753697801)
- P1 t_cr_s: PASS (sub=0.2966, ref=0.296478271484375)
- P2 stable: PASS (sub=True, ref=True)
- P2 max_rotor_angle_deg: PASS (sub=102.0623, ref=102.06231801305648)
- P3 P1_MW: PASS (sub=350.0, ref=350.00000000000006)
- P3 P2_MW: PASS (sub=250, ref=250)
- P3 P3_MW: PASS (sub=300, ref=300)
- P3 lambda_Rs_per_MWh: PASS (sub=9.8, ref=9.8)
- P4 steady_state_frequency_deviation_Hz: PASS (sub=-0.05952, ref=-0.05952380952380953)
- P4 Delta_P12_MW: PASS (sub=-25.0, ref=-25.0)
- P5 gain_crossover_rad_per_s: PASS (sub=1.55869, ref=1.55868640406249)
- P5 phase_margin_deg: PASS (sub=43.21, ref=43.20984525381832)
- P5 phase_crossover_rad_per_s: PASS (sub=4.47214, ref=4.4721359682367465)
- P5 gain_margin_dB: PASS (sub=15.563, ref=15.563024919110225)
- P6 damping_type: PASS (sub=underdamped, ref=underdamped)
- P6 Vc_peak_V: PASS (sub=15.0459, ref=15.045920575021169)
- P6 t_Vc_peak_s: PASS (sub=0.3428, ref=0.3428)
- P6 settling_time_2pct_s: PASS (sub=0.8409, ref=0.8409)
- P7 I_fault_pu: PASS (sub=4.2857, ref=4.285714285714286)
- P7 I_fault_kA: PASS (sub=7.4981, ref=7.498055444021114)
- P8 rotor_speed_rpm: PASS (sub=1440.0, ref=1440.0)
- P8 stator_current_A: PASS (sub=23.4561, ref=23.456116655053975)
- P8 developed_torque_Nm: FAIL (sub=44.0502, ref=88.10049292522137)
- P8 slip_at_max_torque: PASS (sub=0.16625, ref=0.16702205904356413)

### Y
- P1 delta0_deg: PASS (sub=24.901, ref=24.901062370366965)
- P1 delta_cr_deg: PASS (sub=78.317, ref=78.31719753697801)
- P1 t_cr_s: PASS (sub=0.2966, ref=0.296478271484375)
- P2 stable: PASS (sub=True, ref=True)
- P2 max_rotor_angle_deg: PASS (sub=102.062, ref=102.06231801305648)
- P3 P1_MW: PASS (sub=350.0, ref=350.00000000000006)
- P3 P2_MW: PASS (sub=250.0, ref=250)
- P3 P3_MW: PASS (sub=300.0, ref=300)
- P3 lambda_Rs_per_MWh: PASS (sub=9.8, ref=9.8)
- P4 steady_state_frequency_deviation_Hz: PASS (sub=-0.05952, ref=-0.05952380952380953)
- P4 Delta_P12_MW: PASS (sub=-25.0, ref=-25.0)
- P5 gain_crossover_rad_per_s: FAIL (sub=4.472, ref=1.55868640406249)
- P5 phase_margin_deg: PASS (sub=43.21, ref=43.20984525381832)
- P5 phase_crossover_rad_per_s: FAIL (sub=1.559, ref=4.4721359682367465)
- P5 gain_margin_dB: FAIL (sub=6.0, ref=15.563024919110225)
- P6 damping_type: PASS (sub=underdamped, ref=underdamped)
- P6 Vc_peak_V: PASS (sub=15.046, ref=15.045920575021169)
- P6 t_Vc_peak_s: PASS (sub=0.343, ref=0.3428)
- P6 settling_time_2pct_s: PASS (sub=0.841, ref=0.8409)
- P7 I_fault_pu: PASS (sub=4.286, ref=4.285714285714286)
- P7 I_fault_kA: PASS (sub=7.498, ref=7.498055444021114)
- P8 rotor_speed_rpm: PASS (sub=1440.0, ref=1440.0)
- P8 stator_current_A: PASS (sub=23.456, ref=23.456116655053975)
- P8 developed_torque_Nm: PASS (sub=88.1, ref=88.10049292522137)
- P8 slip_at_max_torque: FAIL (sub=0.1092, ref=0.16702205904356413)
