# Movie to Web Converter (movie_to_web.sh)

Convert video files to web-optimized formats (MP4 and WebM) for maximum browser compatibility and streaming performance.

## Overview

Creates web-optimized video files in both MP4 (H.264) and WebM formats, ensuring maximum compatibility across all browsers and devices. Optimized for web delivery with balanced quality and file size.

## Usage

```bash
movie_to_web.sh <path_to_file>
```

### Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `path_to_file` | Required | Path to input video file |

## Features

- **Dual Format Output**: Creates both MP4 and WebM versions
- **Web Optimization**: Settings optimized for web streaming
- **Browser Compatibility**: Ensures playback across all major browsers
- **Automatic Quality**: Pre-configured quality settings for web delivery

## Examples

```bash
# Convert for web deployment
./movie_to_web.sh promotional_video.mov

# Process training videos
./movie_to_web.sh training_session.avi

# Convert product demos
./movie_to_web.sh product_demo.mp4
```

## Output Files
- `filename_web.mp4` - H.264 version for broad compatibility
- `filename_web.webm` - WebM version for modern browsers

## See Also
- [Movie to H.264 Converter](convert_movie_to_h264.md) - H.264-only output
- [Media Processing Overview](../overview.md#media-processing) - All media tools

---

*Script Location: `bash/media/movie_to_web.sh`*  
*Author: Alexander Kucera / babylondreams.de*