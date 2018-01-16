#
#  Copyright (c) 2015, Facebook, Inc.
#  All rights reserved.
#
#  This source code is licensed under the BSD-style license found in the
#  LICENSE file in the root directory of this source tree. An additional grant
#  of patent rights can be found in the PATENTS file in the same directory.
#
#  Author: Alexander M Rush <srush@seas.harvard.edu>
#          Sumit Chopra <spchopra@fb.com>
#          Jason Weston <jase@fb.com>

#/usr/bin/env python

import sys
import os
import re
import gzip
from nltk import word_tokenize, sent_tokenize
#@lint-avoid-python-3-compatibility-imports

# Make directory for output if it doesn't exist

try:
    os.mkdir(sys.argv[2] + "/" + sys.argv[1].split("/")[-2])
except OSError:
    pass

# Strip off .gz ending
end = "/".join(sys.argv[1].split("/")[-2:])[:-len(".gz")] + ".txt"

out = open(sys.argv[2] + end, "w")

# Parse and print titles and articles
NONE, HEAD, NEXT, TEXT = 0, 1, 2, 3
MODE = NONE
title_parse = ""
article_parse = []

def get_words(parse):
    words = []
    for w in parse.split():
        if w[-1] == ')':
            words.append(w.strip(")"))
            if words[-1] == ".":
                break
    return words

def remove_digits(parse):
    return re.sub(r'\d', '#', parse)

for l in gzip.open(sys.argv[1]):
    if MODE == HEAD:
        title_parse = word_tokenize(remove_digits(l.strip()))
        MODE = NEXT

    if MODE == TEXT and l.strip() != "</P>":
        article_parse.append(remove_digits(l.strip()))

    if MODE == NONE and l.strip() == "<HEADLINE>":
        MODE = HEAD

    if MODE == NEXT and l.strip() == "<P>":
        MODE = TEXT

    if MODE == TEXT and l.strip() == "</P>":
        try:
            articles = ''
            # Annotated gigaword has a poor sentence segmenter.
            # Ensure there is a least a period.

            for i in xrange(len(article_parse)):
                articles += article_parse[i] + ' '

            sentence = []
            for w in word_tokenize(articles):
                sentence.append(w)
                if w == '.':
                    break

            # article_parse = "(TOP " + " ".join(articles) + ")"

            # title_parse \t article_parse \t title \t article
            print >>out, "\t".join(['TP', 'AP',
                " ".join(title_parse),
                ' '.join(sentence)
                ])
        except:
            print articles
        finally:
            article_parse = []
            MODE = NONE
