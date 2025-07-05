# Images to H.264 Converter (convert_images_to_h264.sh)

Convert image sequences to H.264 video format with professional encoding settings and configurable quality parameters.

## Overview

The `convert_images_to_h264.sh` script transforms image sequences into high-quality H.264 video files using FFmpeg. It provides professional-grade encoding options with optimized settings for different resolution and quality requirements, making it ideal for animation, time-lapse, and video production workflows.

## Usage

```bash
convert_images_to_h264.sh <path_to_file> [resolution] [framerate] [quality] [max_bitrate]
```

### Arguments

| Argument | Type | Description | Default |
|----------|------|-------------|---------|
| `path_to_file` | Required | Path to input image sequence or video file | - |
| `resolution` | Optional | Output resolution (e.g., 1920x1080) | 1920x1080 |
| `framerate` | Optional | Frame rate in fps | 25 |
| `quality` | Optional | Quality setting (lower = better quality) | 20 |
| `max_bitrate` | Optional | Maximum bitrate in kbps | 10000 |

### Options

| Option | Description |
|--------|-------------|
| `-h, --help` | Show help message and exit |

## Examples

### Basic Image Sequence Conversion
```bash
# Convert numbered image sequence
./convert_images_to_h264.sh sequence.%04d.jpg

# Convert with default settings (1920x1080, 25fps, quality 20)
./convert_images_to_h264.sh frame_%03d.png
```

### Custom Quality Settings
```bash
# High quality for professional use
./convert_images_to_h264.sh images.%04d.tiff 1920x1080 25 18 15000

# Web-optimized version
./convert_images_to_h264.sh sequence.%04d.jpg 1280x720 30 22 8000

# 4K high-quality encode
./convert_images_to_h264.sh frames.%05d.exr 3840x2160 24 16 50000
```

### Different Input Formats
```bash
# From TIFF sequence (professional photography)
./convert_images_to_h264.sh photos_%04d.tiff 1920x1080 24 18 12000

# From PNG sequence (animation/graphics)
./convert_images_to_h264.sh animation_%03d.png 1920x1080 30 20 10000

# From EXR sequence (VFX/rendering)
./convert_images_to_h264.sh render_%05d.exr 2048x1556 24 16 20000
```

## Features

### 🎥 Professional Encoding
- **H.264 Codec**: Industry-standard compression with excellent quality/size ratio
- **Configurable Quality**: CRF-based quality control for consistent results
- **Bitrate Control**: Maximum bitrate limiting for streaming/delivery requirements
- **Frame Rate Flexibility**: Support for any frame rate from 1fps to 120fps

### 📐 Resolution Support
- **Standard Formats**: HD (1920x1080), 4K (3840x2160), 2K (2048x1556)
- **Custom Resolutions**: Any resolution supported by FFmpeg
- **Aspect Ratio Preservation**: Maintains proper aspect ratios
- **Scaling Quality**: High-quality scaling algorithms

### 🛠️ Advanced Options
- **Input Validation**: Comprehensive validation of input files and parameters
- **Progress Monitoring**: Real-time encoding progress feedback
- **Error Handling**: Robust error detection and reporting
- **Shared Library Integration**: Uses optimized codec setup functions

## Bitrate Guidelines

| Resolution | Recommended Bitrate Range | Use Case |
|------------|---------------------------|----------|
| SD (480p) | 2,000 - 5,000 kbps | Web delivery, mobile |
| 720p HD | 5,000 - 10,000 kbps | Standard HD, streaming |
| 1080p HD | 10,000 - 20,000 kbps | Full HD, broadcast |
| 2K | 20,000 - 30,000 kbps | Cinema, professional |
| 4K | 30,000 - 60,000 kbps | Ultra HD, premium content |

## Quality Settings

| CRF Value | Quality Level | Use Case |
|-----------|---------------|----------|
| 16-18 | Excellent | Professional/broadcast |
| 20-22 | High | Standard production |
| 23-25 | Good | Web delivery |
| 26-28 | Acceptable | High compression needs |

## How It Works

### Processing Pipeline
1. **Input Validation**: Verifies image sequence files exist and are accessible
2. **Parameter Setup**: Configures encoding parameters based on input arguments
3. **Codec Configuration**: Sets up H.264 encoder with optimized settings
4. **FFmpeg Execution**: Runs FFmpeg with constructed command line
5. **Progress Monitoring**: Provides real-time feedback during encoding
6. **Output Verification**: Confirms successful completion and output file creation

### Encoding Configuration
The script uses optimized H.264 settings:
- **Profile**: High profile for maximum compatibility
- **Preset**: Balanced preset for quality vs. speed
- **Rate Control**: CRF (Constant Rate Factor) for consistent quality
- **Bitrate Limiting**: Maximum bitrate caps for delivery requirements

## Input Formats

