LED GIF Generator

Includes:
- Script (skill/scripts/led_gif.py)
- Example GIFs

Usage:
python skill/scripts/led_gif.py --mode blink --color R,G,B --durations d1,d2,... --output file.gif
python skill/scripts/led_gif.py --mode fade --color R,G,B --period <ms> [--steps <n>] --output file.gif

Modes (--mode, default: blink):
- blink: alternates on/off; each --durations value (ms) is one frame, starting "on".
- fade: smooth sine-based brightness fade in and out over one --period (ms per full cycle).

Examples:
- Fast blink:
  python skill/scripts/led_gif.py --mode blink --color 255,0,0 --durations 200,200 --output fast_blink.gif

- Triple blink:
  python skill/scripts/led_gif.py --mode blink --color 255,255,255 --durations 500,500,500,500,500,2000 --output triple_blink.gif

- BLE pairing pulse:
  python skill/scripts/led_gif.py --mode blink --color 80,160,255 --durations 250,250,250,250,1000 --output ble_pairing.gif

- Breathing / pulse (fade mode):
  python skill/scripts/led_gif.py --mode fade --color 255,255,255 --period 2000 --steps 30 --output breathing.gif

- Static/solid (blink mode, single duration):
  python skill/scripts/led_gif.py --mode blink --color 0,255,0 --durations 1000 --output solid_green.gif

Durations are in ms. In blink mode, frames alternate ON/OFF automatically starting "on". In fade mode, --period is the total ms for one full fade-in-and-out cycle, and --steps controls how many frames render it (default 30).
