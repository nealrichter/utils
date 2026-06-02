# cut_game.py

Cut clips from a game video (local file or YouTube) and stitch them into a highlight reel with optional annotated interstitial cards.

## Usage

```bash
./cut_game.py -f <timestamps_file> -o <output> [--annotate] [-d <card_video>] [-g <game_video>]
```

### Options

| Flag | Description |
|------|-------------|
| `-g, --game` | Input game video file (not needed if `#{url}` is in timestamps file) |
| `-f, --file` | Timestamps file (see format below) |
| `-c, --clip` | Inline clip ranges: `00:13:55,00:14:35 00:25:30,00:25:50` |
| `-o, --output` | Output filename (default: `highlight_reel.mp4`) |
| `-d, --card` | Video file to prepend/append as title card |
| `--annotate` | Generate interstitial cards before each clip with play info |

## Timestamps File Format

```
#{logo:murray_spartans_logo.png}
#{title} Game: Murray 35 @ Woods Cross 55
#{date} Dec 2, 2025
#{subtitle} Brooklyn Richter (#35): 25 PTS | 8 REB | 2 STL | 1 BLK
#{url}https://www.youtube.com/watch?v=XXXXXXXXXXX

00:14:05,00:14:13 #{play}1 make! [bucket]
00:16:30, ~6 #{play}2 Rebound [strong]
#00:25:30,00:25:40 #commented out - won't be included
```

### Metadata Tags (comment-only lines)

| Tag | Purpose |
|-----|---------|
| `#{title}` | Game title shown on start/end card |
| `#{date}` | Game date shown on start/end card |
| `#{subtitle}` | Stat line shown on start/end card |
| `#{logo:filename}` | Logo image file for cards (relative to script dir) |
| `#{url}` | YouTube URL — clips extracted via yt-dlp instead of local file |

### Clip Time Formats

**Standard:** `START,END` — e.g. `00:14:05,00:14:13`

**Center-offset:** `CENTER, ~N` — extracts CENTER ± N seconds
- `00:16:30, ~6` → extracts from 00:16:24 to 00:16:36

### Clip Lines

Format: `TIME_SPEC #{play}N description [emoji]`

- Lines starting with `#` are ignored (commented out)
- Inline `#comments` after timestamps become play descriptions
- `#{play}N` prefix is stripped; the number and description are shown on interstitial cards

### Emoji Triggers

Use `[word]` or `[emoticon]` in clip comments to display an emoji on the interstitial card.

| Trigger | Aliases | Emoji |
|---------|---------|-------|
| `[bucket]` | | 🏀 |
| `[flex]` | `[strong]` | 💪 |
| `[fire]` | | 🔥 |
| `[100]` | | 💯 |
| `[swish]` | | 🎯 |
| `[check]` | | ✅ |
| `[happy]` | `[:)]` | 😊 |
| `[sad]` | `[:(]` | 😞 |
| `[cry]` | `[;-(]` | 😢 |
| `[mad]` | `[angry]`, `[>:(]` | 😡 |
| `[meh]` | `[:/]` | 😕 |
| `[grin]` | `[:D]` | 😁 |
| `[shock]` | `[:O]` | 😮 |
| `[tongue]` | `[:P]` | 😛 |
| `[lol]` | `[XD]` | 😆 |
| `[wink]` | `[;)]` | 😉 |
| `[love]` | `[<3]` | ❤️ |
| `[question]` | | ❓ |

Plain text emoticons (without brackets) also work as a fallback: `:)`, `:(`, `:/`, `>:(`, `;-(`, `:D`, `:O`, `:P`, `XD`, `<3`, `!!`, `???`

## Examples

From a local game file:
```bash
./cut_game.py -g game.mp4 -f timestamps.txt -o highlights.mp4 --annotate
```

From a YouTube video (uses `#{url}` in timestamps file):
```bash
./cut_game.py -f Storm_WhyNot_NewOrleans_516_timestamps.txt -o Storm_WhyNot_NO.mp4 --annotate
```

With inline clips:
```bash
./cut_game.py -g game.mp4 -c 00:13:55,00:14:35 00:25:30,00:25:50
```

With a pre-made title card:
```bash
./cut_game.py -g game.mp4 -f timestamps.txt -o highlights.mp4 -d card.mp4
```

## YouTube Mode

When `#{url}` is present in the timestamps file:
- Clips are extracted using `yt-dlp` with H.264 codec
- Intermediate clips are saved to `clips_segments/{base_name}_clip_N.mp4`
- A concat manifest is written to `clips_segments/{base_name}.txt`
- No `-g` flag is needed

## Requirements

- `ffmpeg` (with libx264 and aac)
- `yt-dlp` (only for YouTube mode)
- Python 3.11 with Pillow (`pip3.11 install Pillow`)
- Bangers font at `~/Library/Fonts/Bangers-Regular.ttf` (for `--annotate`)
- Logo image in the same directory as the script (for `--annotate` with `#{logo:}`)

## Notes

- `--annotate` auto-generates a start/end title card from metadata tags (overrides `-d`)
- Local clips are re-encoded (H.264 Main, CRF 18) for clean cuts, then concatenated with `-c copy`
- Temp files are created in a system temp directory and cleaned up automatically
- `clips_segments/` files persist for reuse