### Supported Image Formats
- **JPEG/JPG**: Standard photography, compressed images
- **PNG**: Lossless graphics, transparency support
- **TIFF**: Professional photography, high bit depth
- **EXR**: VFX and rendering, HDR images
- **DPX**: Film/broadcast industry standard
- **BMP**: Windows bitmap format

### Sequence Naming Patterns
```bash
# Common patterns (use %d for frame numbers)
frame_%04d.jpg     # frame_0001.jpg, frame_0002.jpg...
image_%03d.png     # image_001.png, image_002.png...
render_%05d.exr    # render_00001.exr, render_00002.exr...
```

## Configuration

### Environment Variables
No environment variables required. All configuration through command-line arguments.

### FFmpeg Dependencies
- **FFmpeg**: Required with H.264 encoder support
- **x264**: H.264 encoding library (usually included with FFmpeg)

## Integration

### Animation Workflows
```bash
#!/bin/bash
# Animation rendering pipeline
SEQUENCE_DIR="~/renders/animation"
OUTPUT_DIR="~/output/videos"

# Multiple quality versions
./convert_images_to_h264.sh "$SEQUENCE_DIR/frame_%04d.png" 1920x1080 24 18 15000
mv output.mp4 "$OUTPUT_DIR/animation_high.mp4"

./convert_images_to_h264.sh "$SEQUENCE_DIR/frame_%04d.png" 1280x720 24 22 8000
mv output.mp4 "$OUTPUT_DIR/animation_web.mp4"
```

### Batch Processing
```bash
#!/bin/bash
# Process multiple sequences
for sequence in ~/sequences/*.%04d.jpg; do
    base_name=$(basename "$sequence" .%04d.jpg)
    ./convert_images_to_h264.sh "$sequence" 1920x1080 25 20 12000
    mv output.mp4 "~/videos/${base_name}_h264.mp4"
done
```

### Time-lapse Creation
```bash
# Time-lapse from photos
./convert_images_to_h264.sh timelapse_%04d.jpg 1920x1080 30 20 15000

# Hyperlapse with motion blur
./convert_images_to_h264.sh hyperlapse_%05d.tiff 3840x2160 60 18 40000
```

## Best Practices

### Pre-Processing
1. **Consistent Naming**: Use consistent frame numbering (e.g., %04d)
2. **Frame Rate Planning**: Choose appropriate frame rate for content type
3. **Resolution Decisions**: Match output resolution to intended use
4. **Quality Testing**: Test quality settings on a short sequence first

### Encoding Optimization
1. **Quality vs. Size**: Balance CRF and bitrate for optimal results
2. **Target Platform**: Consider playback device capabilities
3. **Delivery Method**: Optimize for streaming vs. download
4. **Storage Constraints**: Adjust settings based on storage limitations

### Quality Control
1. **Preview Encoding**: Test settings on a small sample first
2. **Visual Inspection**: Always review encoded output
3. **Bitrate Analysis**: Monitor actual vs. maximum bitrate usage
4. **Compatibility Testing**: Verify playback on target devices

## Troubleshooting

### Common Issues

**FFmpeg Not Found**
- Install FFmpeg with H.264 support
- Ensure FFmpeg is in system PATH
- Verify x264 encoder availability

**Input File Errors**
- Check image sequence naming pattern matches
- Verify all sequence files exist and are readable
- Ensure image format is supported by FFmpeg

**Quality Issues**
- Lower CRF value for better quality (but larger files)
- Increase maximum bitrate for complex content
- Consider different preset for speed vs. quality trade-off

**Performance Problems**
- Use hardware acceleration if available
- Adjust FFmpeg preset for faster encoding
- Process smaller batches for memory management

## Technical Details

### Dependencies
- **FFmpeg**: With H.264/x264 encoder support
- **Shared Libraries**: Uses media_functions.sh for codec setup
- **Common Functions**: Input validation and error handling

### Encoding Command Structure
```bash
ffmpeg -r $FRAMERATE -i "$INPUT_PATTERN" \
       -c:v libx264 -crf $QUALITY \
       -maxrate ${MAX_BITRATE}k -bufsize $((MAX_BITRATE * 2))k \
       -s $RESOLUTION -pix_fmt yuv420p \
       "$OUTPUT_FILE"
```

### Security Considerations
- **Input Validation**: All parameters validated before use
- **Path Safety**: No arbitrary command construction
- **File Validation**: Input files verified before processing

## See Also

- [Images to ProRes Converter](convert_images_to_prores.md) - Professional codec alternative
- [Movie to H.264 Converter](convert_movie_to_h264.md) - Video file input version
- [Media Functions](../lib/media_functions.md) - Shared encoding functions
- [Media Processing Overview](../overview.md#media-processing) - All media tools

---

*Script Location: `bash/media/convert_images_to_h264.sh`*  
*Author: Alexander Kucera / babylondreams.de*  
*Copyright: 2012 BabylonDreams. All rights reserved.*