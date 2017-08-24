#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""

Converts a PSD file to several EXR files (or one layered one) keeping the layer names intact.

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
    parser.add_argument("-m", "--multilayer", help="Output one multilayered EXR if True or one EXR per layer if False. "
                                                   "Default is True.",
                        action="store_true")
    parser.add_argument("-i", "--input", help="input file")

    # Parse arguments
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)

    # Assign or use argument values
    if not args.input:
        print "No input file specified"
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
