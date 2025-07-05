# Media Functions Library (media_functions.sh)

Specialized functions for media processing, codec configuration, and format validation used by all media conversion scripts.

## Overview

Provides optimized codec configurations, media file validation, and format-specific utilities for professional video and audio processing workflows. Used by all media conversion scripts to ensure consistent quality and compatibility.

## Key Functions

### Codec Configuration

#### `setup_h264_codec()`
```bash
setup_h264_codec quality max_bitrate resolution
```
Configures optimized H.264 encoding parameters.

- **Parameters**: quality (CRF), max_bitrate (kbps), resolution
- **Returns**: Sets global codec variables
- **Features**: Professional presets, bitrate limiting, quality optimization

#### `setup_prores_codec()`
```bash
setup_prores_codec format quality resolution
```
Configures Apple ProRes encoding parameters.

- **Parameters**: format (0-4), quality, resolution
- **Returns**: Sets ProRes-specific variables
- **Formats**: Proxy, LT, Standard, HQ, 4444

### Validation Functions

#### `validate_media_file()`
```bash
validate_media_file "path/to/video.mov"
```
Validates media files and checks format compatibility.

- **Parameters**: file_path
- **Returns**: 0 if valid, 1 if invalid
- **Features**: Format detection, codec verification

#### `validate_sequence_pattern()`
```bash
validate_sequence_pattern "frames_%04d.jpg"
```
Validates image sequence naming patterns.

- **Parameters**: sequence_pattern
- **Returns**: 0 if valid pattern, 1 if invalid
- **Features**: FFmpeg pattern validation

### Format Utilities

#### `parse_sequence_filename()`
```bash
parse_sequence_filename "render_001.exr" base_name frame_number
```
Extracts components from sequence filenames.

- **Parameters**: filename, basename_var, frame_var
- **Features**: Frame number extraction, format identification

#### `get_media_info()`
```bash
get_media_info "video.mov" info_array
```
Retrieves comprehensive media file information.

- **Parameters**: file_path, associative_array
- **Returns**: Populates array with metadata
- **Information**: Duration, resolution, codec, bitrate

## Codec Configurations

### H.264 Settings
```bash
# Professional H.264 configuration
CODEC="libx264"
PRESET="medium"
PROFILE="high"
LEVEL="4.0"
PIXEL_FORMAT="yuv420p"
```

### ProRes Settings
| Format | Profile | Quality | Use Case |
|--------|---------|---------|----------|
| 0 | Proxy | Lower quality | Offline editing |
| 1 | LT | Good quality | Standard editing |
| 2 | Standard | High quality | General production |
| 3 | HQ | Higher quality | Professional delivery |
| 4 | 4444 | Highest quality | VFX, alpha channel |

## Usage Examples

### H.264 Encoding Setup
```bash
#!/bin/bash
source "lib/media_functions.sh"

# Configure H.264 for web delivery
setup_h264_codec 22 8000 "1280x720"

# Use configured settings
ffmpeg -i input.mov \
       -c:v "$H264_CODEC" \
       -crf "$H264_QUALITY" \
       -maxrate "$H264_MAXRATE" \
       -s "$H264_RESOLUTION" \
       output.mp4
```

### ProRes Workflow
```bash
#!/bin/bash
source "lib/media_functions.sh"

# Configure ProRes 4444 for VFX
setup_prores_codec 4 18 "2048x1556"

# Validate input sequence
if validate_sequence_pattern "vfx_%05d.exr"; then
    # Process with ProRes settings
    ffmpeg -i "vfx_%05d.exr" \
           -c:v "$PRORES_CODEC" \
           -profile:v "$PRORES_PROFILE" \
           master.mov
fi
```

### Media Validation
```bash
#!/bin/bash
source "lib/media_functions.sh"

# Validate input media
if validate_media_file "$INPUT_FILE"; then
    echo "✓ Input file validated"
    
    # Get media information
    declare -A media_info
    get_media_info "$INPUT_FILE" media_info
    
    echo "Duration: ${media_info[duration]}"
    echo "Resolution: ${media_info[width]}x${media_info[height]}"
    echo "Codec: ${media_info[codec]}"
else
    echo "✗ Invalid input file"
    exit 1
fi
```

## Quality Presets

### Web Delivery
```bash
# Optimized for web streaming
setup_h264_codec 23 8000 "1920x1080"  # HD web
setup_h264_codec 25 5000 "1280x720"   # HD mobile
setup_h264_codec 28 2000 "854x480"    # SD mobile
```

### Professional Delivery
```bash
# Broadcast/professional quality
setup_h264_codec 18 15000 "1920x1080"  # HD broadcast
setup_h264_codec 16 50000 "3840x2160"  # 4K professional
setup_prores_codec 3 18 "1920x1080"    # ProRes HQ
```

### Archive/Master
```bash
# Highest quality for archival
setup_prores_codec 4 16 "4096x2160"    # ProRes 4444 4K
setup_h264_codec 16 60000 "3840x2160"  # H.264 4K master
```

## Format Support

### Input Formats
- **Video**: MOV, MP4, AVI, MKV, M4V
- **Images**: JPEG, PNG, TIFF, EXR, DPX, BMP
- **Audio**: WAV, AIFF, MP3, M4A, FLAC

### Output Formats
- **H.264**: MP4, MOV containers
- **ProRes**: MOV containers (macOS/professional)
- **WebM**: VP8/VP9 for web delivery

## Error Handling

### Validation Errors
```bash
# File validation with error reporting
if ! validate_media_file "$input"; then
    echo "Error: Invalid media file: $input"
    echo "Supported formats: MOV, MP4, AVI, MKV"
    exit 1
fi
```

### Codec Errors
```bash
# Codec availability checking
if ! command -v ffmpeg >/dev/null 2>&1; then
    echo "Error: FFmpeg not found"
    echo "Install FFmpeg to use media processing functions"
    exit 1
fi
```

## Performance Optimization

### Multi-threading
```bash
# Optimize for available CPU cores
THREAD_COUNT="$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)"
ffmpeg -threads "$THREAD_COUNT" ...
```

### Hardware Acceleration
```bash
# macOS VideoToolbox acceleration
if is_macos && check_videotoolbox_support; then
    CODEC="h264_videotoolbox"
else
    CODEC="libx264"
fi
```

## Integration

### Library Dependencies
```bash
# Required libraries
source "${SCRIPT_DIR}/../lib/common.sh"      # Core functions
source "${SCRIPT_DIR}/../lib/media_functions.sh"  # Media-specific
```

### Cross-Platform Support
- **macOS**: Native ProRes support, VideoToolbox acceleration
- **Linux**: Standard FFmpeg codecs, software encoding
- **Windows**: Compatible via WSL or native FFmpeg

## See Also
- [Common Functions](common.md) - Core utility functions
- [Media Processing Scripts](../overview.md#media-processing) - Scripts using these functions
- [System Functions](system_functions.md) - System information utilities

---

*Script Location: `bash/lib/media_functions.sh`*  
*Author: Alexander Kucera / babylondreams.de*