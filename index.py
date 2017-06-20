#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Compute the pixels size and remaining size of a page title or description for Google SERP according to source device (user agent).
This tool is configured for a standard laptop device using Chrome web browser :
user agent Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36
"""

__author__ = "Anthony Sigogne"
__copyright__ = "Copyright 2017, Byprog"
__email__ = "anthony@byprog.com"
__license__ = "MIT"
__version__ = "1.0"

# libraries of tool
import unicodedata
import urllib
from flask import Flask, request, jsonify, url_for
app = Flask(__name__)

# read default user agent config : Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36
config = {}
with open("config/pixel_config_chrome55_desktop.txt") as f :
    for line in f.readlines() :
        key, value = line.strip().rsplit("=",1)
        config[key] = int(value) if value.isdigit() else value

@app.route("/size", methods=['POST'])
def pixels_size():
    """
    URL : /size
    Compute pixels size and remaining size of a title or description.
    Method : POST
    Form data :
        - text : your text
        - type : type of text ("title" or "description")
    Return a JSON dictionary with two keys : {"size":XX, "remaining":YY}
    """
    def remove_accents(input_str) :
        """
        Accents are not used in pixel size computation.
        """
        try :
            nfkd_form = unicodedata.normalize('NFKD', input_str)
            only_ascii = nfkd_form.encode('ASCII', 'ignore')
            return only_ascii
        except :
            return input_str
    # get POST data
    text = request.form.get("text", None)
    text_type = request.form.get("type", "title")

    # compute pixels size and remaining
    if not text :
        result = {"size":0, "remaining":config[type_text+"MaxPixels"]}
    else :
        size = sum([config.get(letter,config.get(letter,5)) for letter in remove_accents(text.strip()).decode("utf8")])
        result = {
            "size":size,
            "remaining":config[text_type+"MaxPixels"] - size
        }

    # return the result (json dict) to request source
    return jsonify(result)

@app.route("/")
def helper():
    """
    URL : /
    Helper that list all methods of tool.
    Return a simple text.
    """
    output = [__doc__.replace("\n","<br/>"),]
    for rule in app.url_map.iter_rules():
        if rule.endpoint == "static" : # skip static endpoint
            continue
        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)
        methods = ','.join(rule.methods)
        output.append(app.view_functions[rule.endpoint].__doc__.replace("\n","<br/>"))
    return "<br/>".join(output)
