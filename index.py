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

@app.route("/pixels", methods=['POST'])
def pixels_width():
    """
    URL : /pixels
    Compute pixels width and remaining width of a page title or description.
    Method : POST
    Form data :
        - text : your text
        - type : type of text ("title" or "description")
    Return a JSON dictionary : {"pixels":XX, "remaining":YY}
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
    data = dict((key, request.form.get(key)) for key in request.form.keys())
    if "text" not in data :
        raise InvalidUsage('No text specified in POST data')
    text = data.get("text", None)
    text_type = data.get("type", "title")
    if text_type not in ["title", "description"] :
        raise InvalidUsage('Type of text must be "title" or "description"')

    # compute pixels width and remaining width
    if not text :
        result = {"width":0, "remaining":config[text_type+"MaxPixels"]}
    else :
        width = sum([config.get(letter,config.get(letter,5)) for letter in remove_accents(text.strip()).decode("utf8")])
        result = {
            "pixels":width,
            "remaining":config[text_type+"MaxPixels"] - width
        }

    # return the result
    return jsonify(result)

@app.route("/")
def helper():
    """
    URL : /
    Helper that list all services of API.
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

class InvalidUsage(Exception):
    """
    Custom invalid usage exception.
    """
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    """
    JSON version of invalid usage exception
    """
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
