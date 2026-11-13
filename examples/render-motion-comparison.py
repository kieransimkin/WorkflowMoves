"""Render and verify a short, synthetic 60 fps motion comparison.

Run with FrameRudiments 0.4.29+, FFmpeg and a locally installed font:
  python examples/render-motion-comparison.py NEW_DIRECTORY --font FONT --ffmpeg FFMPEG
The font is used to render labels. Only the encoded example and its still ship.
"""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from PIL import Image, ImageDraw, ImageFont

import framerudiments
from framerudiments.demo import create_demo
from framerudiments.encoding import binaries
from framerudiments.io import read_json, write_json
from framerudiments.render import render

WIDTH, HEIGHT = 640, 360
FPS = 60
FRAMES = 120
LEFT, RIGHT = 160, 480


def motion_layer(name, center, asset, interpolate):
    return {
        "id": name,
        "asset": asset,
        "center": [center, 190],
        "width": 62,
        "bounds": [center - 130, 100, center + 130, 290],
        "motion": {"kind": "named", "pattern": "circle", "rate": 0.25,
                   "interpolate": interpolate},
        "mapping": {"dx": 75, "dy": 55},
    }


def label(text, left, right, top, bottom, size):
    return {"text": text, "style": {"box": [left, top, right, bottom],
                                    "font_size": size, "stroke": 0}}


def make_project(directory, font):
    path = create_demo(directory, font, width=WIDTH, height=HEIGHT)
    data = read_json(path)
    sprite = data["layers"][0]["asset"]
    data["title"] = "Same 60 fps, different motion"
    data["artist"] = "Synthetic native motion"
    data["audio"]["end_sample"] = data["audio"]["sample_rate"] * 2
    data.pop("lyrics")
    data.pop("cues")
    data["render_quality"] = {
        "spatial_scale": 1, "temporal_samples": 1, "antialias": 0,
    }
    data["identity"] = [
        label("Same 60 fps, different motion", 22, 618, 12, 56, 29),
        label("Held native samples", 24, 296, 64, 105, 22),
        label("Interpolated native samples", 344, 616, 64, 105, 22),
        label("Same source clock and path", 24, 616, 297, 334, 19),
    ]
    data["layers"] = [
        motion_layer("held", LEFT, sprite, False),
        motion_layer("interpolated", RIGHT, sprite, True),
    ]
    write_json(path, data)
    return path


def decoded_panels(ffmpeg, video):
    raw = subprocess.check_output([
        ffmpeg, "-v", "error", "-xerror", "-i", str(video), "-map", "0:v:0",
        "-fps_mode", "passthrough", "-pix_fmt", "rgb24", "-f", "rawvideo", "-",
    ])
    size = WIDTH * HEIGHT * 3
    if len(raw) != FRAMES * size:
        raise ValueError("Decoded frame count differs from the two-second 60 fps plan.")
    for start in range(0, len(raw), size):
        image = Image.frombytes("RGB", (WIDTH, HEIGHT), raw[start:start + size])
        yield image.crop((24, 112, 296, 282)), image.crop((344, 112, 616, 282)), image


def center(panel):
    # Exclude the cream rim and navy background. A coloured region's centroid
    # is less sensitive to H.264 quantisation than a whole-frame pixel hash.
    pixels = panel.load()
    xs, ys = [], []
    for y in range(panel.height):
        for x in range(panel.width):
            red, green, blue = pixels[x, y]
            if green > 120 and green - red > 40 and blue - red > 40:
                xs.append(x)
                ys.append(y)
    if not xs:
        raise ValueError("Expected the decoded teal sprite in each panel.")
    return sum(xs) / len(xs), sum(ys) / len(ys)


def count_holds(centers):
    return sum((after[0] - before[0]) ** 2 + (after[1] - before[1]) ** 2 < 0.75 ** 2
               for before, after in zip(centers, centers[1:]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--font", required=True, type=Path)
    parser.add_argument("--ffmpeg")
    args = parser.parse_args()

    output = args.directory.resolve()
    output.mkdir()
    project = make_project(output / "inputs", args.font)
    ffmpeg, ffprobe = binaries(args.ffmpeg)
    render(project, output / "render", ffmpeg=ffmpeg, ffprobe=ffprobe, preset="fast", crf=16)
    video = output / "render/video.mp4"
    manifest = read_json(output / "render/manifest.json")
    health = read_json(output / "render/candidate-health.json")
    if manifest["frames"] != FRAMES or manifest["fps"] != FPS or not health["review_allowed"]:
        raise ValueError("The native render did not pass technical QA at 60 fps.")
    left, right, stills = [], [], []
    for left_panel, right_panel, image in decoded_panels(ffmpeg, video):
        left.append(center(left_panel))
        right.append(center(right_panel))
        if len(left) in (1, 35, 80):
            stills.append(image)
    held, interpolated = count_holds(left), count_holds(right)
    if held < 40 or interpolated > 4:
        raise ValueError(f"The decoded comparison failed to distinguish the motion: {held}, {interpolated}.")
    sheet = Image.new("RGB", (960, 218), "#101b2e")
    draw = ImageDraw.Draw(sheet)
    label_font = ImageFont.truetype(str(args.font), 17)
    for index, (frame, image) in enumerate(zip((0, 34, 79), stills)):
        x = index * 320
        sheet.paste(image.resize((320, 180), Image.Resampling.LANCZOS), (x, 0))
        draw.text((x + 14, 189), f"Decoded frame {frame}", font=label_font, fill="#e5eef1")
    sheet.save(output / "comparison.png")
    evidence = {
        "renderer": framerudiments.__version__,
        "frames": FRAMES,
        "fps": FPS,
        "adjacent_pairs": FRAMES - 1,
        "held_pose_pairs": held,
        "interpolated_pose_pairs": interpolated,
        "centroid_hold_threshold_px": 0.75,
        "full_decode_and_native_cfr": "passed",
        "video_sha256": hashlib.sha256(video.read_bytes()).hexdigest(),
    }
    (output / "comparison.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(evidence))


if __name__ == "__main__":
    main()
