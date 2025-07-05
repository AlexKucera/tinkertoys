# Movie to H.264 Converter (convert_movie_to_h264.sh)

Convert video files to H.264 format with optimized settings for web delivery, streaming, and distribution.

## Overview

Convert existing video files to H.264 format using professional encoding settings. Ideal for creating web-optimized versions, streaming content, and cross-platform compatible video files.

## Usage

```bash
convert_movie_to_h264.sh <path_to_file> [resolution] [quality] [max_bitrate]
```

### Arguments

| Argument | Type | Description | Default |
|----------|------|-------------|---------|
| `path_to_file` | Required | Path to input video file | - |
| `resolution` | Optional | Output resolution | 1920x1080 |
| `quality` | Optional | Quality setting (CRF) | 20 |
| `max_bitrate` | Optional | Maximum bitrate in kbps | 10000 |

## Examples

### Basic Conversion
```bash
# Convert with default settings
./convert_movie_to_h264.sh input.mov

# Web-optimized version
./convert_movie_to_h264.sh source.avi 1280x720 22 8000

# High quality for distribution
./convert_movie_to_h264.sh master.mov 1920x1080 18 15000
```

### Batch Processing
```bash
# Convert all MOV files in directory
for file in *.mov; do
    ./convert_movie_to_h264.sh "$file" 1920x1080 20 12000
done
```

## Bitrate Guidelines

Same as [Images to H.264](convert_images_to_h264.md#bitrate-guidelines) - optimized for different resolutions and use cases.

## See Also
- [Images to H.264 Converter](convert_images_to_h264.md) - Image sequence version
- [Movie to ProRes Converter](convert_movie_to_prores.md) - Professional alternative
- [Movie to Web Converter](movie_to_web.md) - Multi-format web output

---

*Script Location: `bash/media/convert_movie_to_h264.sh`*  
*Author: Alexander Kucera / babylondreams.de*