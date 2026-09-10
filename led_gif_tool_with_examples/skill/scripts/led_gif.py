import argparse
import math
from PIL import Image, ImageDraw

def create_led_frame(color, state):
    img = Image.new("RGBA", (200,200), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    if state == "on":
        draw.ellipse((60,60,140,140), fill=(*color,255))
    else:
        draw.ellipse((60,60,140,140), outline=(180,180,180,255), width=2)
    return img

BAYER_8X8 = [
    [0, 32, 8, 40, 2, 34, 10, 42],
    [48, 16, 56, 24, 50, 18, 58, 26],
    [12, 44, 4, 36, 14, 46, 6, 38],
    [60, 28, 52, 20, 62, 30, 54, 22],
    [3, 35, 11, 43, 1, 33, 9, 41],
    [51, 19, 59, 27, 49, 17, 57, 25],
    [15, 47, 7, 39, 13, 45, 5, 37],
    [63, 31, 55, 23, 61, 29, 53, 21],
]

def create_fade_frame(color, density):
    # GIF transparency is per-pixel binary (no alpha blending), so a true
    # fade-to-transparent is faked with ordered dithering: at low density
    # only a sparse, evenly-spread scatter of pixels stay opaque, so the LED
    # visually dissolves into the background instead of just darkening.
    size = 200
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((60,60,140,140), fill=255)
    mask_px = mask.load()

    img = Image.new("RGBA", (size, size), (0,0,0,0))
    img_px = img.load()
    for y in range(size):
        row = BAYER_8X8[y % 8]
        for x in range(size):
            if mask_px[x,y] and (row[x % 8] / 64.0) < density:
                img_px[x,y] = (*color, 255)
    return img

def build_blink(color, durations):
    sequence = ["on" if i % 2 == 0 else "off" for i in range(len(durations))]
    frames = [create_led_frame(color, s) for s in sequence]
    return frames, durations

def build_fade(color, period, steps):
    frame_duration = max(1, period // steps)
    frames = []
    for i in range(steps):
        t = i / steps
        brightness = math.sin(math.pi * t) ** 2  # 0 -> 1 -> 0 over one period
        frames.append(create_fade_frame(color, brightness))
    durations = [frame_duration] * steps
    return frames, durations

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--color")
    parser.add_argument("--mode", choices=["blink", "fade"], default="blink")
    parser.add_argument("--durations")
    parser.add_argument("--period", type=int, help="fade mode: total ms for one fade in/out cycle")
    parser.add_argument("--steps", type=int, default=30, help="fade mode: number of frames per cycle")
    parser.add_argument("--output", default="led.gif")
    args = parser.parse_args()

    color = tuple(map(int, args.color.split(",")))

    if args.mode == "fade":
        frames, durations = build_fade(color, args.period, args.steps)
    else:
        durations = list(map(int, args.durations.split(",")))
        frames, durations = build_blink(color, durations)

    frames[0].save(
        args.output,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        disposal=2,
    )

if __name__ == "__main__":
    main()
