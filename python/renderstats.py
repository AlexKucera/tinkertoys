#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""
tinkertoys - renderstats

Release Notes:

V0.1 Initial Release - 2017-10-04

"""

import argparse
import re
import sys
import traceback
from itertools import imap

SEQ_REGEX = re.compile('^(?P<basename>.*[_\.])(?P<frame>\d+)(?P<extension>\..*)$')


# FUNCTIONS -----------------------------------------------
def secondsToHoursMinutesSeconds(seconds):
    """ takes a seconds int or float and returns a string that breaks"""
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours != 0:
        hours = "{} hours ".format(int(hours))
    else:
        hours = ""
    if minutes != 0:
        minutes = "{} minutes ".format(int(minutes))
    else:
        minutes = ""
    seconds = "{:.2f} seconds".format(seconds)

    secondsToString = '{hours}{minutes}{seconds}'.format(hours=hours, minutes=minutes, seconds=seconds)

    return secondsToString


def get_stats(path, filename, files):
    m_stat = []
    r_time = []
    counter = 0
    for i in files:
        if os.path.isfile(os.path.join(path, i)) and i != filename:
            counter += 1
            m_stat.append(os.stat(os.path.join(path, i)).st_mtime)

            if len(m_stat) > 2:
                r_time.append(abs(m_stat[-1] - m_stat[-2]))

    rendertime = max(m_stat) - min(m_stat) + ((max(m_stat) - min(m_stat)) / counter)

    stats = 'Listing render stats for "{}":\n' \
            '\nOverall rendertime: {} for {} files\n' \
            'That\'s an mean/average of {} per frame.\n' \
            'Maximum per frame time was: {}\n' \
            'Minimum per frame time was: {}'.format(
        path,
        secondsToHoursMinutesSeconds(rendertime),
        counter,
        secondsToHoursMinutesSeconds(rendertime / counter),
        secondsToHoursMinutesSeconds(max(r_time)),
        secondsToHoursMinutesSeconds(min(r_time))
    )

    return stats

def check_size(path, files):
    for i in files:
        if os.path.isfile(os.path.join(path, i)) and os.path.getsize(os.path.join(path, i)) < 128:
            yield i


def check_files(path, files):
    seq_files = get_sequential_files(files)
    message = ""
    message += "\nFound the following continuous frame ranges:"

    message = string_range(seq_files, message)

    missing_frames = sorted(list(missing(min(seq_files), max(seq_files), seq_files)))
    if len(missing_frames) > 0:

        message += "\n\nExpected a continuous range from {} to {}. Missing {} frames:".format(
            min(seq_files),
            max(seq_files),
            len(missing_frames)
        )

        message = string_range(missing_frames, message)

    else:
        message += "\nAll frames accounted for."

    if len(list(check_size(path, files))) > 0:
        message += "\n\nSome files ({}) are smaller then 128 bytes and are likely broken or incomplete:".format(
            len(list(check_size(path, files))))
        message = string_range(get_sequential_files(check_size(path, files)), message)

    return message


def missing(first, last, list, incr=1):
    """
    Returns the set of frames missing for this instance as the difference
    between the set of all frames from self.first to self.last (inclusive)
    with the increment provided.

    :key incr: the increment value to use (1) for the full set of frames.
    :type incr: int
    :returns: set of all missing frames.
    :rtype: set
    """

    return set(xrange(first, last + 1, incr)).difference(list)


def contractor(ranges):
    """
    Yields the current SequentialRange contents as a list of tuples.
    Each tuple represents (first, last, increment) of a continuous frame
    range.  The purpose of contractor is to provide a quick means of
    seeing all the continuous and discontinuous ranges in the
    SequentialRange object via a Generator object.

    :yields: each (first, last, incr) tuple.
    :ytype: tuple
    """
    frames = sorted(list(ranges))
    total = len(frames)
    curr_idx = 0
    while curr_idx < total:
        first, last, incr = frames[curr_idx], frames[curr_idx], 1
        if curr_idx + 2 < total:
            last_idx = curr_idx + 2
            curr_incr = frames[curr_idx + 1] - frames[curr_idx]
            while last_idx < total:
                if curr_incr == frames[last_idx] - frames[last_idx - 1]:
                    last = frames[last_idx]
                    incr = curr_incr
                    curr_idx = last_idx
                else:
                    break

                last_idx += 1

        curr_idx += 1
        yield first, last


def string_range(frame_range, message):

    for frames in contractor(frame_range):
        if frames[0] == frames[1]:
            message += "\n{}".format(frames[0])
        else:
            message += "\n{}-{}".format(frames[0], frames[1])

    return message

def get_sequential_files(filenames):
    """
    Generator that yields the sequential files in list of filenames.

    :arg filenames: a list of filenames to search for sequential files
    :type filenames: iterable
    :yields: each valid FileSequence in filenames
    :ytype: pysequences.model.filesequence.FileSequence
    """
    results = {}
    for match in imap(SEQ_REGEX.match, filenames):
        if match:
            key = '%(pad)s'.join([match.group('basename'), \
                                  match.group('extension')])

            if key not in results.keys():
                results[key] = set()
            # end if

            results[key].add(match.group('frame'))
            # end if
    # end for loop

    for name in sorted(results.keys()):
        frames = set(imap(int, results[name]))
        lengths = list(sorted(set(imap(len, results[name]))))

        if len(lengths) == 1:
            length = lengths[0]
        else:
            length = min(lengths)

        return frames


# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------
import os


def main(infile, fileout, recursive, filename):
    infile = os.path.abspath(os.path.normpath(infile))

    if os.path.isdir(infile):
        path = infile
    else:
        path = os.path.dirname(infile)

    if recursive:
        for path, dirs, files in os.walk(path):
            get_stats(path, filename, files)
    else:
        files = os.listdir(path)
        stats = get_stats(path, filename, files)
        filecheck = check_files(path, files)

        if fileout:
            outfile = os.path.join(path, filename)
            with open(outfile, "w") as f:
                f.write(stats)
                f.write(filecheck)
        else:
            print(stats)
            print(filecheck)



# END MAIN PROGRAM -----------------------------------------------

if __name__ == '__main__':
    # Set up optional arguments
    parser = argparse.ArgumentParser(
        description="Outputs a list of render statistics for a provided folder. Accepts any file or folder path.")
    parser.add_argument("input", help="input file/folder")
    parser.add_argument("-r", "--recursive", help="Go through all subfolders recursively.", action='store_true')
    parser.add_argument("-f", "--file", help="Output statistics to file instead of stdout.", action='store_true')
    parser.add_argument("-n", "--name", help="Name to be used for the renderstats file. (default: renderstats.txt)",
                        default="renderstats.txt")

    # Parse arguments
    try:
        args = parser.parse_args()

        # Assign or use argument values

        if not args.input:
            print("\nNo input specified\n\n")
            parser.print_help()
        else:
            infile = args.input

            try:
                main(infile, args.file, args.recursive, args.name)
            except:
                print traceback.format_exc()

    except:

        sys.exit(0)
