# Stereo to Mono Audio Split (split_stereo_to_mono.sh)

Split stereo audio files into separate mono channel files with lossless quality preservation.

## Overview

Separates stereo audio files into individual left and right channel mono files using Apple Lossless format. Essential for audio post-production, music production, and broadcast workflows where channel separation is required.

## Usage

```bash
split_stereo_to_mono.sh <path_to_file>
```

### Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `path_to_file` | Required | Path to input stereo audio file |

## Features

- **Lossless Quality**: Uses Apple Lossless format for quality preservation
- **Channel Separation**: Creates separate left and right channel files
- **Format Support**: Handles WAV, AIFF, MP3, and other common audio formats
- **Professional Output**: Apple Lossless suitable for further processing

## Examples

```bash
# Split music recording
./split_stereo_to_mono.sh song_stereo.wav

# Process podcast audio
./split_stereo_to_mono.sh interview.aiff

# Separate dialogue tracks
./split_stereo_to_mono.sh dialogue_stereo.mp3
```

## Output Files
- `filename_left.m4a` - Left channel in Apple Lossless
- `filename_right.m4a` - Right channel in Apple Lossless

## Use Cases
- **Music Production**: Separate instruments recorded on different channels
- **Podcast Production**: Split host and guest recordings
- **Audio Restoration**: Process channels independently
- **Broadcast**: Create separate mono feeds for different outputs

## See Also
- [Media Functions](../lib/media_functions.md) - Audio processing utilities
- [Media Processing Overview](../overview.md#media-processing) - All media tools

---

*Script Location: `bash/media/split_stereo_to_mono.sh`*  
*Author: Alexander Kucera / babylondreams.de*