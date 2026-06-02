#!/usr/bin/env python3.11
"""Cut clips from a game video and stitch into a highlight reel."""
import argparse
import subprocess
import os
import tempfile

parser = argparse.ArgumentParser(description="Cut clips from a game video and merge into a highlight reel.")
parser.add_argument("-g", "--game", help="Input game video file (not needed if #{url} is in timestamps file)")
parser.add_argument("-c", "--clip", nargs="+", help="Clip time ranges as START,END (e.g. 00:13:55,00:14:35)")
parser.add_argument("-f", "--file", help="File with clip timestamps, one START,END per line")
parser.add_argument("-o", "--output", default="highlight_reel.mp4", help="Output filename (default: highlight_reel.mp4)")
parser.add_argument("-d", "--card", help="Video file to prepend and append as a title card")
parser.add_argument("--annotate", action="store_true", help="Insert a clip number card before each clip")
args = parser.parse_args()

timestamps = []
metadata = {"title": "", "subtitle": "", "date": "", "logo": "", "url": ""}

def time_to_secs(t):
    parts = t.strip().split(":")
    return int(parts[0])*3600 + int(parts[1])*60 + float(parts[2])

def secs_to_time(s):
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    sec = s % 60
    return f"{h:02d}:{m:02d}:{sec:05.2f}"

