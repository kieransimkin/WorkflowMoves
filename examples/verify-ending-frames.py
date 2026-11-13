"""Reproduce a stale last-frame still using two synthetic FrameRudiments renders.

Run with FrameRudiments 0.4.29, Pillow and a pinned FFmpeg/FFprobe:
    python examples/verify-ending-frames.py NEW_DIR --font FONT --ffmpeg FFMPEG
The two-second 60 fps clips use only generated shapes, text and a test tone.
"""

import argparse
import json
from pathlib import Path
import shutil
import subprocess

import framerudiments
from framerudiments.demo import create_demo
from framerudiments.encoding import binaries
from framerudiments.io import read_json, sha256, write_json
from framerudiments.render import extract_encoded_checkpoints, render
from PIL import Image, ImageDraw, ImageFont


def encode(root, heading, colour, font, ffmpeg, ffprobe):
    project = create_demo(root / "inputs", font, width=480, height=270)
    data = read_json(project)
    data.pop("lyrics")
    data.pop("cues")
    data["title"] = heading
    data["audio"]["end_sample"] = 2 * data["audio"]["sample_rate"]
    data["background"]["colour"] = colour
    data["identity"] = [
        {"text": heading, "style": {"box": [16, 32, 464, 96], "font_size": 41, "stroke": 0}}
    ]
    data["layers"] = data["layers"][:1]
    write_json(project, data)
    output = root / "render"
    render(project, output, ffmpeg=ffmpeg, ffprobe=ffprobe, preset="fast", crf=16)
    health = read_json(output / "candidate-health.json")
    if not health["review_allowed"] or health["technical_qa"] != "passed":
        raise ValueError(f"Native verification did not pass for {heading}.")
    return output / "video.mp4"


def ending_frames(root, old_video, current_video, ffmpeg, ffprobe):
    probe = subprocess.run(
        [ffprobe, "-v", "error", "-select_streams", "v:0", "-show_frames",
         "-show_entries", "frame=best_effort_timestamp_time", "-of", "json", current_video],
        check=True, capture_output=True, text=True, timeout=30,
    )
    frames = json.loads(probe.stdout)["frames"]
    if len(frames) != 120:
        raise ValueError("Expected 120 independently decoded frames.")

    prior = root / "prior-frames"
    current = root / "current-frames"
    prior.mkdir()
    current.mkdir()
    last = len(frames) - 1
    selected = f"encoded-{last:08}.png"
    extract_encoded_checkpoints(ffmpeg, old_video, prior, [last])
    previous = prior / selected
    reused_path = root / "last-frame.png"
    shutil.copyfile(previous, reused_path)
    previous_hash = sha256(reused_path)

    failed_seek = [ffmpeg, "-v", "warning", "-nostdin", "-sseof", "-0.005", "-i", current_video,
                   "-map", "0:v:0", "-frames:v", "1", "-update", "1"]
    unguarded = subprocess.run(
        [*failed_seek, "-y", reused_path], capture_output=True, text=True, timeout=30,
    )
    guarded_path = current / "seek-result.png"
    guarded = subprocess.run(
        [*failed_seek, "-abort_on", "empty_output_stream", "-n", guarded_path],
        capture_output=True, text=True, timeout=30,
    )
    empty_seek = "Output file is empty" in unguarded.stderr
    if not empty_seek or sha256(reused_path) != previous_hash or guarded.returncode == 0 or guarded_path.exists():
        raise ValueError("The expected empty-seek behavior was not reproduced.")

    extract_encoded_checkpoints(ffmpeg, current_video, current, [0, last])
    if {path.name for path in current.iterdir()} != {"encoded-00000000.png", selected}:
        raise ValueError("Checkpoint filenames or count differ from the request.")
    actual_frame = current / selected
    if sha256(actual_frame) == previous_hash:
        raise ValueError("The fresh ending still matches the stale output.")
    evidence = {
        "renderer": framerudiments.__version__,
        "ffmpeg": subprocess.check_output([ffmpeg, "-version"], text=True, timeout=20).splitlines()[0],
        "prior_video_sha256": sha256(old_video),
        "current_video_sha256": sha256(current_video),
        "frames": len(frames),
        "last_decoded_frame": last,
        "last_decoded_video_time": frames[-1]["best_effort_timestamp_time"],
        "unguarded_seek_exit_code": unguarded.returncode,
        "unguarded_seek_empty_output": empty_seek,
        "guarded_seek_failed": guarded.returncode != 0,
        "stale_png_sha256": previous_hash,
        "fresh_png_sha256": sha256(actual_frame),
    }
    return reused_path, actual_frame, evidence


def contact_sheet(pictures, output, font):
    sheet = Image.new("RGB", (996, 334), "#0f172a")
    draw = ImageDraw.Draw(sheet)
    label = ImageFont.truetype(str(font), 21)
    for index, (picture, title) in enumerate(zip(pictures, ("Reused path after empty seek", "Frame 119 from fresh decode"))):
        x = 12 + index * 492
        with Image.open(picture) as decoded:
            decoded.load()
            if decoded.size != (480, 270):
                raise ValueError(f"Unexpected decoded image dimensions: {decoded.size}")
            sheet.paste(decoded, (x, 12))
        draw.text((x, 294), title, font=label, fill="#e2e8f0")
    sheet.save(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--font", type=Path, required=True)
    parser.add_argument("--ffmpeg", required=True)
    args = parser.parse_args()
    output = args.directory.resolve()
    output.mkdir()
    ffmpeg, ffprobe = binaries(args.ffmpeg)
    old_video = encode(output / "prior", "Prior ending", "#481e26", args.font, ffmpeg, ffprobe)
    current_video = encode(output / "current", "Current ending", "#133747", args.font, ffmpeg, ffprobe)
    stale, actual, evidence = ending_frames(output, old_video, current_video, ffmpeg, ffprobe)
    sheet = output / "ending-frame-comparison.png"
    contact_sheet((stale, actual), sheet, args.font)
    evidence["comparison_png_sha256"] = sha256(sheet)
    write_json(output / "ending-frame-evidence.json", evidence)
    print(json.dumps(evidence))


if __name__ == "__main__":
    main()
