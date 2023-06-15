import unicodedata

SENT_END_SIGN = set('。！？……')
SENT_SPLIT_SIGN = set('，')

def split_sentence(text):  
    sents = []
    cur_sent = ''
    for ch in text:
        cur_sent += ch
        if ch in SENT_END_SIGN:
            if len(cur_sent.strip()) > 0:
                sents.append(cur_sent.strip())
            cur_sent = ''
    if len(cur_sent.strip()) > 0:
        sents.append(cur_sent.strip())
    # print(sents)
    return sents


def is_whitespace(char):
    """Checks whether `char` is a whitespace character."""
    # \t, \n, and \r are technically control characters but we treat them
    # as whitespace since they are generally considered as such.
    if char == " " or char == "\t" or char == "\n" or char == "\r":
        return True
    cat = unicodedata.category(char)
    if cat == "Zs":
        return True
    return False


def is_control(char):
    """Checks whether `char` is a control character."""
    # These are technically control characters but we count them as whitespace
    # characters.
    if char == "\t" or char == "\n" or char == "\r":
        return False
    cat = unicodedata.category(char)
    if cat.startswith("C"):
        return True
    return False


def is_punctuation(char):
    """Checks whether `char` is a punctuation character."""
    cp = ord(char)
    # We treat all non-letter/number ASCII as punctuation.
    # Characters such as "^", "$", and "`" are not in the Unicode
    # Punctuation class but we treat them as punctuation anyways, for
    # consistency.
    if (cp >= 33 and cp <= 47) or (cp >= 58 and cp <= 64) or (cp >= 91 and cp <= 96) or (cp >= 123 and cp <= 126):
        return True
    cat = unicodedata.category(char)
    if cat.startswith("P"):
        return True
    return False


def is_end_of_word(text):
    """Checks whether the last character in text is one of a punctuation, control or whitespace character."""
    last_char = text[-1]
    return bool(is_control(last_char) | is_punctuation(last_char) | is_whitespace(last_char))


def is_start_of_word(text):
    """Checks whether the first character in text is one of a punctuation, control or whitespace character."""
    first_char = text[0]
    return bool(is_control(first_char) | is_punctuation(first_char) | is_whitespace(first_char))

def is_chinese_char(text):
    """Checks whether CP is the codepoint of a CJK character."""
    # This defines a "chinese character" as anything in the CJK Unicode block:
    #   https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_(Unicode_block)
    #
    # Note that the CJK Unicode block is NOT all Japanese and Korean characters,
    # despite its name. The modern Korean Hangul alphabet is a different block,
    # as is Japanese Hiragana and Katakana. Those alphabets are used to write
    # space-separated words, so they are not treated specially and handled
    # like the all of the other languages.
    cp = ord(text)
    if (
        (cp >= 0x4E00 and cp <= 0x9FFF)
        or (cp >= 0x3400 and cp <= 0x4DBF)  #
        or (cp >= 0x20000 and cp <= 0x2A6DF)  #
        or (cp >= 0x2A700 and cp <= 0x2B73F)  #
        or (cp >= 0x2B740 and cp <= 0x2B81F)  #
        or (cp >= 0x2B820 and cp <= 0x2CEAF)  #
        or (cp >= 0xF900 and cp <= 0xFAFF)
        or (cp >= 0x2F800 and cp <= 0x2FA1F)  #
    ):  #
        return True

    return False

def split_word(text):
    text = text.strip()
    words = []
    word = ''
    for ch in text:
        if is_chinese_char(ch):
            if word != '':
                words.append(word)
                word = ''
            words.append(ch)
        elif ch.isalpha() or ch.isdigit():
            word += ch
        elif is_end_of_word(ch):
            if word != '':
                words.append(word)
                word = ''
            if is_punctuation(ch):
                words.append(ch)
    if word != '':
        words.append(word)
        word = ''
    return words

def is_chinese_sentence(text):
    words = split_word(text)
    cnt = 0
    for word in words:
        if len(word) == 1 and (is_chinese_char(word) or is_punctuation(word)):
            cnt += 1
    return cnt * 1. / len(words) > .7

def split_sentence_short(text): # 切成短文本，逗号分隔
    '''
    input='如果你想拥有一款高效保湿的面霜，'那么科颜氏高保湿霜绝对是你的不二选择。'
    output=['如果你想拥有一款高效保湿的面霜，', '那么科颜氏高保湿霜绝对是你的不二选择。']
    '''
    sents_split = []
    cur_sent = ''
    for ch in text:
        cur_sent += ch
        if ch in SENT_SPLIT_SIGN:
            if len(cur_sent.strip()) > 0:
                sents_split.append(cur_sent.strip())
            cur_sent = ''
    # print('cur_sent',cur_sent)
    if len(cur_sent.strip()) > 0:
        sents_split.append(cur_sent.strip())
    # print('sents_split---', sents_split)
    return sents_split 

def split_word_from_asr(sentence):
    ret = []
    for word in sentence["words"]:
        if len(word["text"]) == 1:
            ret.append(Word(word["text"],int(word["begin_time"]),int(word["end_time"])))
        elif len(word["text"]) > 1:
            i = 0
            init_start = int(word["begin_time"])
            init_end = int(word["end_time"])
            word_cost = int((init_end - init_start) / len(word["text"]))
            while i <= len(word["text"]) - 1:
                if i == 0:
                    char = word["text"][i]
                    end = init_start + word_cost 
                    if char != ' ':
                        ret.append(Word(char,init_start,end))
                    start = end 
                elif 0 < i < len(word["text"])-1:
                    char = word["text"][i]
                    end = start + word_cost
                    if char != ' ':
                        ret.append(Word(char,start,end)) 
                elif i == len(word["text"]) - 1:
                    char = word["text"][i]
                    if char != ' ':
                        ret.append(Word(char,start,init_end))
                i += 1
    
    return ret 

