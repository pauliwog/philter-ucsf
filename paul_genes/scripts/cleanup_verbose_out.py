# takes verbose output from Philter and re-formats it to be easier to look at

import re
import argparse


def parse(fin):

    with open(fin) as f:
        text = f.readlines()

    newtext = []

    for i in range(len(text)):
        line = text[i]

        # if line is "searching regex with index x"
        if line.startswith('map_regex(): searching for regex'):

            # get values in line
            index = re.search('index (\d+)', line).group(1)

            newtext.append("\n\nRegex index is '%s'" % (index)) # reformat values and add to newtext

        # if line is "regex is re.compile()"
        elif line.startswith('map_regex(): regex is'):

            # get values in line
            exp = re.search('regex is ([a-zA-Z]+?\.[a-zA-Z]+?\([\s\S]+\))', line).group(1)

            newtext.append("\nRegular expression is '%s'" % (exp)) # reformat values and add to newtext

        # if line is a match object
        elif line.startswith('<re.Match object;'):

            # get values in line
            word = re.search('match=[\'|\"](.+?)[\'|\"]\>', line).group(1)
            start = re.search('span=\((\d+?),', line).group(1)
            end = re.search('span=\(\d+?, (\d+?)\),', line).group(1)

            newtext.append("\nWord is '%s',    Start is '%s',   End is '%s'" % (word, start, end)) # reformat values and add to newtext

        # if line is not one of the above, add the original line to newtext
        else:

            newtext.append(line)

    return newtext


def main():

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--fin", type=str) # path to Philter's output .txt file
    args = ap.parse_args()

    fin = args.fin
    fout = fin[:-4]+"_transformed.txt"

    newtext = parse(fin)

    with open(fout, "w") as fout:
        for line in newtext:
            fout.write(line)


main()
