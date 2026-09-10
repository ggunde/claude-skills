---
name: led-gif-generator
description: generate led blink or fade pattern gifs using python. use when user asks to create led indicators like "3 blinks", "ble pairing", "solid green", "breathing light", "pulsing led", or any led timing/fade pattern. outputs gif, preview, and python command.
---

# LED GIF Generator

## Behavior
- Always generate a GIF using Python (Pillow)
- Provide:
  1. Downloadable .gif
  2. Python command used
  3. Preview description

## Input Interpretation
Translate natural language into:
- color (RGB)
- mode: `blink` (discrete on/off) or `fade` (smooth breathing/pulse)
- blink mode: timing pattern (durations in ms)
- fade mode: period (ms per full fade in/out cycle) and optional steps (frames per cycle)

## Modes

### Blink (default)
`--mode blink --color R,G,B --durations d1,d2,...`
Alternates on/off; each duration is one frame, starting "on".

### Fade
`--mode fade --color R,G,B --period <ms> [--steps <n, default 30>]`
Smooth sine-based brightness fade in and out over one period, using ordered dithering (GIF has no real alpha blending). Use for "breathing", "pulsing", "fade in and out" requests.

## Presets

### BLE pairing
- Mode: blink
- Pattern: on,off,on,off,off
- Durations: 250,250,250,250,1000
- Color: soft blue (80,160,255)

### Triple blink
- Mode: blink
- Pattern: on,off,on,off,on,off
- Durations: 500,500,500,500,500,2000

### Fast alert
- Mode: blink
- Pattern: on,off
- Durations: 200,200
- Color: red

### Solid
- Mode: blink
- Pattern: on
- Duration: 1000

### Breathing / pulse
- Mode: fade
- Period: 2000 (one fade in+out cycle every 2s)
- Steps: 30
- Color: soft white (255,255,255) unless specified

## Execution
1. Parse user request
2. Map to mode + color + (durations, or period/steps)
3. Ensure a venv exists at `.venv` inside this skill's directory with Pillow installed:
   - If `.venv` is missing: `python3 -m venv .venv && .venv/bin/pip install --quiet Pillow`
   - This only needs to happen once; reuse the venv on subsequent runs.
4. Run `scripts/led_gif.py` using `.venv/bin/python` (not the system python)
5. Return file + command used

## Output format
- short explanation
- download link
- python command
