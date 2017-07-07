#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
API - compute the pixels width and remaining width of a title and/or description of page for Google SERP.

The goal of this tool is to optimize the writing of titles and descriptions of web pages.
If the title or description of your page is too long, Google will automatically cut it to a certain length and add "..." at the end.
This decreases the chance that a visitor will visit your site.

The source device used in this tool is a laptop with Chrome web browser (user agent) :
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36

In this configuration, the maximum width of the title is 554 pixels, and 1204 pixels for the description.
"""

__author__ = "Anthony Sigogne"
__copyright__ = "Copyright 2017, Byprog"
__email__ = "anthony@byprog.com"
__license__ = "MIT"
__version__ = "1.0"

import url
from flask import Flask, request, jsonify

# init flask app and import helper
app = Flask(__name__)
with app.app_context():
    from helper import *

# read desktop user agent config : Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36
config = {}
with open("config/pixel_config_chrome55_desktop.txt") as f :
    for line in f.readlines() :
        key, value = line.strip().rsplit("=",1)
        config[key] = int(value) if value.isdigit() else value

@app.route("/pixels", methods=['POST'])
def pixels_width_text():
    """
    URL : /pixels
    Compute pixels width and remaining width of a title or/and description.
    Method : POST
    Form data :
        - title : the title to analyze [string, required (if no description)]
        - description : the description to analyze [string, required (if no title)]
    Return width and remaining pixels for title and/or description.
    """
    # get POST data
    data = dict((key, request.form.get(key)) for key in request.form.keys())
    if "title" not in data and "description" not in data :
        raise InvalidUsage('No title and/or description in POST data')
    title = data.get("title", None)
    description = data.get("description", None)

    # compute pixels width and remaining width of title and description
    result = pixels_width(title, description)

    # return the result
    return jsonify(result)

@app.route("/pixels_url", methods=['POST'])
def pixels_width_url():
    """
    URL : /pixels_url
    Compute pixels width and remaining width of a page title and description.
    Method : POST
    Form data :
        - url : the url to analyze [string, required]
    Return width and remaining pixels for title and description.
    """
    # get POST data
    data = dict((key, request.form.get(key)) for key in request.form.keys())
    if "url" not in data :
        raise InvalidUsage('No URL in POST data')

    # get title and description in page
    url_data = url.crawl(data.get("url"))
    title = url.extract_title(url_data.text)
    description = url.extract_description(url_data.text)

    # compute pixels width and remaining width of title and description
    result = pixels_width(title, description)

    # return the result
    return jsonify(result)

def pixels_width(title, description) :
    """
    Compute pixels width and remaining width of a title or/and description.
    """
    result = {}

    # compute title width
    width = url.pixels(title, config)
    remaining = config["titleMaxPixels"] - width
    if remaining >= 0 :
        serp_title = title
    else :
        serp_title = url.cut_pixels_google(title, config["titleMaxPixels"], config)
    result["title"] = {
        "original_title":title,
        "serp_title":serp_title,
        "width":width,
        "remaining":remaining
    }

    # compute description width
    width = url.pixels(description, config)
    remaining = config["descriptionMaxPixels"] - width
    if remaining >= 0 :
        serp_description = description
    else :
        serp_description = url.cut_pixels_google(description, config["descriptionMaxPixels"], config)
    result["description"] = {
        "original_description":description,
        "serp_description":serp_description,
        "width":width,
        "remaining":remaining
    }

    return result
