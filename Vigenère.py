import re
from functools import reduce
import itertools
import freqAnalysis
from collections import defaultdict
# import requests
# from bs4 import BeautifulSoup

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

cipher_text = """
K Q O W E F V J P U J U U N U K G L M E K J I

N M W U X F Q M K J B G W R L F N F G H U D W

U U M B S V L P S N C M U E K Q C T E S W R E

E K O Y S S I W C T U A X Y O T A P X P L W P

N T C G O J B G F Q H T D W X I Z A Y G F F N

S X C S E Y N C T S S P N T U J N Y T G G W Z

G R W U U N E J U U Q E A P Y M E K Q H U I D

U X F P G U Y T S M T F F S H N U O C Z G M R

U W E Y T R G K M E E D C T V R E C F B D J Q

C U S W V B P N L G O Y L S K M T E F V J J T

W W M F M W P N M E M T M H R S P X F S S K F

F S T N U O C Z G M D O E O Y E E K C P J R G

P M U R S K H F R S E I U E V G O Y C W X I Z

A Y G O S A A N Y D O E O Y J L W U N H A M E

B F E L X Y V L W N O J N S I O F R W U C C E

S W K V I D G M U C G O C R U W G N M A A F F

V N S I U D E K Q H C E U C P F C M P V S U D

G A V E M N Y M A M V L F M A O Y F N T Q C U

A F V F J N X K L N E I W C W O D C C U L W R

I F T W G M U S W O V M A T N Y B U H T C O C

W F Y T N M G Y T Q M K B B N L G F B T W O J

F T W G N T E J K N E E D C L D H W T V B U V

G F B I J G Y Y I D G M V R D G M P L S W G J

L A G O E E K J O F E K N Y N O L R I V R W V

U H E I W U U R W G M U T J C D B N K G M B I

D G M E E Y G U O T D G G Q E U J Y O T V G G

B R U J Y S
"""

# message: text string
# key: key string in upper case
# encode: boolean, true for encode, false for decode
def v_cipher(message, key, encode):
    result_list = []
    for n in range(len(message)):
        place = LETTERS.find(message[n])
        if encode:
            place += LETTERS.find(key[n % len(key)])
        else:
            place -= LETTERS.find(key[n % len(key)])
        place %= len(LETTERS) # wraparound
        result_list.append(LETTERS[place])
    return ''.join(result_list)


# find the repeated letter combinations (3-5 letter length is sufficient)
# return a dict, key is the repeated combinations, value is the distance
# between the repeat
def repeat_combination(message):
    # dict to store repeated combination and distance
    c_dis = {}
    for keyword_length in range(3, 6):
        for i in range(len(message)):
            if i + keyword_length <= len(message):
                check_c = message[i:i + keyword_length]
                rest_message = message[i+keyword_length:]
                repeat_pos = rest_message.find(check_c)
                if repeat_pos > - 1 and check_c not in c_dis:
                    c_dis[check_c] = repeat_pos + keyword_length
    return c_dis


# guess the keywords length
# by sum the factors frequency
# return the length with the maximum counts as a factor
def keyword_len(message):
    combination_dict = repeat_combination(message)
    keyword_len_dict = {}
    for _, value in combination_dict.items():
        factors_set = factors(value)
        for f in factors_set:
            if f != 1:
                if f in keyword_len_dict:
                    keyword_len_dict[f] += 1
                elif f not in keyword_len_dict:
                    keyword_len_dict[f] = 1
    return max(keyword_len_dict, key=keyword_len_dict.get)


def factors(n):
    return set(reduce(list.__add__,
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

# def google_count(input_text):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'
#     }
#     r = requests.get("https://www.google.com/search", headers=headers, params={'q': input_text})
#     soup = BeautifulSoup(r.text, "lxml")
#     res = soup.find(id="result-stats")
#     return res.text


cipher_text = re.sub(r"[\n\t\s]*", "", cipher_text)
result_keyword_len = keyword_len(cipher_text)
sub_string_list_big = []
for i in range(result_keyword_len):
    sub_string_list = []
    for sub_i in range(i, len(cipher_text), result_keyword_len):
        sub_string_list.append(cipher_text[sub_i])
    sub_string_list_big.append(''.join(sub_string_list))

# for each sub_string find the top possible letters
decode26_dict = defaultdict(list)
for index, sub_string in enumerate(sub_string_list_big):
    # decode 26 times
    for letter in LETTERS:
        decode26_dict[index].append(v_cipher(sub_string, letter, False))

letter_freq = defaultdict(list)
for key, value in decode26_dict.items():
    for sub_s in value:
        freq = freqAnalysis.englishFreqMatchScore(sub_s)
        letter_freq[key].append(freq)
# print(letter_freq)
final_result = defaultdict(list)
for key, value in letter_freq.items():
    # print(value)
    max_value = max(value)
    for sub_i, sub_l in enumerate(value):
        if sub_l == max_value:
            final_result[key].append(LETTERS[sub_i])

for words in list(itertools.product(*final_result.values())):
    print(''.join(words), end='   ')
    print(v_cipher(cipher_text[:20], ''.join(words), False))

