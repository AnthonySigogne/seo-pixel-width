#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
API to compute the pixel width and remaining width of a page title or description for Google SERP according to source device (laptop, mobile,...).
The goal of this tool is to optimize the writing of titles and descriptions of web pages.

The source device used in this tool is a laptop with Chrome web browser :
user agent -> Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36

In this configuration, the maximum width of the title is 588 pixels, and 1250 pixels for the description.
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

@app.route("/width", methods=['POST'])
def pixels_width():
    """
    URL : /width
    Compute pixels width and remaining width of a page title or description.
    Method : POST
    Form data :
        - text : your text
        - type : type of text ("title" or "description")
    Return a JSON dictionary with two keys : {"width":XX, "remaining":YY}
    """
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
    # get POST data
    text = request.form.get("text", None)
    text_type = request.form.get("type", "title")

    # compute pixels width and remaining width
    if not text :
        result = {"width":0, "remaining":config[text_type+"MaxPixels"]}
    else :
        width = sum([config.get(letter,config.get(letter,5)) for letter in remove_accents(text.strip()).decode("utf8")])
        result = {
            "width":width,
            "remaining":config[text_type+"MaxPixels"] - width
        }

    # return the result (json dict)
    return jsonify(result)

@app.route("/")
def helper():
    """
    URL : /
    Helper that list all methods of tool.
    Return a simple text.
    """
    # print module docstring
    output = [__doc__.replace("\n","<br/>"),]

    # then, get and print docstring of each rule
    for rule in app.url_map.iter_rules():
        if rule.endpoint == "static" : # skip static endpoint
            continue
        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)
        methods = ','.join(rule.methods)
        output.append(app.view_functions[rule.endpoint].__doc__.replace("\n","<br/>"))

    return "<br/>".join(output)
