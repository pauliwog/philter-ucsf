import re
import os
import shutil
import json
import time
import argparse
import pandas as pd
from pandas.io.json import json_normalize

# output items in nested dict
def get_values(nested_dict, out_path):
    for key, value in nested_dict.items(): # got through dict

        if type(value) is dict: # if value is another nested dict

            with open(out_path, "a") as fout:
                fout.write("\n\n%s" % (key))

            get_values(value, out_path) # until we reach the end of nested dicts

        else: # if the value is not a nested dict, output

            with open(out_path, "a") as fout:
                if value == "NA":
                    fout.write("\n%s : %s" % (key, value))
                elif "difference" in key and float(value) > 0: # add a plus sign in front of positive differences
                    if "percentage" in key: # if value is a percent
                        fout.write("\n%s : +%s%%" % (key, value))
                    else:
                        fout.write("\n%s : +%s" % (key, value))
                elif "percentage" in key: # if value is a percent
                    fout.write("\n%s : %s%%" % (key, value))
                else:
                    fout.write("\n%s : %s" % (key, value))



# compare the two summary.json eval files
def compare_eval_summaries(dir1, dir2, outdir, batch_name, compare_each_batch):

    time.sleep(1)
    print("Comparing ...%s/eval/summary.json files..." % (dir2[-35:]))

    text1 = json.loads(open(os.path.join(dir1, "eval/summary.json")).read())
    text2 = json.loads(open(os.path.join(dir2, "eval/summary.json")).read())

    summary = {} # dict to output

    for key in text1:
        summary[key] = {}
        summary[key].update({"dir1" : text1[key]})
        summary[key].update({"dir2" : text2[key]})
        summary[key].update({"difference (dir2 - dir1)" : float(text2[key])-float(text1[key])}) # compute difference between dir2 and dir1
        if float(text2[key]) != 0 or float(text1[key]) != 0:
            summary[key].update({"percentage difference ((dir2/dir1 - 1)*100)" : (float(text2[key])/float(text1[key])-1)*100})
        else:
            summary[key].update({"percentage difference ((dir2/dir1 - 1)*100)" : "NA"})

    if compare_each_batch:
        out_path = os.path.join(outdir, batch_name, "eval_summary.txt")
    else:
        out_path = os.path.join(outdir, batch_name+"_eval_summary.txt")

    get_values(summary, out_path) # output dict



