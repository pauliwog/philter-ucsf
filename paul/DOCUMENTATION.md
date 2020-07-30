# Who am I and what I worked on
I'm Paul, a rising junior in high school, and I worked remotely at the UCSF Bakar Computational Health Sciences Institute on Philter as a summer intern in 2020. Philter is a clinical de-identification software which removes protected health information (phi) from clinical notes to make the data in the notes more readily available to the scientific community. Philter stands for "Protected Health Information filter." I implemented whitelists and safe regexes for gene symbols and pathology terms to address the issue of Philter obscuring these symbols and terms. Gene symbols and pathology terms (eg. BRCA1) were obscured by Philter because they have similarities to person names. Specifically, I tackled gene symbols, staging terms, cassette/slide numbers, lymph nodes, and molecular markers.

<img align="right" width=40% src="https://media.springernature.com/lw685/springer-static/image/art%3A10.1038%2Fs41746-020-0258-y/MediaObjects/41746_2020_258_Fig1_HTML.png?as=webp">

Philter follows a pipeline comprised of different methods which identify values as “safe” or “phi.” Those methods are pattern matching, blacklists, and whitelists. Philter is a rule based algorithm—so the order in which the methods are applied matters. The general pipeline order is (1) safe regexes, (2) PHI regexes, (3) blacklists, (4) whitelists, (5) the catch-all (not in the config file.) See the image to the right as an example (image from [https://www.nature.com/articles/s41746-020-0258-y](https://www.nature.com/articles/s41746-020-0258-y)).

Whitelists get used near the end of the pipeline, after Philter has identified the phi. The whitelists might contain values which are actually phi, so putting the whitelist at the end allows values to be identified as phi before they would have been incorrectly flagged as safe by the whitelist. What whitelists do is prevent the "catch-all" at the end of the pipeline (which obscures everything not marked as safe) from obscuring the safe values in the whitelist. Introducing gene symbols and pathology terms whitelists would theoretically prevent Philter from obscuring the gene symbols and pathology terms present in the clinical notes.

However, upon closer examination and testing, I discovered that multiple regular expressions earlier in the pipeline tagged the gene symbols as names—which meant that the whitelist never had a chance to tag the symbols as safe. To fix this, I created a "safe" regex which I put into the pipeline ahead of the regexes which were obscuring gene symbols. This "safe" regex would get to the gene symbols ahead of the other regexes and mark them as safe. I used the same technique of creating a safe regex or whitelist to address the incorrect obscuring of some pathology terms.

I also worked with David, my fellow summer intern, a little (it was his project) to create the correct xml annotations for the MIMIC notes. I only provided some advice and tested his results. The reason why I'm mentioning it is because having correct annotations is crucial to testing any sort of thing with Philter—they allow Philter to evaluate its performance. The annotations are xml files, and for each phi in a clinical note they contain the (1) phi type, (2) actual value, (3) start and stop indices of the value(s), and (4) an ID. For example, Philter, reading an annotation file, can identify real phi it obscured (true positives), which values it obscured but were actually safe (false positives), etc, and calculate metrics about its performance. I needed annotations for my test set of notes in order to determine how much the whitelists/safe regexes helped, or to tell if my modifications negatively impacted Philter.

If some of my scripts are confusing, check out [details_on_scripts.md](https://github.com/pauliwog/philter-ucsf/blob/master/paul/details_on_scripts.md).

Here is [my change-log](https://github.com/pauliwog/philter-ucsf/blob/master/paul/CHANGE_LOG.md) which should have everything I added or modified.

And [the README](https://github.com/pauliwog/philter-ucsf/blob/master/paul/README.md) for the "paul" folder gives an overview of what all my files are.

If you are curious and want to see what I did every day, you can check out [this google doc](https://docs.google.com/document/d/1R0CZyHlFhXny1KTAiDswyUyNCPmuKjYGK685wO2t_ug/edit?usp=sharing) with more of my planning and notes.

If any questions arise about my documentation, code, or really anything, feel free to email me at burke.invent@gmail.com (not a link it's just blue for some reason).

# What I did

### Overview
**Setup**
1. Got access to and downloaded clinical notes (MIMIC, i2b2).
2. Downloaded and set up Philter-Beta.
3. Got Philter-Zeta and set up a virtual python environment.

**Gene symbols project**
1. Found, downloaded, extracted, and converted a list of gene symbols to create a whitelist.
2. Made a list of the most common gene symbols, then searched for and copied MIMIC notes containing a common gene symbol to use as a test set of notes.
3. Ran these MIMIC notes through Philter (without the whitelist), compared before and after to find obscured gene symbols, then separated the notes with the obscured symbols.
    - If I ran Philter on a note and it obscured the gene symbol(s) in that note, then running Philter with the whitelist would hopefully rescue those symbols.
    - Whether Philter rescued the symbols or not would tell me how well the whitelist was working.
4. Downloaded and set up newest version of Philter because the beta version was buggy when using xml annotations.
5. Realized a big problem with the whitelist approach and created a safe regex to catch gene symbols before they got caught by phi regexes.
6. Merged my code with new latest version of Philter, then ran MIMIC notes with annotations through Philter, with and without my modifications and determined that the whitelist + safe regexes did work (after a couple edits)! I then sent my code off to get tested on UCSF data.
7. Edited the safe regex and whitelist based on the testing results from UCSF data and tested again until everything was working well.

**Pathology project**
1. Tried to find and download notes with pathology terms ([mtsamples](https://www.mtsamples.com/)), decided to use the MIMIC test set I created instead.
2. Created safe regexes or whitelists for staging terms, cassette (or slide) numbers, lymph nodes, and molecular markers.
3. Tested on MIMIC notes. Even though the notes didn't have the pathology terms I was trying to rescue, I could use the MIMIC notes to refine my regexes and make sure they didn't catch non-pathology terms.
5. Edited my safe regexes and whitelists, kept testing (eventually on UCSF data), rinse and repeat.

**Required libraries (some are built-in, the others can all be installed with pip or another package manager)**
1. ```argparse``` to provide options so users don't have to change variables in the script.
2. ```time``` to time how long scripts take to run.
3. ```pandas``` for using dataframes for a bunch of things.
4. ```os``` for interacting with files.
5. ```shutil``` also for interacting with files.
6. ```re``` for lots of things, generally extracting information.
7. ```json``` for reading and writing json files.
8. ```etree from lxml``` for extracting text between xml tags.
9. ```json_normalize from pandas.io.json``` to unpack nested json.


## A closer look at the setup
### Part 1
Obtained access to MIMIC and i2b2 data sets (I just followed the instructions on the site pages).
- [Link to MIMIC](https://mimic.physionet.org/gettingstarted/access/).
- [Link to i2b2](https://portal.dbmi.hms.harvard.edu/projects/n2c2-nlp/#).

### Part 2
I forked and set up a repository of the beta version of Philter on GitHub, [link](https://github.com/BCHSI/philter-ucsf) to the published Philter-Beta and [my repo](https://github.com/pauliwog/philter-ucsf)—my repo is not a fork of beta version, but a copy of the latest version of Philter + my modifications. Then I set up my Mac with Homebrew, python, etc—here's how I did it (all in Terminal.app).
1. Install command line tools: ```xcode-select --install```.
2. Install [Homebrew](https://brew.sh/): ```/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"```.
3. Update path for Homebrew : ```export PATH="/usr/local/opt/python/libexec/bin:$PATH"```.
4. Install python3, pip, setuptools, etc and create separate dir for python 3: ```brew install python3 && cp /usr/local/bin/python3 /usr/local/bin/python```.
5. Done! All the necessary tools have been installed, and python 3 is ready to be used. The commands ```python -V``` or ```python3 -V``` will display python versions. Use ```pip3 install <packagename>``` to install packages for python 3 (eg. ```pip3 install numpy```).

### Part 3
When I got Philter-Zeta, it came with a virtual environment, but it didn't work properly for me—my local file paths differed. So I learned how to set up a virtual python environment (referencing [this handy article](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-macos)). Again, if you're following in my steps or don't know, here's how to set a virtual environment up.
1. ```cd the/proj/dir``` or ```mkdir the/proj/dir && cd the/proj/dir``` to get to the directory you want to create the virtual environment in.
2. ```python3 -m venv python_env``` creates the virtual environment (python_env will be a new directory created in the current directory). This command also sets up the basic directories and files in the virtual environment.
3. ```source python_env/bin/activate``` will activate the virtual environment. Now your command line prompt should look like this ```(python_env) computer-name:path/to/somewhere$```. To deactivate the virtual environment, just simply type ```deactivate```.


## A closer look at the gene symbols project
### Part 1
1. There's this really nice website, [genenames.org](https://www.genenames.org/) (called HGNC), which has an easy, customizable form for downloading gene data ([link to form](https://biomart.genenames.org/martform/#!/default/HGNC?datasets=hgnc_gene_mart)). It takes the data from NCBI gene banks (or other places if you so choose). I downloaded all the gene symbols and names from NCBI, which included approved, alias, and previous symbols/names for each gene.

<table class="tg", style="float:right">
<caption>Example gene data from HGNC</caption>
<thead>
  <tr>
    <th class="tg-0pky">HGNC ID</th>
    <th class="tg-0pky">Status</th>
    <th class="tg-0pky">Approved symbol</th>
    <th class="tg-0pky">Previous symbol</th>
    <th class="tg-0pky">Alias symbol</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-0pky">HGNC:5</td>
    <td class="tg-0pky">Approved</td>
    <td class="tg-0pky">A1BG</td>
    <td class="tg-0pky">no data</td>
    <td class="tg-0pky">no data</td>
  </tr>
  <tr>
    <td class="tg-0pky">HGNC:37133</td>
    <td class="tg-0pky">Approved</td>
    <td class="tg-0pky">A1BG-AS1</td>
    <td class="tg-0pky">NCRNA00181</td>
    <td class="tg-0pky">FLJ23569</td>
  </tr>
  <tr>
    <td class="tg-0pky">HGNC:37133</td>
    <td class="tg-0pky">Approved</td>
    <td class="tg-0pky">A1BG-AS1</td>
    <td class="tg-0pky">A1BGAS</td>
    <td class="tg-0pky">FLJ23569</td>
  </tr>
  <tr>
    <td class="tg-0pky">HGNC:37133</td>
    <td class="tg-0pky">Approved</td>
    <td class="tg-0pky">A1BG-AS1</td>
    <td class="tg-0pky">A1BG-AS</td>
    <td class="tg-0pky">FLJ23569</td>
  </tr>
  <tr>
    <td class="tg-0pky">HGNC:24086</td>
    <td class="tg-0pky">Approved</td>
    <td class="tg-0pky">A1CF</td>
    <td class="tg-0pky">no data</td>
    <td class="tg-0pky">ACF</td>
  </tr>
  <tr>
    <td class="tg-0pky">HGNC:24086</td>
    <td class="tg-0pky">Approved</td>
    <td class="tg-0pky">A1CF</td>
    <td class="tg-0pky">no data</td>
    <td class="tg-0pky">ASP</td>
  </tr>
</tbody>
</table>

2. Once that was downloaded, I created a script ([HGNC_symbols_to_json.py](https://github.com/pauliwog/philter-ucsf/blob/master/paul/gene_symbols/HGNC_symbols_to_json.py)) to extract the gene symbols from the HGNC download and create a json file containing each symbol, in the correct format for Philter to use as a whitelist. This script read the HGNC list and used regex to extract the gene symbols from it.
3. Philter runs using a config file, which tells it what to do, and in what order. To get Philter to use the whitelist I created, I first duplicated the original config file and added a section at the bottom (more details in part 5) telling Philter to use the whitelist ([my test config file](https://github.com/pauliwog/philter-ucsf/blob/master/configs/philter_zeta_genes.json)). I chose to create a separate config file for testing because it is easy to switch between config files when running Philter (the ``` -f path/to/config/file.json``` option).

### Parts 2 and 3
1. Next, I wanted a test set of notes containing gene symbols, so I compiled a list of 35 common symbols ([common_symbols.txt](https://github.com/pauliwog/philter-ucsf/blob/master/paul/common_symbols.txt)) to search for in the MIMIC notes.
2. I then searched for those symbols in all the MIMIC notes using the Unix ```grep``` command and copied the notes containing the common symbols into a new directory.
```bash
   grep -l -r -w -f path/to/common_symbols.txt path/to/dir/containing/notes/to/search/in/ > path/to/output/file.txt
```
```bash
   for file in `cat path/to/output/file.txt`; do cp "$file" path/todir/where/you/want/the/files/containing/the/gene/symbols/to/go/ ; done
```
3. After this was done, I ended up with ~20,000 notes, and running 20,000 notes through Philter all at once would take weeks on my laptop (and I didn't have enough memory anyway), so I created a short script ([batch.py](https://github.com/pauliwog/philter-ucsf/blob/master/paul/scripts/batch.py)) which took the notes and batched them into folders containing the same number of notes each (I chose 1,000 notes per folder). I then ran these folders through original Philter (without the whitelist) five at a time. There's a reverse script to unbatch files which I created as well, [unbatch.py](https://github.com/pauliwog/philter-ucsf/blob/master/paul/scripts/unbatch.py). Here's the basic command I used to run Philter-Beta _(doesn't work for later versions of Philter)_.
```bash
    python3 batch.py -i path/to/dir/with/files/to/be/batched/ -o path/to/dir/where/batched/files/will/go/ -n number_of_files_per_batch
```
```bash
   python3 main.py -i path/to/input/dir/ -a path/to/xml(the annotations)/dir/ -o path/to/output/dir/ -f path/to/config/file.json -c path/to/coords/file.json -e False > path/to/output/file.txt
```
4. Next, I compared the before and after notes (before and after Philter annotations) to find the notes containing gene symbols obscured by Philter. These notes would become the test set for the whitelist. I originally designed my script which identified these obscured gene symbols to use another grep search, so sorry if you are duplicating my process—you're going to need to do another grep :disappointed: (or you could write your own script).
```bash
   grep -n -r -w -f common_symbols.txt dir/with/original/notes/ > path/to/another/output/file.txt
```
5. Using my script ([find_obscured_symbols.py](https://github.com/pauliwog/philter-ucsf/blob/master/paul/scripts/find_obscured_symbols.py)) and the grep search from the previous step, I went through all the MIMIC notes run through Philter (step 3) looking for notes containing obscured gene symbols. My script also has an option to copy the notes containing the symbols to a new directory, which I used. _Original_ means the notes which were input to Philter. _Annotated_ means the notes which have been run through Philter and have phi obscured with asterisks.
```bash
   python3 find_obscured_symbols.py -o path/to/dir/with/original/notes/ -a path/to/dir/with/annotated/notes/ -g path/to/grep/output/file/from/step/four.txt -s path/to/list/of/common_symbols.txt -c copy -d path/to/dir/where/notes/will/be/copied/to/
```

### Part 4 and 5
After trying for a while with Lakshmi's help to get Philter-Beta to accept the xml annotations so we could test the modifications, we decided to use the newest version of Philter instead, not wanting to mess too much with the beta version. This decision was also important because Philter-Zeta outputs more log and eval files, making it easier to see how the whitelists and safe regexes helped.

As described at the very top, the gene symbols whitelist had been inserted into the config file near the very end. However, when I ran Philter with the whitelist on my new test set, nothing changed. After some fiddling, Lakshmi told me to move the whitelist to the top of the config file and try again. This time, the gene symbols were not obscured! But...putting the whitelist at the beginning of the pipeline was dangerous, because the whitelist could catch real phi values and mark them as safe (false negatives) before the real phi could be caught by regular expressions later in the pipeline. For example, if somebody was named Ace, then their name would be marked as safe because it was in the whitelist (if the note was in all caps). So we definitely didn't want to put the whitelist at the front of the pipeline. It seemed like we had two other options, to edit the phi regexes catching the gene symbols, or to create a "safe" regex to tag gene symbols as safe.

The next logical step was to take a closer look at the regexes which were catching the symbols. To do so, I enabled the verbose option in Philter (```-v```) and added a print statement in philter.py so I could see the each regex and everything it caught. And when I subsequently ran Philter on several test notes, I found that multiple different regexes were catching the gene symbols :cry:. That meant to fix the problem I would have to edit multiple regexes. On top of that, some of them looked quite complicated.

So instead, I decided to create a safe regex, one that would catch the gene symbols and tag them as safe. To do so, I ran a grep search (another one) on the test notes so I could look at all the instances of gene symbols and find patterns which could be used to identify a symbol. Using those patterns, I created a regular expression to catch the gene symbols and mark them as safe. However, the regex which I was using to represent a gene symbol, ```[A-Z][A-Z0-9\-]+```, could also catch non-gene symbols, so to fix this problem I modified a piece of code a previous intern had written which would take regex containing a "variable" and replace that variable with a long list of something. In my case this was a list of gene symbols—much easier than editing a regular expression with 2000 lines of symbols! Here's the [transform_gene_symbols.py](https://github.com/pauliwog/philter-ucsf/blob/master/filters/regex/transform_gene_symbols.py) code, and the [regex with the variable](https://github.com/pauliwog/philter-ucsf/blob/master/filters/regex/gene_symbols/gene_symbols_safe_04.txt) and [without](https://github.com/pauliwog/philter-ucsf/blob/master/filters/regex/gene_symbols/gene_symbols_safe_04_transformed.txt).

This safe regex went at the top of the config file because it needed to get to the gene symbols before the phi regexes could. This placement was deemed safe because the regex was pretty specific and therefore unlikely to catch non-gene symbols or real phi.

### Part 6
I then tested my regex and whitelist on the MIMIC test set with annotations, tightened my regex based on the results, and eventually got everything working! Next, we wanted to test my additions to Philter on the UCSF data using the latest code, so I created a [change-log](https://github.com/pauliwog/philter-ucsf/blob/master/paul/CHANGE-LOG.md) so Lakshmi could merge my additions to the latest code (which wasn't allowed access to). Once the merge was completed, Lakshmi tested it on the UCSF data. The results were also good—of course after a couple little modifications.


## A closer look at the pathology terms project
### Part 1
Unfortunately, the MIMIC and i2b2 data sets didn't have any (or only very few) notes which contained the pathology terms which I would be attempting to recover. So, I went looking for more notes which had the pathology terms. Lakshmi had provided me with a website, [mtsamples.com](https://www.mtsamples.com/), but it only had eight pathology notes. I did some more searching and I didn't find anything better, which meant that once I was ready to test, the pathology regexes would have to be tested by Lakshmi on the UCSF notes. However, I could use the MIMIC test set I already had to refine my regexes before I tested on UCSF data.

### Parts 2, 3, 4, and 5
When I first started looking at the pathology terms, Lakshmi provided me with a couple examples for each type of term. She also gave me two potential safe regexes for staging terms and cassette numbers.
1. **Cassette or slide numbers.** [Link](https://github.com/pauliwog/philter-ucsf/blob/master/filters/regex/pathology/cassette_numbers_safe.txt) to safe regex. The provided regex was not super specific, and I'll spare you the details of figuring out how to get it properly working, but here's the general gist. When initially placed at the top of the config file, this safe regex caught some real phi while testing on UCSF data (for example "suite A40" or "room J3"). Looking closer, we discovered that many cassette numbers were caught by...not complete.
2. **Staging terms.** [Link](https://github.com/pauliwog/philter-ucsf/blob/master/filters/whitelists/whitelist_staging_terms.json) to whitelist. The provided regex wasn't bad—staging terms follow a pattern of characters, so it wasn't hard to create a regex to match them. But the complete list of staging terms was only 100 terms long, so I decided to create a whitelist to be sure that I was only matching staging terms. And because the staging terms were super unique (eg. pT4aN1aM1), this whitelist could go near the beginning of the pipeline without fear of mistakenly tagging a real phi as safe.
3. **Lymph nodes.** [Link](https://github.com/pauliwog/philter-ucsf/blob/master/filters/regex/pathology/lymph_nodes_safe.txt) to safe regex. Lymph nodes were pretty simple. Only having one example, I used my imagination to try to account for all the possibilities of these numbers, and created a safe regex which checked for a variation of the words "lymph nodes" before the match. As is obvious in the example below, the "(11/16)" following "lymph nodes" looks a lot like a date, which is why Philter was obscuring it. In fact, this particular example could actually be November 16th!
```
...in eleven of sixteen lymph nodes (11/16)...
```
4. **Molecular markers.** [Link](https://github.com/pauliwog/philter-ucsf/blob/master/filters/regex/pathology/molecular_markers_safe_transformed.txt) to safe regex. I was provided with two examples, one containing the protein "Ki-67", and the other the gene symbols "MLH1, MSH2, MSH6, and PMS2". When I tried to find a list of molecular markers, I generally got lists of proteins, which often included gene symbols or molecular markers in the descriptions. The whole thing was rather confusing—there wasn't really a good definition of what a "molecular marker" was, and I was lacking examples to create a good pattern based safe regex. So, in consultation with Lakshmi, I decided to reuse the gene symbols safe regex, although checking for different words surrounding the match. I based this regex off  the two examples I had. I used the same "replacing a variable with a list" technique as well.
    - [Human Protein Reference Database](http://www.hprd.org/).
    - [Protein Atlas](https://www.proteinatlas.org/search).
    - [Peptide Atlas](http://www.peptideatlas.org/#).
    - [Uniprot](https://www.uniprot.org/uniprot/) (I think this one is the best).

## Next steps
- **Make the gene symbols safe regex more efficient.**
- **Make the cassette numbers, lymph nodes, and molecular markers safe regexes better.**
- **Compile a better list for molecular markers.**

### Thats it!

I hope this is helpful—I had a lot of fun working on these projects!

Paul
