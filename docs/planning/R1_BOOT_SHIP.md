# R1 boot — ship demos (engines)

Install optional engines (system **ngspice** + Python extras):

```bash
sudo apt-get install -y ngspice libngspice0 libngspice0-dev   # Debian/Ubuntu
uv sync --extra engines --extra dev
```

## RLC (SPICE)

`problem.json`:

```json
{
  "cir": "* series RC\nV1 1 0 DC 10\nR1 1 2 1k\nC1 2 0 1u\n.tran 1m 10m\n.end\n"
}
```

```bash
uv run electrical-engineer run simulate-circuit
EE_NO_BROWSER=1 uv run electrical-engineer ui
```

## Control (Bode + step)

```bash
uv run electrical-engineer run solve-control-problem
# plots: runs/<id>/bode.png, step.png
```

Optional TF: `{"tf": "1/(s+1)"}` or `{"num": [1], "den": [1, 1]}` in `problem.json`.

## Power fault

```bash
cat > problem.json <<'EOF'
{"fault_type": "LG", "z1_pu": 0.1, "z2_pu": 0.1, "z0_pu": 0.3}
EOF
uv run electrical-engineer run simulate-power-fault
```

Checked |I| = 6.0 pu for default prefault 1.0 pu.

## Block diagram → Bode/step

```bash
cat > problem.json <<'EOF'
{
  "blocks": [{"id": "G", "tf": "10/(s+1)"}, {"id": "H", "tf": "1"}],
  "unity_feedback": {"forward": "G", "feedback": "H"}
}
EOF
uv run electrical-engineer run control-diagram-to-model
```

## Protection (study-level)

```bash
cat > problem.json <<'EOF'
{"ct_primary_a":300,"ct_secondary_a":5,"relay_pickup_a":2,"fault_current_a":800}
EOF
uv run electrical-engineer run study-protection-setting
```

## DC drive speed

```bash
cat > problem.json <<'EOF'
{"kind":"dc","v_dc":120,"ra_ohm":1,"k_torque":0.5,"t_load_nm":5}
EOF
uv run electrical-engineer run solve-drives-problem
```

## Digital control (z-domain)

```bash
cat > problem.json <<'EOF'
{"num":[0.1],"den":[1,-0.5],"ts":0.01}
EOF
uv run electrical-engineer run solve-digital-control-problem
```
