# convert_psd_to_exr.py

Convert Photoshop PSD files to OpenEXR format while preserving layer structure and names, with secure subprocess handling and comprehensive error management.

## Overview

convert_psd_to_exr.py is a professional tool for converting Adobe Photoshop PSD files to OpenEXR format, maintaining layer integrity and supporting both individual layer extraction and multi-part EXR creation. The script uses ImageMagick and OpenEXR tools for high-quality conversion suitable for VFX and compositing workflows.

## Features

- **Layer Preservation** - Maintains original layer names and structure
- **Multiple Output Modes** - Individual EXR files per layer or single multi-part EXR
- **Batch Processing** - Convert entire directories of PSD files
- **EXR Compression** - Support for all OpenEXR compression algorithms
- **Security Hardened** - No shell injection vulnerabilities
- **Performance Timing** - Integrated timing for conversion monitoring
- **Error Handling** - Robust error handling with detailed reporting

## Requirements

### External Dependencies
- **ImageMagick** with OpenEXR and HDRi support
  - Homepage: https://www.imagemagick.org/
  - HDRi Guide: https://www.imagemagick.org/script/high-dynamic-range.php
- **OpenEXR binaries** (exrmultipart, exrmaketiled)
  - Homepage: http://www.openexr.org/

### Installation
```bash
# macOS with Homebrew
brew install imagemagick --with-openexr
brew install openexr

# Ubuntu/Debian
sudo apt-get install imagemagick libmagick++-dev openexr libopenexr-dev

# CentOS/RHEL
sudo yum install ImageMagick-devel OpenEXR-devel
```

## Usage

### Basic Usage
```bash
# Convert single PSD file
python3 convert_psd_to_exr.py input.psd

# Convert all PSD files in directory
python3 convert_psd_to_exr.py /path/to/psd/directory

# Create multi-layer EXR instead of individual files
python3 convert_psd_to_exr.py input.psd --multilayer
```

### Advanced Usage
```bash
# Specify EXR compression
python3 convert_psd_to_exr.py input.psd --compression zip

# Batch convert with multi-layer output
python3 convert_psd_to_exr.py /path/to/psds \
    --multilayer \
    --compression b44a
```

## Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `input` | - | Input PSD file or directory containing PSD files | Required |
| `--compression` | `-c` | EXR compression type | `B44A` |
| `--multilayer` | `-m` | Output multilayered EXR instead of one EXR per layer | False |

## EXR Compression Options

| Compression | Description | Use Case |
|-------------|-------------|----------|
| `none` | No compression | Fastest access, largest files |
| `rle` | Run-length encoding | Simple compression |
| `zip` | Zip compression | Good compression ratio |
| `piz` | PIZ compression | Good for noisy images |
| `pxr24` | Pixar 24-bit | Lossy, smaller files |
| `b44` | B44 compression | Good for final images |
| `b44a` | B44A compression | Best general purpose (default) |
| `dwaa` | DWAA compression | Advanced compression |
| `dwab` | DWAB compression | Advanced compression |

## Output Modes

### Individual Layer Mode (Default)
Creates separate EXR files for each layer:
```
input.psd → input_layer1.exr
          → input_layer2.exr
          → input_layer3.exr
```

### Multi-Layer Mode (--multilayer)
Creates single EXR with all layers:
```
input.psd → input.exr (contains all layers)
```

## Layer Processing

### Layer Detection
The script automatically detects layers by:
1. Running `identify -verbose` on the PSD file
2. Parsing layer information from ImageMagick output
3. Extracting layer names and indices
4. Handling empty or flattened layers gracefully

### Layer Export Process
1. **Extract Layer** - Uses ImageMagick convert to extract individual layers
2. **Apply Compression** - Uses exrmaketiled to apply EXR compression
3. **Clean Temporary Files** - Removes intermediate files automatically
4. **Combine (if multi-layer)** - Uses exrmultipart to create single file

### RGBA Layer Handling
- RGBA layer is automatically placed as the topmost layer in multi-part EXR
- Ensures proper compositing order for downstream applications
- Compatibility with industry-standard EXR workflows

## Examples

### Example 1: Single File Conversion
```bash
python3 convert_psd_to_exr.py ~/Desktop/comp_v001.psd
```

Output:
```
Processing: /Users/alex/Desktop/comp_v001.psd
Processing layer 1: background
Processing layer 2: foreground
Processing layer 3: rgba
PSD To EXR Conversion Running Time: 45.30 seconds
```

Creates:
- `comp_v001_background.exr`
- `comp_v001_foreground.exr`
- `comp_v001_rgba.exr`

### Example 2: Multi-Layer EXR
```bash
python3 convert_psd_to_exr.py ~/Desktop/comp_v001.psd --multilayer
```

Creates single file: `comp_v001.exr` containing all layers

### Example 3: Batch Processing
```bash
python3 convert_psd_to_exr.py ~/Projects/Renders/PSDs --compression zip
```

Converts all PSD files in the directory with ZIP compression.

