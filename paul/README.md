# A couple notes
- Some of the code in this directory was created to work with Philter-Beta, so it might require adjustment to work with this newer version of Philter
- Here's a [link](https://github.com/pauliwog/philter-data) to the data I used
- ```DOCUMENTATION.md``` is, funnily enough, my documentation :grin:
- ```CHANGE-LOG.md``` contains everything I modified/added
- ```blank.json``` is a blank json file just in case I needed it
- ```common_symbols.txt``` contains the symbols I used to find my test set of MIMIC clinical notes
- ```find_obscured_symbols.py``` will compare before and after notes (before and after Philter annotations) and identify and copy notes which have obscured gene symbols
- ```find_unobscured_symbols.py``` will compare unmodified and modified notes (annotated with and without whitelists/regexes) and identify notes which have symbols which are no longer obscured
