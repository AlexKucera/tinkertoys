# Images to ProRes Converter (convert_images_to_prores.sh)

Convert image sequences to Apple ProRes format with professional-grade quality settings for broadcast and post-production workflows.

## Overview

The `convert_images_to_prores.sh` script transforms image sequences into Apple ProRes video files, the industry standard for professional video production. It supports all ProRes variants from Proxy to 4444, providing optimal quality for editing, color grading, and broadcast delivery.

## Usage

```bash
convert_images_to_prores.sh <path_to_file> [resolution] [framerate] [quality] [format]
```

### Arguments

| Argument | Type | Description | Default |
|----------|------|-------------|---------|
| `path_to_file` | Required | Path to input image sequence | - |
| `resolution` | Optional | Output resolution | 1920x1080 |
| `framerate` | Optional | Frame rate in fps | 25 |
| `quality` | Optional | Quality setting | 20 |
| `format` | Optional | ProRes format (0-4) | 4 (4444) |

### ProRes Formats

| Value | Format | Description | Use Case |
|-------|--------|-------------|----------|
| 0 | Proxy | Low resolution/bitrate | Offline editing |
| 1 | LT | Light compression | Standard editing |
| 2 | Standard | Balanced quality/size | General production |
| 3 | HQ | High quality | Professional delivery |
| 4 | 4444 | Highest quality + alpha | VFX, color grading |

## Examples

### Professional Workflows
```bash
# VFX sequence to ProRes 4444
./convert_images_to_prores.sh vfx_%05d.exr 2048x1556 24 18 4

# Animation to ProRes HQ
./convert_images_to_prores.sh anim_%04d.png 1920x1080 24 20 3

# Proxy for offline editing
./convert_images_to_prores.sh dailies_%04d.jpg 1920x1080 25 22 0
```

### Broadcast Production
```bash
# Broadcast standard (ProRes HQ)
./convert_images_to_prores.sh sequence_%04d.tiff 1920x1080 25 18 3

# 4K production (ProRes 4444)
./convert_images_to_prores.sh frames_%05d.dpx 3840x2160 24 16 4
```

## See Also
- [Images to H.264 Converter](convert_images_to_h264.md) - Web delivery alternative
- [Media Functions](../lib/media_functions.md) - ProRes encoding setup
- [Media Processing Overview](../overview.md#media-processing) - All media tools

---

*Script Location: `bash/media/convert_images_to_prores.sh`*  
*Author: Alexander Kucera / babylondreams.de*