# compare the tp, tn, fp, fn .eval files
def compare_eval_files(indir, dir1, dir2, options, outdir, totals, compare_each_batch):

    # set up lists to go through
    print_statements = []
    current_comparison = []
    check_in = []
    check_against = []

    if "fp" in options: # if user wants to compare false positives
        fp1 = open(os.path.join(dir1, "eval/fp.eval")).read().splitlines()
        fp2 = open(os.path.join(dir2, "eval/fp.eval")).read().splitlines()
        check_in.extend([fp1, fp2])
        check_against.extend([fp2, fp1])
        print_statements.extend(["False positives in dir1 and not dir2:", "\n\n\nFalse positives in dir2 and not dir1:"])
        current_comparison.extend(["fp", "fp"]) # account for comparing both ways (1 vs 2, 2 vs 1)

    if "tp" in options: # if user wants to compare true positives
        tp1 = open(os.path.join(dir1, "eval/tp.eval")).read().splitlines()
        tp2 = open(os.path.join(dir2, "eval/tp.eval")).read().splitlines()
        check_in.extend([tp1, tp2])
        check_against.extend([tp2, tp1])
        print_statements.extend(["True positives in dir1 and not dir2:", "\n\n\nTrue positives in dir2 and not dir1:"])
        current_comparison.extend(["tp", "tp"]) # account for comparing both ways (1 vs 2, 2 vs 1)

    if "fn" in options: # if user wants to compare false negatives
        fn1 = open(os.path.join(dir1, "eval/fn.eval")).read().splitlines()
        fn2 = open(os.path.join(dir2, "eval/fn.eval")).read().splitlines()
        check_in.extend([fn1, fn2])
        check_against.extend([fn2, fn1])
        print_statements.extend(["False negatives in dir1 and not dir2:", "\n\n\nFalse negatives in dir2 and not dir1:"])
        current_comparison.extend(["fn", "fn"]) # account for comparing both ways (1 vs 2, 2 vs 1)

    if "tn" in options: # if user wants to compare true negatives
        tn1 = open(os.path.join(dir1, "eval/tn.eval")).read().splitlines()
        tn2 = open(os.path.join(dir2, "eval/tn.eval")).read().splitlines()
        check_in.extend([tn1, tn2])
        check_against.extend([tn2, tn1])
        print_statements.extend(["True negatives in dir1 and not dir2:", "\n\n\nTrue negatives in dir2 and not dir1:"])
        current_comparison.extend(["tn", "tn"]) # account for comparing both ways (1 vs 2, 2 vs 1)

    # go through each comparison, eg. (1) true positives dir1 vs dir2, (2) true postives dir2 vs dir1, (3) fase positives dir1 vs dir2, (4) false positives dir2 vs dir1
    for i in range(len(print_statements)):

        if i % 2 == 0: # account for comparing both ways for each file
            time.sleep(1)
            print("Comparing ...%s/eval/%s files..." % (dir2[-35:], current_comparison[i]))

        exist = False # if there are no values in only one of the two dirs

        if compare_each_batch:
            with open(os.path.join(outdir, current_comparison[i]+".txt"), "a") as fout:
                fout.write(print_statements[i])

        for line in check_in[i]: # iterate through each line in the .eval files

            if line not in check_against[i]: # if the line in the first file is not in the second

                exist = True

                # set up dictionary to make output easier

                line = line.split("\t")

                line_data = {}

                line_data["filepath"] = line[0]
                line_data["phi_type"] = line[1]
                line_data["match"] = line[2]
                line_data["start"] = line[3]
                line_data["stop"] = line[4].strip()

                filename = re.findall('[\S]+\/([\S]+?\.txt)', line_data["filepath"])[0]

                # get the "match in context" from the original txt file passed through Philter
                line_data["match in context"] = open(os.path.join(indir, filename)).read()[int(line_data["start"])-100 : int(line_data["stop"])+100].strip().replace("\n", "\\n")
                line_data["match in context"] = " ".join(line_data["match in context"].split()) # replace all whitespace with a single space

                # output
                if compare_each_batch:
                    with open(os.path.join(outdir, current_comparison[i]+".txt"), "a") as fout:
                        fout.write("\n\n")
                        for key in line_data:
                            fout.write("%s:\t'%s'\n" % (key, line_data[key]))

                if i % 2 == 0:
                    totals[current_comparison[i]+"_1not2"].extend([{"filepath": line_data["filepath"], "phi_type": line_data["phi_type"], "match": line_data["match"], "start": line_data["start"], "stop": line_data["stop"], "context": line_data["match in context"]}])
                else:
                    totals[current_comparison[i]+"_2not1"].extend([{"filepath": line_data["filepath"], "phi_type": line_data["phi_type"], "match": line_data["match"], "start": line_data["start"], "stop": line_data["stop"], "context": line_data["match in context"]}])

        # if no differences exist
        if compare_each_batch:
            if not exist:
                with open(os.path.join(outdir, current_comparison[i]+".txt"), "a") as fout:
                    fout.write("\n\nNo differences exist.")

    return(totals)



