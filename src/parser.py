import argparse
import os


def filepath(string):
    if os.path.isfile(string):
        return string
    else:
        raise FileNotFoundError(string)

def parsing():
    parser = argparse.ArgumentParser(prog='pg-project',
                                    fromfile_prefix_chars='@',
                                    description='Options below')
    parser.add_argument('-d', '--db',
                        metavar="",
                        help='Path to SQLite DB file, creates on path if file doesn\'t exist')
    parser.add_argument('-s', '--songs',
                        type=filepath,
                        metavar="",
                        help='Path to song file',
                        required=True)
    parser.add_argument('-t', '--trips',
                        type=filepath,
                        metavar="",
                        help='Path to triplets file',
                        required=True)
    args = parser.parse_args()
    return args
