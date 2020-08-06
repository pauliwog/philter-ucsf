import re

with open("../filters/regex/genes_and_patho_terms/gene_symbols_safe_transformed.txt") as fin:
    test_regex = re.compile(fin.read())

# with open("../filters/regex/genes_and_patho_terms/cassette_numbers_safe.txt") as fin:
#     test_regex = re.compile(fin.read())

# test_string = """True positives in dir1 and not dir2:
#
# filepath:	'./data/i2b2/i2b2_notes/157-02.txt'
# phi_type:	'AGE'
# match:	'54'
# start:	'28'
# stop:	'29'
# match in context:	''
#
#
# filepath:	'./data/i2b2/i2b2_notes/180-01.txt'
# phi_type:	'DATE'
# match:	'July'
# start:	'758'
# stop:	'761'
# with meals,
# Erythropoietin, Premarin and Provera, Nephrox 150 mg tid, insulin
# NPH 10 units qam.
# On July 17, after hemodialysis, Ms. Tinsley was given a partial
# dose of Vancomycin and developed pruritus.
#
#
# filepath:	'./data/i2b2/i2b2_notes/300-01.txt'
# phi_type:	'DOCTOR'
# match:	'ostrowski'
# start:	'1928'
# stop:	'1936'
# minimal anemia but with drop over past 4 months.
#
# ALLERGIES:
# No Known Drug Allergies 05/21/2087 ostrowski
#
# MEDICATIONS:
# Lidex cream No Match bid prn up to 2 week : 01/09/2087 - 02/02/2090 ACT : ostr
#
#
# filepath:	'./data/i2b2/i2b2_notes/300-02.txt'
# phi_type:	'DOCTOR'
# match:	'ostrowski'
# start:	'2178'
# stop:	'2186'
# sis w ? diverticulitis ? SBO resolved
# GERD.
#
# ALLERGIES:
# No Known Drug Allergies 05/21/2087 ostrowski
#
# MEDICATIONS:
# CIPRO 500MG PO bid : 12/01/2089 - 02/02/2090 ACT : ostrowski
# Script: Amt:'
#
#
# filepath:	'./data/i2b2/i2b2_notes/329-04.txt'
# phi_type:	'PATIENT'
# match:	'Ursula'
# start:	'536'
# stop:	'541'
# titration at home. As patient is currently very somnolent this history is based on phone interview with Ursula Jacks who is the HCP and is very involved with his father's care. The patient was diagnosed with
#
#
# filepath:	'./data/i2b2/i2b2_notes/332-05.txt'
# phi_type:	'HOSPITAL'
# match:	'EFS'
# start:	'10278'
# stop:	'10280'
# ng recs, discuss with family in AM
# _______________________________________
# Brandon Hale
# EFS III, Internal Medicine
# Pager #28913
# ADDENDUM:
# Case and plan discussed and incorporated into this
#
#
# filepath:	'./data/i2b2/i2b2_notes/355-03.txt'
# phi_type:	'PROFESSION'
# match:	'manaager'
# start:	'2609'
# stop:	'2616'
# Qam
# Social History:
# Lifestyle -on disability secondary to tarditive dyskinesia, used to be a manaager, is married with three children ages 3, 6, 9 yrs
# Tobacco -none
# Alcohol -occasionally, last drink
#
#
# filepath:	'./data/i2b2/i2b2_notes/396-04.txt'
# phi_type:	'PATIENT'
# match:	'Brendon'
# start:	'1699'
# stop:	'1705'
# anemia of renal disease. She was discharged to Lahey Clinic and has just returned home. Her son, Brendon Ambrose who was the healthcare proxy, is here with her today.
# Today, she feels reasonably well.
#
#
#
# True positives in dir2 and not dir1:
#
# filepath:	'./data/i2b2/i2b2_notes/300-01.txt'
# phi_type:	'DOCTOR'
# match:	'ostrow'
# start:	'1928'
# stop:	'1933'
# nimal anemia but with drop over past 4 months.
#
# ALLERGIES:
# No Known Drug Allergies 05/21/2087 ostrowski
#
# MEDICATIONS: Lidex cream No Match bid prn up to 2 week : 01/09/2087 - 02/02/2090 ACT : o
#
#
# filepath:	'./data/i2b2/i2b2_notes/300-02.txt'
# phi_type:	'DOCTOR'
# match:	'ostrow'
# start:	'2178'
# stop:	'2183'
# sis w ? diverticulitis ? SBO resolved GERD.
#
# ALLERGIES: No Known Drug Allergies 05/21/2087 ostrowski
#
# MEDICATIONS: CIPRO 500MG PO bid : 12/01/2089 - 02/02/2090 ACT : ostrowski
# Script: A"""

# test_string = "make sure to hold ace2 until tomorrow"
# test_string = "ith meals,\nErythropoietin, Premarin and Provera, Nephrox 150 mg tid, insulin\nNPH 10 units qam.\n \nOn July 17, after hemodialysis, Ms. Tinsley was given a partial\ndose of Vancomycin and developed pruritus."
# test_string = "nimal anemia but with drop over past 4 months.\n\n\n\n\n\nALLERGIES: \n\nNo Known Drug Allergies 05/21/2087 ostrowski\n\n\n\n\n\nMEDICATIONS: \n\nLidex cream No Match bid prn up to 2 week : 01/09/2087 - 02/02/2090 ACT : ostr"
test_string = """




Record date: 2081-02-06

54 yo for CPE



MEDICATIONS



FOLIC ACID      Tablet(s) PO

VIT C (ASCORBIC ACID)      Capsule(s) PO


"""

print(test_regex.findall(test_string))