# compare the log/phi_marked.json files
def compare_log_phi_marked(dir1, dir2, indir, outdir, totals, compare_each_batch):

    time.sleep(1)
    print("Comparing ...%s/log/phi_marked.json files..." % (dir2[-35:]))

    log1 = os.path.join(dir1, "log/phi_marked.json")
    log2 = os.path.join(dir2, "log/phi_marked.json")
    in_only_1 = [] # for tags in dir1 and not dir2
    in_only_2 = [] # for tags in dir2 and not dir1

    with open(log1) as fin:
        log1_big = json.load(fin)
    with open(log2) as fin:
        log2_big = json.load(fin)

    for filepath in log1_big: # go through each file

        tags1 = log1_big[filepath]
        tags2 = log2_big[filepath]

        for tag in tags1: # go through each tag
            if tag not in tags2: # if tag is not in second dir
                filename = re.findall('[\S]+\/([\S]+?\.txt)', filepath)[0]
                context = open(os.path.join(indir, filename)).read()[int(tag["start"])-50 : int(tag["end"])+50].strip().replace("\n", "\\n")
                context = " ".join(context.split()) # replace all whitespace with a regular space
                word = tag["word"]
                in_only_1.append([word, filepath, tag, context])

        for tag in tags2: # go through each tag
            if tag not in tags1: # if tag is not in the first dir
                filename = re.findall('[\S]+\/([\S]+?\.txt)', filepath)[0]
                context = open(os.path.join(indir, filename)).read()[int(tag["start"])-50 : int(tag["end"])+50].strip().replace("\n", "\\n")
                context = " ".join(context.split()) # replace all whitespace with a regular space
                word = tag["word"]
                in_only_2.append([word, filepath, tag, context])

    # output

    if compare_each_batch:
        if bool(in_only_1): # if there are tags in dir1 and not dir2

            with open(os.path.join(outdir, "tags_in_only_1.txt"), "a") as fout:
                for item in in_only_1:
                    fout.write("\n\nWord: '%s'\nFilepath: '%s'\nTag [start, stop, word, phi-type]: '%s'\nMatch in context: '%s'" % (item[0], item[1], item[2], item[3]))

        else: # if there are no tags in dir1 and not dir2

            s = "There are no tags in dir1 and not dir2."
            with open(os.path.join(outdir, "tags_in_only_1.txt"), "a") as fout:
                fout.write(s)


        if bool(in_only_2): # if there are tags in dir1 and not dir2

            with open(os.path.join(outdir, "tags_in_only_2.txt"), "a") as fout:
                for item in in_only_2:
                    fout.write("\n\nWord: '%s'\nFilepath: '%s'\nTag [start, stop, word, phi-type]: '%s'\nMatch in context: '%s'" % (item[0], item[1], item[2], item[3]))

        else: # if there are no tags in dir1 and not dir2

            s = "There are no tags in dir2 and not dir1."
            with open(os.path.join(outdir, "tags_in_only_2.txt"), "a") as fout:
                fout.write(s)

    for item in in_only_1:
        totals["tags_1not2"].extend([{"word": item[0], "filepath": item[1], "tag": item[2], "context": item[3]}])
    for item in in_only_2:
        totals["tags_2not1"].extend([{"word": item[0], "filepath": item[1], "tag": item[2], "context": item[3]}])

    if compare_each_batch:
        with open(os.path.join(outdir, "phi_marked_summary.txt"), "a") as fout:
            fout.write("There were %d tags in dir1 and not dir2.\n" % (len(in_only_1)))
            fout.write("There were %d tags in dir2 and not dir1.\n" % (len(in_only_2)))

    return (totals)



def total_up(outdir, totals):

    outdir = os.path.join(outdir, "totals/")
    shutil.rmtree(outdir, ignore_errors=True)
    os.mkdir(outdir)

    with open(os.path.join(outdir, "everything.json"), 'w', encoding='utf-8') as fout:
        json.dump(totals, fout, ensure_ascii=False, indent=4)

    current_out = ["fp_1not2", "fp_2not1", "tp_1not2", "tp_2not1", "fn_1not2", "fn_2not1", "tn_1not2", "tn_2not1"]

    for item in current_out:
        with open(os.path.join(outdir, item+".json"), 'w', encoding='utf-8') as fout:
            if totals[item]:
                json.dump(totals[item], fout, ensure_ascii=False, indent=4)
            else:
                fout.write("There are no %ss in dir %s and not dir %s." % (item.split("_")[0], item.split("_")[1][:1], item.split("_")[1][-1:]))



