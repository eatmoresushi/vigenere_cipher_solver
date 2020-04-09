import matplotlib.pyplot as plt
import re
from collections import Counter
from itertools import combinations

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
COMMON_BIGRAM = ['th','er','on','an','re','he','in','ed','nd','ha','at','en','es','of','or','nt','ea','ti','to','it','st','io','le','is','ou','ar','as','de','rt','ve']

cipher_text = '''
OCOYFOLBVNPIASAKOPVYGESKOVMUFGUWMLNOOEDRNCFORSO
CVMTUUTYERPFOLBVNPIASAKOPVIVKYEOCNKOCCARICVVLTS
OCOYTRFDVCVOOUEGKPVOOYVKTHZSCVMBTWTRHPNKLRCUEGM
SLNVLZSCANSCKOPORMZCKIZUSLCCVFDLVORTHZSCLEGUXMI
FOLBIMVIVKIUAYVUUFVWVCCBOVOVPFRHCACSFGEOLCKMOCG
EUMOHUEBRLXRHEMHPBMPLTVOEDRNCFORSGISTHOGILCVAIO
AMVZIRRLNIIWUSGEWSRHCAUGIMFORSKVZMGCLBCGDRNKCVC
PYUXLOKFYFOLBVCCKDOKUUHAVOCOCLCIUSYCRGUFHBEVKRO
ICSVPFTUQUMKIGPECEMGCGPGGMOQUSYEFVGFHRALAUQOLEV
KROEOKMUQIRXCCBCVMAODCLANOYNKBMVSMVCNVROEDRNCGE
SKYSYSLUUXNKGEGMZGRSONLCVAGEBGLBIMORDPROCKINANK
VCNFOLBCEUMNKPTVKTCGEFHOKPDULXSUEOPCLANOYNKVKBU
OYODORSNXLCKMGLVCVGRMNOPOYOFOCVKOCVKVWOFCLANYEF
VUAVNRPNCWMIPORDGLOSHIMOCNMLCCVGRMNOPOYHXAIFOOUEPGCHK
'''

def getLetterCount(message):
    # Returns a dictionary with keys of single letters and values of the
    # count of how many times they appear in the message parameter:
    letterCount = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}

    for letter in message.upper():
        if letter in LETTERS:
            letterCount[letter] += 1

    return letterCount

def getBiLetterCount(message):
    words = re.sub('\W', '', message)
    words = re.findall("\w\w",
                       words)

    return Counter(words)


single_count = getLetterCount(cipher_text) # noticed no letter 'J'
bi_count = getBiLetterCount(cipher_text) # assume OC = th, OY and FO in commonest list
all_comb = list(combinations(COMMON_BIGRAM, 4)) # check all combinations, mainly look at those starts with th
print(bi_count)
for c in all_comb:
    if c[0] == 'th':
        print(''.join(c))
