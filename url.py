#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Toolbox for URLs.
"""

__author__ = "Anthony Sigogne"
__copyright__ = "Copyright 2017, Byprog"
__email__ = "anthony@byprog.com"
__license__ = "MIT"
__version__ = "1.0"

import re
import requests
import unicodedata
from html import unescape

def crawl(url) :
    """
    Crawl an URL.
    Return URL data.
    """
    try :
        r = requests.get(url)
    except :
        return None
    return r

def extract_title(html) :
    """
    Extract the title of a page.
    """
    try :
        title = unescape(re.search("<title>([^<]+)</title>", html).group(1))
    except :
        title = "" # no title on page
    return title

def extract_description(html) :
    """
    Extract the description of a page.
    """
    try :
        description = unescape(re.search('<meta name="[^">]*description"[^">]*content="([^">]+)',html).group(1))
    except :
        description = "" # no description on page
    return description

# -- PIXEL WIDTH METHODS -- #

def remove_accents(input_str) :
    """
    Accents are not used in pixel width computation.
    """
    try :
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        only_ascii = nfkd_form.encode('ASCII', 'ignore')
        return only_ascii
    except :
        return input_str

def pixels(text, config) :
    """
    Compute pixels width of title or description.
    """
    return sum([config.get(letter,config.get(letter,5)) for letter in remove_accents(text.strip()).decode("utf8")])

def cut_pixels_google(text, max_pixels, config) :
    """
    Cut a text (title or description) to fit in pixel limits of Google serp.
    """
    cut_text = ""
    pixel_counter = 0
    for i, letter in enumerate(remove_accents(text.strip()).decode("utf8")) :
        pixel_counter += config.get(letter,config.get(letter,5))
        if pixel_counter > max_pixels :
            if letter == ' ' :
                return cut_text+"..."
            else :
                return cut_text.rsplit(' ',1)[0]+"..."
        cut_text += text[i]
    return cut_text