def main():
    help_str = """
        Compares two Philter runs. This script will compare any/all of the
        'eval/summary.json', 'eval/fp/tp/fn/tp.eval', or 'log/phi_marked.json'
        files.

        If the options 'fp', 'tp', 'fn', or 'tn' is included, the script will
        read in the .eval files and find values which exist in one dir but not
        the other (it will compare both dir1 vs dir2 and dir2 vs dir1).

        If the option 'summary' is included, the script will read in the
        'eval/summary.json' files and compute the differences between each file
        (dir2 - dir1).

        If the option 'phi_marked' is included, the script will read in the
        'log/phi_marked.json' files and find the tags which exist in one dir
        but not the other, and vice versa.
    """
    ap = argparse.ArgumentParser(description=help_str)
    ap.add_argument("-i", "--input_directory",
                    help="""The path to the directory which was input to
                            Philter (the text files).""",
                    type=str)
    ap.add_argument("-d1", "--directory_one",
                    help="""One of the two directories which will be compared.
                            Generally this dir should be the the control, or
                            dir which is being tested against.""",
                    type=str)
    ap.add_argument("-d2", "--directory_two",
                    help="""The other of the two directories which will be
                            compared. Generally this dir should be the test
                            dir.""",
                    type=str)
    ap.add_argument("-o", "--outputdir",
                    help="",
                    default=".",
                    type=str)
    ap.add_argument("-ops", "--options",
                    help="""Which files will be compared. The options are
                            'summary', 'phi_marked', 'fp', 'tp', 'fn', or 'tn',
                            or any combination of them. For example, if 'fp'
                            and 'tp' were used, '-o fp tp', this script would
                            compare the files 'eval/fp.eval' and 'eval/tp.eval'.
                            """,
                    nargs="+",
                    type=str)
    ap.add_argument("-each", "--compare_each_batch",
                    default="no",
                    help="""Whether each individual batch will be compared.
                            'Yes' will compare each individual batch as well as
                            all the batches together, 'no' will only compare
                            everything together. Default it 'no'.
                            """,
                    type=str)

    args = ap.parse_args()

    indir = args.input_directory
    dir1 = args.directory_one
    dir2 = args.directory_two
    outputdir = args.outputdir
    options = args.options

    start_time = time.time()

    if options is None:
        print("Please enter options.")
        exit()

    if args.compare_each_batch == "yes":
        compare_each_batch = True
    elif args.compare_each_batch == "no":
        compare_each_batch = False
    else:
        print("Please enter valid argument for -each.")
        exit()

    outdir = os.path.join(outputdir, "compare_results_out_"+dir2.split("/")[-2])
    shutil.rmtree(outdir, ignore_errors=True)
    os.mkdir(outdir)

    subdirs_exist = False

    if compare_each_batch:
        for root, dirs, files in os.walk(dir2):
            for dir in dirs:
                if "eval" not in dir and "log" not in dir:
                    outdir = os.path.join(outputdir, "compare_results_out_"+dir2.split("/")[-2], dir.split("/")[-1])
                    shutil.rmtree(outdir, ignore_errors=True)
                    os.mkdir(outdir)

    for root, dirs, files in os.walk(dir2):
        for dir in dirs:
            if "eval" not in dir and "log" not in dir:
                subdirs_exist = True
                break
        break

    if subdirs_exist:

        totals = {"fp_1not2": [], "fp_2not1": [], "tp_1not2": [], "tp_2not1": [], "fn_1not2": [], "fn_2not1": [], "tn_1not2": [], "tn_2not1": [], "tags_1not2": [], "tags_2not1": []}

        if "summary" in options:
            for root, dirs, files in os.walk(dir2):
                for dir in dirs:
                    if "eval" not in dir and "log" not in dir:
                        outdir = os.path.join(outputdir, "compare_results_out_"+dir2.split("/")[-2])
                        compare_eval_summaries(os.path.join(dir1, dir), os.path.join(dir2, dir), outdir, dir.split("/")[-1], compare_each_batch)

        for root, dirs, files in os.walk(dir2):
            for dir in dirs:
                if "eval" not in dir and "log" not in dir:
                    outdir = os.path.join(outputdir, "compare_results_out_"+dir2.split("/")[-2], dir.split("/")[-1])
                    totals = compare_eval_files(os.path.join(indir, dir), os.path.join(dir1, dir), os.path.join(dir2, dir), options, outdir, totals, compare_each_batch)

        if "phi_marked" in options:
            for root, dirs, files in os.walk(dir2):
                for dir in dirs:
                    if "eval" not in dir and "log" not in dir:
                        outdir = os.path.join(outputdir, "compare_results_out_"+dir2.split("/")[-2], dir.split("/")[-1])
                        totals = compare_log_phi_marked(os.path.join(dir1, dir), os.path.join(dir2, dir), os.path.join(indir, dir), outdir, totals, compare_each_batch)

        total_up("compare_results_out_"+dir2.split("/")[-2], totals)

    else:

        outdir = os.path.join(outputdir, "compare_results_out_"+dir2.split("/")[-2])
        shutil.rmtree(outdir, ignore_errors=True)
        os.mkdir(outdir)

        if "summary" in options:
            compare_eval_summaries(dir1, dir2, outdir, None, compare_each_batch)

        compare_eval_files(indir, dir1, dir2, options, outdir)

        if "phi_marked" in options:
            compare_log_phi_marked(dir1, dir2, indir, outdir)

    print("Completed in %f seconds.\n" % (time.time() - start_time))


main()
