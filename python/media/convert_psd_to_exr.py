#!/usr/bin/env python3
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""

Converts a PSD file to several EXR files (or one layered one) keeping the layer names intact.

Requires ImageMagick (https://www.imagemagick.org/)
with OpenEXR and HDRi support (https://www.imagemagick.org/script/high-dynamic-range.php)
as well as the OpenEXR binaries (http://www.openexr.org/).

v0.1 - 2017-08-24

Copyright 2017 - BabylonDreams - Alexander Kucera & Monika Kucera GbR

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

"""

import sys
import subprocess
import os
import traceback
import argparse

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'development'))
from timer import timer


def extract_layers(input_file):
    """Extract layer information from PSD file using ImageMagick.
    
    Args:
        input_file: Path to PSD file
        
    Returns:
        Layer information as string
    """
    try:
        # Use subprocess.run with list arguments to prevent shell injection
        result = subprocess.run(
            ['identify', '-verbose', input_file],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Extract layer information from verbose output
        layers = []
        for line in result.stdout.splitlines():
            if 'label:' in line:
                layer_name = line.split(':', 1)[1].strip()
                layers.append(layer_name)
        
        return '\n'.join(layers)
        
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to extract layers from {input_file}: {e}")


def export_layer(psd_index, layer_name, input_file, compression):
    """Export a single layer from PSD to EXR format.
    
    Args:
        psd_index: Layer index in PSD file
        layer_name: Name of the layer
        input_file: Path to PSD file
        compression: EXR compression type
        
    Returns:
        Path to extracted EXR file
    """
    extracted_filename = f"{os.path.splitext(input_file)[0]}_{layer_name}_tmp.exr"
    
    try:
        # Use subprocess.run with list arguments to prevent shell injection
        subprocess.run([
            'convert',
            f'{input_file}[{psd_index}]',
            '-compress', compression,
            '-colorspace', 'RGB',
            extracted_filename
        ], check=True)
        
        return extracted_filename
        
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to export layer {layer_name}: {e}")


def exr_compression(input_file, compression):
    """Apply EXR compression to the file.
    
    Args:
        input_file: Path to EXR file
        compression: Compression type
    """
    file_split = os.path.splitext(input_file)
    output_file = f"{file_split[0][:-4]}{file_split[1]}"
    
    try:
        subprocess.run([
            'exrmaketiled',
            '-o',
            '-z', compression,
            input_file,
            output_file
        ], check=True)
        
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to compress EXR file {input_file}: {e}")


def exr_multipart(layers, input_file):
    """Combine multiple EXR layers into a single multipart EXR."""
    cmd_args = ['exrmultipart', '-combine', '-i']

    multiFilename = f"{os.path.splitext(input_file)[0]}.exr"

    if os.path.exists(multiFilename):
        multiFilename = f"{os.path.splitext(input_file)[0]}_multi.exr"

    # Make sure rgba is the topmost layer of the EXR
    for layer in layers:
        if layer.strip() == "rgba":
            layer_file = get_layerFilename(input_file, layer)
            cmd_args.append(f"{layer_file}::{layer.strip()}")

    for layer in layers:
        if layer == "":
            print("Skipping empty layer name. Likely flattened compatibility layer.")
        elif layer.strip() == "rgba":
            pass
        else:
            layer_file = get_layerFilename(input_file, layer)
            cmd_args.append(f"{layer_file}::{layer.strip()}")

    cmd_args.extend(['-o', multiFilename])
    try:
        subprocess.run(cmd_args, check=True)
        print(f"Created multipart EXR: {multiFilename}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to create multipart EXR: {e}")

    for layer in layers:
        cleanup(get_layerFilename(input_file, layer))


def get_layerFilename(input_file, layer):
    """Generate filename for a layer EXR file."""
    layer = layer.strip()
    return f"{os.path.splitext(input_file)[0]}_{layer}.exr"


def cleanup(file_path):
    """Remove temporary file if it exists."""
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except OSError as e:
            print(f"Warning: Could not remove {file_path}: {e}")


def main(input_path, multi, compression):
    """Main conversion function."""
    if not (os.path.isfile(input_path) or os.path.isdir(input_path)):
        raise ValueError(f"Input path does not exist: {input_path}")

    start = timer()

    if os.path.isdir(input_path):
        # Find all PSD files in directory
        files = []
        for filename in os.listdir(input_path):
            if filename.lower().endswith('.psd'):
                full_path = os.path.join(input_path, filename)
                if os.path.isfile(full_path):
                    files.append(full_path)
    else:
        if not input_path.lower().endswith('.psd'):
            raise ValueError("Input file must be a PSD file")
        files = [input_path]

    print(f"Found {len(files)} files to convert.")

    for file_path in files:
        try:
            print(f"Processing: {file_path}")
            
            layers = extract_layers(file_path)
            
            if not layers.strip():
                print(f"No layers found in {file_path}. Skipping.")
                continue
            
            layer_list = [layer.strip() for layer in layers.split("\n") if layer.strip()]
            
            for i, layer in enumerate(layer_list, 1):
                print(f"Processing layer {i}: {layer}")
                tmp_file = export_layer(i, layer, file_path, compression)
                exr_compression(tmp_file, compression)
                cleanup(tmp_file)
            
            if multi and layer_list:
                exr_multipart(layer_list, file_path)
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            continue

    timer(start, "PSD To EXR Conversion")


if __name__ == '__main__':

    # Set up optional arguments
    parser = argparse.ArgumentParser(description="Convert a given set of PSD files to OpenEXR files.")

    parser.add_argument("-c", "--compression", help="choose the EXR compression type "
                                                    "(none/rle/zip/piz/pxr24/b44/b44a/dwaa/dwab); default is B44A",
                        default="B44A")
    parser.add_argument("-m", "--multilayer", help="Output multilayered EXR instead of one EXR per layer.",
                        action="store_true")
    parser.add_argument("input", help="input PSD file or directory containing PSD files")

    # Parse arguments
    try:
        args = parser.parse_args()
        # Assign or use argument values

        main(args.input, args.multilayer, args.compression)
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
