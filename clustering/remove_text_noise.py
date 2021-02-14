import re

#remove https://...
#       www.....com
#       numbers
#       characters: ? ! " < > \ / % + , . : ( ) ‘ ’ &

NOISE_REGEX_PATTERN = '''(https:.+?\s)|(www\..+\.com?\s)|([\d]+)|[^\w\d\s]'''
COMMON_WORDS = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 'will', 'an', 'my', 'one', 'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'when', 'me', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take', 'person', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us']

COMMON_WORDS_PATTERN = "( the | be | to | of | and | a | in | that | have | i | it | for | not | on | with | he | as | you | do | at | this | but | his | by | from | they | we | say | her | she | or | will | an | my | one | all | would | there | their | what | so | up | out | if | about | who | get | which | go | when | me | make | can | like | time | no | just | him | know | take | person | into | year | your | good | some | could | them | see | other | than | then | now | look | only | come | its | over | think | also | back | after | use | two | how | our | work | first | well | way | even | new | want | because | any | these | give | day | most | us )"

def remove_text_noise(raw_text):
    cleaned = re.sub(NOISE_REGEX_PATTERN, "", raw_text)
    return cleaned

def remove_with_pattern(pattern, text):
    cleaned = re.sub(pattern, '', text)
    return cleaned 
    
def remove_common_words(raw_text):
    cleaned = re.sub(COMMON_WORDS_PATTERN, " ", raw_text)
    return cleaned
    