if args.file:
    with open(args.file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Parse metadata from comment-only lines
            if line.startswith("#"):
                if "#{title}" in line:
                    metadata["title"] = line.split("#{title}")[1].strip()
                elif "#{subtitle}" in line:
                    metadata["subtitle"] = line.split("#{subtitle}")[1].strip()
                elif "#{date}" in line:
                    metadata["date"] = line.split("#{date}")[1].strip()
                elif "#{logo:" in line:
                    metadata["logo"] = line.split("#{logo:")[1].rstrip("} ").strip()
                elif "#{url}" in line:
                    metadata["url"] = line.split("#{url}")[1].strip()
                continue
            comment = ""
            if "#" in line:
                comment = line.split("#", 1)[1].strip()
                # Strip #{play}N tag, keep description
                if comment.startswith("{play}"):
                    comment = comment.split("}", 1)[1].strip()
                    # Remove leading number if present
                    parts = comment.split(" ", 1)
                    if parts[0].isdigit() and len(parts) > 1:
                        comment = parts[1]
            line = line.split("#")[0].strip()
            if not line:
                continue
            # Handle center-offset format: "00:16:30, ~6"
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 2 and parts[1].startswith("~"):
                center = time_to_secs(parts[0])
                offset = float(parts[1][1:])
                start = secs_to_time(center - offset)
                end = secs_to_time(center + offset)
                timestamps.append((start, end, comment))
            else:
                # Standard format: START,END or START-END
                flat = line.replace("-", ",").split(",")
                if len(flat) >= 2:
                    timestamps.append((flat[0].strip(), flat[1].strip(), comment))
elif args.clip:
    for c in args.clip:
        sep = "," if "," in c else "-"
        parts = c.split(sep, 1)
        if len(parts) != 2 or not parts[1]:
            print(f"Error: invalid clip format '{c}', expected START,END (e.g. 00:13:55,00:14:35)")
            exit(1)
        timestamps.append((parts[0], parts[1], ""))
else:
    # Default timestamps (Murray vs Woods Cross Dec 2)
    timestamps = [
        ("00:13:55", "00:14:35", ""),
        ("00:14:45", "00:15:15", ""),
        ("00:15:30", "00:15:59", ""),
        ("00:25:30", "00:25:50", ""),
        ("00:29:20", "00:29:40", ""),
        ("00:35:15", "00:35:35", ""),
        ("00:48:20", "00:48:39", ""),
        ("00:51:40", "00:51:59", ""),
        ("00:52:20", "00:52:39", ""),
        ("00:54:46", "00:55:25", ""),
        ("01:01:15", "01:01:35", ""),
        ("01:14:15", "01:14:35", ""),
    ]

if not timestamps:
    print("No clips specified. Use -c, -f, or run without either for defaults.")
    exit(1)

if not args.game and not metadata["url"]:
    print("Error: provide -g <game_file> or include #{url} in timestamps file.")
    exit(1)

tmpdir = tempfile.mkdtemp(prefix="cut_game_")
temp_files = []
list_file = os.path.join(tmpdir, "mylist.txt")

# Generate start/end card from metadata if --debug and we have metadata
if args.annotate and (metadata["title"] or metadata["subtitle"]):
    from PIL import Image, ImageDraw, ImageFont
    bangers = os.path.expanduser("~/Library/Fonts/Bangers-Regular.ttf")
    script_dir = os.path.dirname(os.path.abspath(__file__))

    def make_title_card(out_path):
        img = Image.new("RGB", (1920, 1080), "black")
        draw = ImageDraw.Draw(img)
        try:
            font_xl = ImageFont.truetype(bangers, 110)
            font_lg = ImageFont.truetype(bangers, 88)
            font_md = ImageFont.truetype(bangers, 68)
            font_sm = ImageFont.truetype(bangers, 52)
        except:
            font_xl = ImageFont.load_default()
            font_lg = font_xl
            font_md = font_xl
            font_sm = font_xl
        logo_path = os.path.join(script_dir, metadata["logo"]) if metadata["logo"] else ""
        if logo_path and os.path.exists(logo_path):
            logo = Image.open(logo_path).convert("RGBA")
            logo.thumbnail((250, 250))
            img.paste(logo, ((1920 - logo.width) // 2, 30), logo)
        draw.text((960, 360), "#35 Brooklyn Richter", fill="white", font=font_xl, anchor="mm")
        if metadata["title"]:
            draw.text((960, 490), metadata["title"], fill="lime", font=font_md, anchor="mm")
        if metadata["date"]:
            draw.text((960, 580), metadata["date"], fill="#cccccc", font=font_sm, anchor="mm")
        if metadata["subtitle"]:
            draw.text((960, 700), metadata["subtitle"], fill="yellow", font=font_lg, anchor="mm")
        img.save(out_path)

    card_png = os.path.join(tmpdir, "title_card.png")
    make_title_card(card_png)
    card_mp4 = os.path.join(tmpdir, "title_card.mp4")
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-loop", "1", "-i", card_png,
        "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
        "-t", "3", "-c:v", "libx264", "-profile:v", "main", "-crf", "18", "-pix_fmt", "yuv420p",
        "-r", "30", "-c:a", "aac", "-b:a", "128k", "-shortest",
        card_mp4
    ])
    # Override the card argument with our generated one
    args.card = card_mp4

for i, (start, end, comment) in enumerate(timestamps):
    if args.annotate:
        count_file = os.path.join(tmpdir, f"count_{i}.mp4")
        card_png = os.path.join(tmpdir, f"count_{i}.png")
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 255))
        draw = ImageDraw.Draw(img)
        try:
            bangers = os.path.expanduser("~/Library/Fonts/Bangers-Regular.ttf")
            font_num = ImageFont.truetype(bangers, 280)
            font_name = ImageFont.truetype(bangers, 100)
            font_comment = ImageFont.truetype(bangers, 80)
        except:
            font_num = ImageFont.load_default()
            font_name = font_num
            font_comment = font_num
        # Logo
        script_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(script_dir, metadata["logo"]) if metadata["logo"] else ""
        if logo_path and os.path.exists(logo_path):
            logo = Image.open(logo_path).convert("RGBA")
            logo.thumbnail((250, 250))
            lx = (1920 - logo.width) // 2
            img.paste(logo, (lx, 50), logo)
        draw.text((960, 350), f"Play {i+1}", fill="lime", font=font_num, anchor="mm")
        draw.text((960, 580), "#35 Brooklyn Richter", fill="white", font=font_name, anchor="mm")
        if comment:
            # Replace text emoticons with emoji (bracket tags checked first)
            bracket_map = {
                "[bucket]": "🏀", "[flex]": "💪", "[strong]": "💪", "[fire]": "🔥",
                "[100]": "💯", "[swish]": "🎯", "[check]": "✅",
            }
            emoticon_map = {
                ";-(": "😢", ":-(": "😞", ":)": "😊", ":(": "😞",
                ";)": "😉", ":D": "😁", ":/": "😕", ">:(": "😡",
                ":P": "😛", "<3": "❤️", ":O": "😮", "XD": "😆",
                "!!": "🔥", "???": "❓",
            }
            display_comment = comment
            emoji_found = ""
            for emoticon, emoji in bracket_map.items():
                if emoticon in display_comment:
                    emoji_found = emoji
                    display_comment = display_comment.replace(emoticon, "").strip()
                    break
            if not emoji_found:
                for emoticon, emoji in emoticon_map.items():
                    if emoticon in display_comment:
                        emoji_found = emoji
                        display_comment = display_comment.replace(emoticon, "").strip()
                        break
            # Clean up leftover emoticon text
            for e in list(bracket_map) + list(emoticon_map):
                display_comment = display_comment.replace(e, "")
            display_comment = display_comment.strip()
            draw.text((960, 730), display_comment, fill="yellow", font=font_comment, anchor="mm")
            if emoji_found:
                try:
                    emoji_font = ImageFont.truetype("/System/Library/Fonts/Apple Color Emoji.ttc", 160)
                    draw.text((960, 880), emoji_found, font=emoji_font, anchor="mm", embedded_color=True)
                except:
                    pass
        img = img.convert("RGB")
        img.save(card_png)
        subprocess.run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-loop", "1", "-i", card_png,
            "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
            "-t", "1", "-c:v", "libx264", "-profile:v", "main", "-crf", "18", "-pix_fmt", "yuv420p",
            "-r", "30", "-c:a", "aac", "-b:a", "128k", "-shortest",
            count_file
        ])
        temp_files.append(count_file)
    temp_filename = os.path.join(tmpdir, f"clip_{i}.mp4")
    temp_files.append(temp_filename)
    duration = time_to_secs(end) - time_to_secs(start)
    print(f"Extracting Clip {i+1}: {start} to {end} ({duration:.0f}s)")
    if metadata["url"]:
        # Use yt-dlp to extract from YouTube
        script_dir = os.path.dirname(os.path.abspath(__file__))
        clips_dir = os.path.join(script_dir, "clips_segments")
        os.makedirs(clips_dir, exist_ok=True)
        # Derive base name from timestamps filename
        base_name = os.path.splitext(os.path.basename(args.file))[0] if args.file else "clip"
        clip_raw = os.path.join(clips_dir, f"{base_name}_clip_{i+1}_raw.mp4")
        clip_file = os.path.join(clips_dir, f"{base_name}_clip_{i+1}.mp4")
        section = f"*{start}-{end}"
        subprocess.run([
            "yt-dlp", "--download-sections", section,
            "-f", "bv*+ba/b", "-S", "vcodec:h264",
            "--merge-output-format", "mp4",
            "--force-overwrites",
            "-o", clip_raw, metadata["url"]
        ])
        # Re-encode to normalize fps/resolution/audio for clean concat
        subprocess.run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-i", clip_raw,
            "-c:v", "libx264", "-profile:v", "main", "-crf", "18", "-pix_fmt", "yuv420p",
            "-r", "30", "-c:a", "aac", "-b:a", "128k", "-ar", "48000",
            clip_file
        ])
        os.remove(clip_raw)
        # Copy to temp location for concat
        import shutil as _shutil
        _shutil.copy2(clip_file, temp_filename)
    else:
        subprocess.run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-ss", start, "-to", end,
            "-i", args.game,
            "-c:v", "libx264", "-profile:v", "main", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "128k",
            temp_filename
        ])

with open(list_file, "w") as f:
    if args.card:
        f.write(f"file '{os.path.abspath(args.card)}'\n")
    for temp_file in temp_files:
        f.write(f"file '{temp_file}'\n")
    if args.card:
        f.write(f"file '{os.path.abspath(args.card)}'\n")

# Also write a manifest in clips_segments/ if using yt-dlp
if metadata["url"] and args.file:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    clips_dir = os.path.join(script_dir, "clips_segments")
    base_name = os.path.splitext(os.path.basename(args.file))[0]
    manifest_path = os.path.join(clips_dir, f"{base_name}.txt")
    with open(manifest_path, "w") as mf:
        for temp_file in temp_files:
            mf.write(f"file '{os.path.abspath(temp_file)}'\n")
    print(f"Manifest written: {manifest_path}")

print("Stitching clips together...")
subprocess.run([
    "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
    "-f", "concat", "-safe", "0",
    "-i", list_file,
    "-c", "copy", args.output
])

import shutil
shutil.rmtree(tmpdir)

print(f"Done: {args.output}")
