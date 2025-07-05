# Movie to ProRes Converter (convert_movie_to_prores.sh)

Convert video files to Apple ProRes format for professional post-production and broadcast workflows.

## Usage

```bash
convert_movie_to_prores.sh <path_to_file> [resolution] [framerate] [quality] [format]
```

### ProRes Formats
- **0**: Proxy - Offline editing
- **1**: LT - Standard editing  
- **2**: Standard - General production
- **3**: HQ - Professional delivery
- **4**: 4444 - VFX, color grading (default)

## Examples

```bash
# Convert to ProRes 4444 for color grading
./convert_movie_to_prores.sh source.mov 1920x1080 25 18 4

# Create proxy for offline editing
./convert_movie_to_prores.sh master.avi 1920x1080 25 22 0

# Professional delivery format
./convert_movie_to_prores.sh final.mp4 1920x1080 24 18 3
```

## See Also
- [Images to ProRes Converter](convert_images_to_prores.md) - Image sequence version
- [Movie to H.264 Converter](convert_movie_to_h264.md) - Web delivery alternative

---

*Script Location: `bash/media/convert_movie_to_prores.sh`*  
*Author: Alexander Kucera / babylondreams.de*