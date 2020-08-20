# moves or copies files from multiple directories into one.

import os
import shutil
import argparse


def unbatch(indir, outdir, copy_or_move):

    for root, dirs, files in os.walk(indir):

        for dir in dirs:

            files = os.listdir(os.path.join(root, dir)) # get all files in dir

            for f in files: # iterate through the files in a dir

                # move file to new location
                source = os.path.join(root, dir, f)
                dest = os.path.join(outdir, f)

                if copy_or_move == "m":
                    shutil.move(source, dest)
                else:
                    shutil.copy(source, dest)

            # remove original dir when all files are out
            if copy_or_move == "m":
                rem = os.path.join(root, dir)
                os.rmdir(rem)


def main():
    help_str = """
        Moves or copies files from multiple directories into one.
    """
    ap = argparse.ArgumentParser(description=help_str)
    ap.add_argument("-i", "--indir",
                    help="""Path to the directory containing the folders
                            containing the files to be unbatched.""",
                    type=str)
    ap.add_argument("-o", "--outdir",
                    help="""Path to the directory to output the unbatched files.""",
                    type=str)
    ap.add_argument("-c", "--copy_or_move", default="c",
                    help="""Whether the files should be copied or moved to their
                            new location. 'c' to copy, 'm' to move. Default is
                            'c'.""",
                    type=str)


    args = ap.parse_args()

    indir = args.indir
    outdir = args.outdir
    copy_or_move = args.copy_or_move

    shutil.rmtree(outdir, ignore_errors=True)
    os.mkdir(outdir)

    if copy_or_move == "c" or copy_or_move == "m":
        unbatch(indir, outdir, copy_or_move)
    else:
        print("Please enter valid option for choosing to copy or move your files.")


main()
