# -*- coding: utf-8 -*-
"""
    Rzk lexer
    ~~~~~~~~~

    Pygments lexer for Rzk language (of proof assistant for synthetic ∞-categories).

    :copyright: Copyright 2023 Nikolai Kudasov
    :license: BSD 3, see LICENSE for details.
"""

import pygments.lexer
from pygments.lexer import bygroups
from pygments.token import *

__all__ = ["RzkLexer"]

class RzkLexer(pygments.lexer.RegexLexer):
    name = 'Rzk'
    aliases = ['rzk']
    filenames = ['*.rzk']
    url = 'https://github.com/fizruk/rzk'
    KEYWORDS = [] # ['as', 'uses']
    def get_tokens_unprocessed(self, text):
        for index, token, value in super(RzkLexer,self).get_tokens_unprocessed(text):
            if token is Name and value in self.KEYWORDS:
                yield index, Keyword, value
            else:
                yield index, token, value
    tokens = {
        'root': [
            (r'--.*\n', Comment),
            (r'^(#lang)(\s+)((?![-?!.])[^.\\;,#"\]\[)(}{><|\s]*)(?=$|[.\\;,#"\]\[)(}{><|\s])\s*$',
             bygroups(Name.Decorator, Punctuation, String)),
            (r'^(#check|#compute(-whnf|-nf)?|#set-option|#unset-option)(?=$|[.\\;,#"\]\[)(}{><|\s-])',
             bygroups(Name.Decorator)),
            (r'^(#section|#end)(\s+(?![-?!.])[^.\\;,#"\]\[)(}{><|\s]*)?(?=$|[.\\;,#"\]\[)(}{><|\s])',
             bygroups(Name.Decorator, Name.Entity)),
            (r'^(#assume|#variable|#variables)(\s+)((?![-?!.])[^.\\;,#"\]\[)(}{><|:]*)(?=$|[.\\;,#"\]\[)(}{><|\s])',
             bygroups(Keyword.Declaration, Punctuation, Name.Variable)),
            (r'^(#def|#define|#postulate)(\s+)((?![-?!.])[^.\\;,#"\]\[)(}{><|\s]*)(?=$|[.\\;,#"\]\[)(}{><|\s])((\s+)(uses)(\s+\()((?![-?!.])[^.\\;,#"\]\[)(}{><|]*)(\)))?',
             bygroups(Keyword.Declaration, Punctuation, Name.Function, None, Punctuation, Keyword, Punctuation, Name.Variable, Punctuation)),

            # bultins
            (r'(?<=[.\\;,#"\]\[)(}{><|\s])(CUBE|TOPE|U(nit)?|𝒰)(?=$|[.\\;,#"\]\[)(}{><|\s])',
             Keyword.Type),
            (r'(?<=[.\\;,#"\]\[)(}{><|\s])(1|2|𝟙|𝟚|Sigma|∑|Σ)(?=$|[.\\;,#"\]\[)(}{><|\s])',
             Keyword.Type),
            (r'(===|<=|\\/|/\\)',
             Operator),
            (r'(⊤|⊥|\*_1|⋆)|(?<=[.\\;,#"\]\[)(}{><|\s])(0_2|1_2|TOP|BOT)(?=$|[.\\;,#"\]\[)(}{><|\s])',
             Name.Constant),
            (r'(?<=[.\\;,#"\]\[)(}{><|\s])(recOR|rec∨|recBOT|rec⊥|idJ|refl|first|second|π₁|π₂|unit)((?=$|[.\\;,#"\]\[)(}{><|\s])|(?=_{))',
             Name.Constant),
            (r'(?<=[.\\;,#"\]\[)(}{><|\s])as(?=$|[.\\;,#"\]\[)(}{><|\s])',
             Keyword),

            # parameters
            (r'(\(\s*)([^{:\)]+\s*)(:)(?=$|[.\\;,#"\]\[)(}{><|\s])',
             bygroups(Punctuation, Name.Variable, Punctuation)),

            (r'"', String, 'string'),

            (r'(\\\s*)((([^\t\n\r !"#\(\),-\.;:\\\/=<>\?\[\\\]\{\|\}][^\t\n\r !"#\(\),\.;:<>\?\[\\\]\{\|\}]*)\s*)+)',
                bygroups(Punctuation, Name.Variable)),
        ],
        'string': [
            (r'[^"]+', String),
            (r'"', String, '#pop'),
        ],
    }
