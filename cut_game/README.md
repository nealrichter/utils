# cut_game.py

Cut clips from a game video and stitch them into a highlight reel with optional annotated interstitial cards.

## Usage

```bash
./cut_game.py -g <game_video> -f <timestamps_file> -o <output> [--annotate] [-d <card_video>]
```

### Options

| Flag | Description |
|------|-------------|
| `-g, --game` | Input game video file (required) |
| `-f, --file` | Timestamps file (see format below) |
| `-c, --clip` | Inline clip ranges: `00:13:55,00:14:35 00:25:30,00:25:50` |
| `-o, --output` | Output filename (default: `highlight_reel.mp4`) |
| `-d, --card` | Video file to prepend/append as title card |
| `--annotate` | Generate interstitial cards before each clip with play info |

## Timestamps File Format

```
#{title} Game: Murray 35 @ Woods Cross 55
#{date} Dec 2, 2025
#{subtitle} Brooklyn Richter (#35): 25 PTS | 8 REB | 2 STL | 1 BLK

00:14:05,00:14:13 #{play}1 make! [bucket]
00:15:41,00:15:57 #{play}2 defense! [strong]
#00:25:30,00:25:40 #commented out - won't be included
00:32:20,00:32:32 #{play}4 rebound & putback! [fire]
```

### Metadata Tags (comment-only lines)

| Tag | Purpose |
|-----|---------|
| `#{title}` | Game title shown on start/end card |
| `#{date}` | Game date shown on start/end card |
| `#{subtitle}` | Stat line shown on start/end card |

### Clip Lines

Format: `START,END #{play}N description [emoji]`

- Lines starting with `#` are ignored (commented out)
- Inline `#comments` after timestamps become play descriptions
- `#{play}N` prefix is stripped; the number and description are shown on interstitial cards

### Emoji Triggers

| Trigger | Emoji |
|---------|-------|
| `[bucket]` | 🏀 |
| `[flex]` / `[strong]` | 💪 |
| `[fire]` / `!!` | 🔥 |
| `[100]` | 💯 |
| `[swish]` | 🎯 |
| `[check]` | ✅ |
| `:)` | 😊 |
| `:(` / `:-(` | 😞 |
| `;-(` | 😢 |
| `>:(` | 😡 |
| `:D` | 😁 |
| `:/` | 😕 |
| `:O` | 😮 |
| `<3` | ❤️ |

## Examples

Basic clip extraction:
```bash
./cut_game.py -g game.mp4 -c 00:13:55,00:14:35 00:25:30,00:25:50
```

Full annotated highlight reel:
```bash
./cut_game.py -g game.mp4 -f timestamps.txt -o highlights.mp4 --annotate
```

With a pre-made title card:
```bash
./cut_game.py -g game.mp4 -f timestamps.txt -o highlights.mp4 -d card.mp4
```

## Requirements

- `ffmpeg` (with libx264 and aac)
- Python 3.11 with Pillow (`pip3.11 install Pillow`)
- Bangers font at `~/Library/Fonts/Bangers-Regular.ttf`
- `murray_spartans_logo.png` in the same directory (for interstitial cards)

## Notes

- `--annotate` auto-generates a start/end title card from metadata tags (overrides `-d`)
- Clips are re-encoded (H.264 Main, CRF 18) for clean cuts, then concatenated with `-c copy`
- Temp files are created in a system temp directory and cleaned up automatically
