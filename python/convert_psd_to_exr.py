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

from timer import timer


def extract_layers(input_file):
    # imagemagick command to print out layer information about the input PSD
    identify_cmd = "identify -verbose '{}' | grep 'label:' | cut -d: -f 2".format(input_file)

    # check_output runs the specified command, and writes the result string to the var
    layers = subprocess.check_output(identify_cmd, shell=True)

    return layers


def export_layer(psdIndex, layer_name, inputFile, compression):
    extractedFilename = ""
    extIndex = inputFile.rfind(".psd")
    if extIndex is not -1:
        extractedFilename = inputFile[:extIndex]

    extractedFilename += "_" + layer_name + "_tmp.exr"
    cmd = "convert '{input}[{index}]' -compress {compress} -colorspace RGB '{output}'".format(
        input=inputFile,
        index=psdIndex,
        output=extractedFilename,
        compress=compression
    )

    print cmd
    subprocess.call(cmd, shell=True)
    return extractedFilename


def exr_compression(input):
    filesplit = os.path.splitext(input)
    cmd = "exrmaketiled -o -z b44a '{}' '{}'".format(input, "{}{}".format(filesplit[0][:-4], filesplit[1]))
    print cmd
    subprocess.call(cmd, shell=True)


def cleanup(input):
    if os.path.exists(input):
        try:
            print("removing {}".format(input))
            os.remove(input)
        except:
            print traceback.format_exc()


def main():
    argv = sys.argv
    if len(argv) < 2:
        print('No file specified')
        return
    else:
        if os.path.isfile(argv[1]) or os.path.isdir(argv[1]):

            start = timer()

            if os.path.isdir(argv[1]):
                list = os.listdir(argv[1])
                files = []

                for l in list:
                    l = os.path.join(argv[1], l)
                    if os.path.isfile(l):

                        files.append(l)
            else:
                files = [argv[1]]

            print("Found {} files to convert.".format(len(files)))

            for f in files:

                if os.path.splitext(f)[1] == ".psd":
                    layers = extract_layers(f)

                    i = 0
                    for layer in layers.split('\n'):
                        i += 1
                        layer = layer.strip()
                        if layer == "":
                            print("Skipping empty layer name. Likely flattened compatibility layer.")
                        else:
                            print("layer {}: {}".format(i, layer))
                            if len(argv) == 3:
                                compression = argv[2]
                            else:
                                compression = "B44A"
                            tmpfile = export_layer(i, layer, f, compression)
                            exr_compression(tmpfile)
                            cleanup(tmpfile)
                else:
                    print("Not a PSD document. Skipping.")

            timer(start, "PSD To EXR Conversion")
        else:
            print('No file specified')
            return


if __name__ == "__main__":
    main()
