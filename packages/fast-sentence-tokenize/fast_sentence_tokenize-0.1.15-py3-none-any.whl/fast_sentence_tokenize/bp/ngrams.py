#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Simple Sliding Window N-Gram Extractor """


from typing import List

from baseblock import BaseObject, Enforcer

from fast_sentence_tokenize.svc import SlidingWindowExtract

extract_ngrams = SlidingWindowExtract().process


class NGrams(BaseObject):
    """ Simple Sliding Window N-Gram Extractor """

    def __init__(self,
                 tokens: List[str]):
        """ Change Log

        Created:
            26-Oct-2022
            craigtrim@gmail.com

        Args:
            tokens (List[str]): the incoming tokens
        """
        BaseObject.__init__(self, __name__)
        if self.isEnabledForDebug:
            Enforcer.is_list_of_str(tokens)

        self._tokens = tokens

    def bigrams(self,
                skip_gram: bool = False) -> list:
        """ Extract Bigrams

        Args:
            skip_gram (int, optional): skip every N grams. Defaults to 0.

        Returns:
            list: a list of bigrams (or skipgrams)
        """
        return extract_ngrams(tokens=self._tokens,
                              gram_level=2,
                              skip_gram=skip_gram)

    def trigrams(self,
                 skip_gram: bool = False) -> list:
        """ Extract Trigrams

        Args:
            skip_gram (int, optional): skip every N grams. Defaults to 0.

        Returns:
            list: a list of trigrams (or skipgrams)
        """
        return extract_ngrams(tokens=self._tokens,
                              gram_level=3,
                              skip_gram=skip_gram)

    def quadgrams(self,
                  skip_gram: bool = False) -> list:
        """ Extract Quadgrams

        Args:
            skip_gram (int, optional): skip every N grams. Defaults to 0.

        Returns:
            list: a list of quadgrams (or skipgrams)
        """
        return extract_ngrams(tokens=self._tokens,
                              gram_level=4,
                              skip_gram=skip_gram)
