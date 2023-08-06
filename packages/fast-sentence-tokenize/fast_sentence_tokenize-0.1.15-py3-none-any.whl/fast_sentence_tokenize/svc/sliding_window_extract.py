#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Simple Sliding Window N-Gram Extractor """


from typing import List

from baseblock import BaseObject, TextUtils


class SlidingWindowExtract(BaseObject):
    """ Simple Sliding Window N-Gram Extractor """

    def __init__(self):
        """ Change Log

        Created:
            26-Oct-2022
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)

    def process(self,
                tokens: List[str],
                gram_level: int,
                skip_gram: bool = False) -> list:
        """ Extract Bigrams

        Args:
            tokens (List[str]): the incoming tokens
            gram_level (int): the gram level to extract at
            skip_gram (bool, False): skip every other gram. Defaults to False.

        Returns:
            list: a list of bigrams (or skipgrams)
        """

        if not skip_gram:
            return TextUtils.sliding_window(
                tokens=tokens,
                window_size=gram_level)

        tokens_even = []
        tokens_odd = []

        for i in range(len(tokens)):
            if i % 2 != 0:
                tokens_odd.append(tokens[i])
            else:
                tokens_even.append(tokens[i])

        grams_odd = TextUtils.sliding_window(
            tokens=tokens_odd,
            window_size=gram_level)

        grams_even = TextUtils.sliding_window(
            tokens=tokens_even,
            window_size=gram_level)

        return grams_odd + grams_even
