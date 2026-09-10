import argparse
from PIL import Image, ImageDraw

def create_led_frame(color, state, size=(200, 200)):
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    if state == "on":
        draw.ellipse((60, 60, 140, 140), fill=(*color, 255))
    else:
        draw.ellipse((60, 60, 140, 140), outline=(180, 180, 180, 255), width=2)
    return img

def parse_color(color_str):
    return tuple(map(int, color_str.split(",")))

def parse_durations(duration_str):
    return list(map(int, duration_str.split(",")))

def generate_sequence(n):
    return ["on" if i % 2 == 0 else "off" for i in range(n)]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--color", required=True)
    parser.add_argument("--durations", required=True)
    parser.add_argument("--output", default="led.gif")
    args = parser.parse_args()

    color = parse_color(args.color)
    durations = parse_durations(args.durations)
    sequence = generate_sequence(len(durations))

    frames = [create_led_frame(color, s) for s in sequence]
    frames[0].save(args.output, save_all=True, append_images=frames[1:], duration=durations, loop=0)

if __name__ == "__main__":
    main()
