#!/usr/bin/env python
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

from timer import timer


def extract_layers(input_file):
    # imagemagick command to print out layer information about the input PSD
    identify_cmd = "identify -verbose '{}' | grep 'label:' | cut -d: -f 2".format(input_file)

    # check_output runs the specified command, and writes the result string to the var
    layers = subprocess.check_output(identify_cmd, shell=True)

    return layers


def export_layer(psdIndex, layer_name, inputFile, compression):
    extractedFilename = "{basename}_{layer}_tmp.exr".format(
        basename=os.path.splitext(inputFile)[0],
        layer=layer_name
    )

    cmd = "convert '{input}[{index}]' -compress {compress} -colorspace RGB '{output}'".format(
        input=inputFile,
        index=psdIndex,
        output=extractedFilename,
        compress=compression
    )

    # print cmd
    subprocess.call(cmd, shell=True)
    return extractedFilename


def exr_compression(input, compression):
    filesplit = os.path.splitext(input)
    cmd = "exrmaketiled -o -z {} '{}' '{}'".format(compression, input, "{}{}".format(filesplit[0][:-4], filesplit[1]))
    # print cmd
    subprocess.call(cmd, shell=True)


def exr_multipart(layers, input):
    cmd = "exrmultipart -combine -i"

    multiFilename = "{basename}.exr".format(basename=os.path.splitext(input)[0])

    if os.path.exists(multiFilename):
        multiFilename = "{basename}_multi.exr".format(basename=os.path.splitext(input)[0])

    # Make sure rgba is the topmost layer of the EXR
    for layer in layers:
        if layer.strip() == "rgba":
            cmd = "{} '{}'::'{}'".format(cmd, get_layerFilename(input, layer), layer.strip())

    for layer in layers:
        if layer == "":
            print("Skipping empty layer name. Likely flattened compatibility layer.")
        elif layer.strip() == "rgba":
            pass
        else:
            cmd = "{} '{}'::'{}'".format(cmd, get_layerFilename(input, layer), layer)

    cmd = "{} -o '{}'".format(cmd, multiFilename)
    print cmd
    subprocess.call(cmd, shell=True)

    for layer in layers:
        cleanup(get_layerFilename(input, layer))


def get_layerFilename(input, layer):
    layer = layer.strip()
    layerFilename = "{basename}_{layer}.exr".format(
        basename=os.path.splitext(input)[0],
        layer=layer
    )
    return layerFilename


def cleanup(input):
    if os.path.exists(input):
        try:
            # print("removing {}".format(input))
            os.remove(input)
        except:
            print traceback.format_exc()


def main(input, multi, compression):
    if os.path.isfile(input) or os.path.isdir(input):

        start = timer()

        if os.path.isdir(input):
            list = os.listdir(input)
            files = []

            for l in list:
                if os.path.splitext(l)[1] == ".psd":
                    l = os.path.join(input, l)
                    if os.path.isfile(l):
                        files.append(l)
        else:
            files = [input]

        print("Found {} files to convert.".format(len(files)))

        for f in files:

            layers = extract_layers(f)

            i = 0
            for layer in layers.split("\n"):
                i += 1
                layer = layer.strip()
                if layer == "":
                    print("Skipping empty layer name. Likely flattened compatibility layer.")
                else:
                    print("layer {}: {}".format(i, layer))
                    tmpfile = export_layer(i, layer, f, compression)
                    exr_compression(tmpfile, compression)
                    cleanup(tmpfile)

            if multi:
                exr_multipart(layers.split("\n"), f)


            else:
                print("Not a PSD document. Skipping.")

        timer(start, "PSD To EXR Conversion")


if __name__ == '__main__':

    # Set up optional arguments
    parser = argparse.ArgumentParser(description="Convert a given set of PSD files to OpenEXR files.")

    parser.add_argument("-c", "--compression", help="choose the EXR compression type "
                                                    "(none/rle/zip/piz/pxr24/b44/b44a/dwaa/dwab); default is B44A",
                        default="B44A")
    parser.add_argument("-m", "--multilayer", help="Output multilayered EXR instead of one EXR per layer.",
                        action="store_true")
    parser.add_argument("-i", "--input", help="input file")

    # Parse arguments
    try:
        args = parser.parse_args()
        # Assign or use argument values

        if not args.input:
            print("\nNo input file specified\n\n")
            parser.print_help()
        else:
            infile = args.input

            if args.multilayer:
                multi = True
            else:
                multi = False

            if args.compression:
                compression = args.compression
            else:
                compression = "B44A"

            try:
                main(infile, multi, compression)
            except:
                print traceback.format_exc()

    except:

        sys.exit(0)
