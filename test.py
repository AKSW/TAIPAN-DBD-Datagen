import re

_camel_case_string = "isTopicOf"
_camel_string_regex = re.compile(r"([A-Z])")
_token_list = _camel_string_regex.split(_camel_case_string)

_word_list = [_token_list[0]]
for i, _ in enumerate(_token_list):
    if i % 2 == 1:
        word = "".join([_token_list[i], _token_list[i + 1]])
        _word_list.append(word)

import ipdb; ipdb.set_trace()
