# -*- coding: utf-8 -*-
# Google, you autocomplete me
# A feature to add autocomplete code to the python interective shell
# Cristóbal Valenzuela

from __future__ import unicode_literals
from six import string_types
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit import prompt
import auto

class MyCompleter(Completer):
    def __init__(self, ignore_case=False, meta_dict=None, WORD=False, sentence=False, match_middle=False):
        assert not (WORD and sentence)
        self.ignore_case = ignore_case
        self.meta_dict = meta_dict or {}
        self.WORD = WORD
        self.sentence = sentence
        self.match_middle = match_middle

    def get_completions(self, document, complete_event):
        # Get word/text before cursor.
        if self.sentence:
            word_before_cursor = document.text_before_cursor
        else:
            word_before_cursor = document.get_word_before_cursor(WORD=self.WORD)

        for i in range(5):
            yield Completion(auto.completme(document.text_before_cursor, 3)) # call the

def main():
    completer = MyCompleter()
    text = prompt('> ', completer=completer, complete_while_typing=True)
    #print('You said: %s' % text)
    main()

if __name__ == '__main__':
    main()