### Example 4: VFX Pipeline Integration
```bash
#!/bin/bash
# VFX conversion pipeline

INPUT_DIR="/mnt/projects/shot001/comp"
OUTPUT_DIR="/mnt/projects/shot001/elements"

echo "Converting PSD comps to EXR..."
cd "$OUTPUT_DIR"

python3 convert_psd_to_exr.py "$INPUT_DIR" \
    --compression b44a \
    --multilayer

echo "Conversion complete. Files ready for Nuke."
```

## Error Handling

### Common Issues and Solutions

**Issue**: "identify: command not found"
```bash
# Install ImageMagick
brew install imagemagick  # macOS
sudo apt-get install imagemagick  # Ubuntu
```

**Issue**: "exrmultipart: command not found"
```bash
# Install OpenEXR tools
brew install openexr  # macOS
sudo apt-get install openexr  # Ubuntu
```

**Issue**: "No layers found in file"
```
Solution: PSD file may be flattened or corrupted
- Check file in Photoshop
- Ensure layers are properly named
- Try re-saving PSD with maximum compatibility
```

**Issue**: Conversion fails on specific layers
```
Solution: Check for unsupported layer types
- Some layer effects may not convert properly
- Rasterize complex layers before conversion
- Check layer names for special characters
```

### Security Features

- **No Shell Injection** - All subprocess calls use list arguments
- **Input Validation** - Validates file paths and arguments
- **Safe File Operations** - Proper handling of temporary files
- **Error Isolation** - Errors in one file don't stop batch processing

## Performance Optimization

### Large File Handling
- **Streaming Processing** - Processes layers individually to manage memory
- **Temporary File Management** - Automatic cleanup of intermediate files
- **Compression Optimization** - Intelligent compression selection
- **Batch Efficiency** - Optimized for processing multiple files

### Memory Considerations
- Each layer is processed independently
- Temporary files are cleaned immediately after use
- Memory usage scales with individual layer size, not total PSD size

## Integration

### Nuke Pipeline
```python
# Nuke script to import multi-layer EXR
import nuke

def import_multilayer_exr(filepath):
    """Import multi-layer EXR into Nuke."""
    read_node = nuke.createNode("Read")
    read_node['file'].setValue(filepath)
    
    # Set up layer channels
    read_node['premultiplied'].setValue(True)
    read_node['auto_alpha'].setValue(True)
    
    return read_node

# Usage
exr_file = "/path/to/converted/comp_v001.exr"
read_node = import_multilayer_exr(exr_file)
```

### After Effects Integration
```jsx
// After Effects script to import EXR sequence
var comp = app.project.activeItem;
var folder = Folder.selectDialog("Select EXR folder");

if (folder) {
    var files = folder.getFiles("*.exr");
    for (var i = 0; i < files.length; i++) {
        var importOptions = new ImportOptions(files[i]);
        var footage = app.project.importFile(importOptions);
        comp.layers.add(footage);
    }
}
```

### Maya Integration
```python
# Maya script to import EXR files
import maya.cmds as cmds

def import_exr_layers(directory):
    """Import EXR files as file textures in Maya."""
    import os
    
    exr_files = [f for f in os.listdir(directory) if f.endswith('.exr')]
    
    for exr_file in exr_files:
        filepath = os.path.join(directory, exr_file)
        
        # Create file texture node
        file_node = cmds.shadingNode('file', asTexture=True)
        cmds.setAttr(f"{file_node}.fileTextureName", filepath, type="string")
        cmds.setAttr(f"{file_node}.colorSpace", "Raw", type="string")
        
        print(f"Imported: {exr_file}")

# Usage
import_exr_layers("/path/to/converted/exrs")
```

## Workflow Best Practices

### PSD Preparation
1. **Layer Organization** - Use descriptive layer names
2. **Flattening** - Avoid unnecessary layer effects
3. **Naming Convention** - Use consistent, pipeline-friendly names
4. **File Size** - Consider splitting very large PSDs

### Conversion Strategy
1. **Test First** - Convert single file before batch processing
2. **Compression Choice** - Select appropriate compression for use case
3. **Quality Control** - Verify converted files in target application
4. **Archive Originals** - Keep original PSD files for future edits

### Pipeline Integration
1. **Automation** - Include in render pipeline scripts
2. **Validation** - Check converted files automatically
3. **Metadata** - Preserve creation and modification dates
4. **Version Control** - Track PSD and EXR versions together

## Troubleshooting

### ImageMagick Issues
```bash
# Check ImageMagick installation
identify -version

# Check OpenEXR support
identify -list format | grep EXR

# Test basic conversion
convert input.psd[0] test.exr
```

### OpenEXR Tools Issues
```bash
# Check OpenEXR tools
which exrmaketiled
which exrmultipart

# Test EXR tools
exrheader test.exr
```

### File Permission Issues
```bash
# Fix permissions
chmod 755 /path/to/script
chmod 644 /path/to/psd/files
```

---

*convert_psd_to_exr.py provides professional PSD to EXR conversion with layer preservation, security hardening, and comprehensive error handling for VFX and compositing workflows.*