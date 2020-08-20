# batches files from one larger directory to multiple smaller ones.

import os
import shutil
import argparse


def batch(inputdir, outputdir, size_of_batch, copy_or_move):

    n = size_of_batch # start n at max to initiate process
    m = 1 # for sequential directory names

    for root, dirs, files in os.walk(inputdir):

        for file in files:

            if n >= size_of_batch: # if number of files hits max

                # create new output dir
                dir = os.path.join(outputdir, "batch"+str(m))
                os.mkdir(dir)

                m += 1 # add one to dir name
                n = 0 # reset number of files in batch

            # move file to new location
            source = os.path.join(root, file)
            dest = os.path.join(dir, file)

            if copy_or_move == "m":
                shutil.move(source, dest)
            else:
                shutil.copy(source, dest)

            n += 1 # add one to number of files in current batch


def main():
    help_str = """
        Batches files from one larger directory to multiple smaller ones.
        Outputs directories batch1, batch2, batch3, etc, each containing a
        specified number of files. Will either copy or move the files.
    """
    ap = argparse.ArgumentParser(description=help_str)
    ap.add_argument("-i", "--inputdir"
                    help="""Path to the directory containing the files to be
                            batched.""",
                    type=str)
    ap.add_argument("-o", "--outputdir"
                    help="""Path to the directory to output the batched files.""",
                    type=str)
    ap.add_argument("-n", "--size_of_batch", default=1000,
                    help="""The number of files which each batch should
                            contain. Default is 1000.""",
                    type=int)
    ap.add_argument("-c", "--copy_or_move", default="c",
                    help="""Whether the files should be copied or moved to their
                            new location. 'c' to copy, 'm' to move. Default is
                            'c'.""",
                    type=str)


    args = ap.parse_args()

    input = args.inputdir
    output = args.outputdir
    size = args.size_of_batch
    copy_or_move = args.copy_or_move

    if copy_or_move == "c" or copy_or_move == "m":
        batch(input, output, size, copy_or_move)
    else:
        print("Please enter valid option for choosing to copy or move your files.")


main()
