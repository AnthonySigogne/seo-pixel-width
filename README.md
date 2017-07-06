# seo-pixel-width
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) ![Python 2.7](https://img.shields.io/badge/python-3.5-blue.svg)

API - compute the pixels width and remaining width of a title and/or description of page for Google SERP.

The goal of this tool is to optimize the writing of titles and descriptions of web pages. If the title or description of your page is too long, Google will automatically cut it to a certain length and add "..." at the end. This decreases the chance that a visitor will visit your site.

The source device used in this tool is a standard laptop with Chrome web browser (user agent) :
```
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36
```

In this configuration, the maximum width of the title is 588 pixels, and 1250 pixels for the description.

## INSTALL AND RUN

### REQUIREMENTS
This tool requires *Python3*.

### WITH PIP
```
git clone https://github.com/AnthonySigogne/seo-pixel-width.git
cd seo-pixel-width
pip install -r requirements.txt
```

Then, run the tool :
```
FLASK_APP=index.py flask run
```

To run in debug mode, prepend `FLASK_DEBUG=1` to the command :
```
FLASK_DEBUG=1 ... flask run
```

### WITH DOCKER
To run the tool with Docker, you can use my DockerHub image :
https://hub.docker.com/r/anthonysigogne/seo-pixel-width/
```
docker run -p 5000:5000 anthonysigogne/seo-pixel-width
```

Or, build yourself a Docker image :
```
git clone https://github.com/AnthonySigogne/seo-pixel-width.git
cd seo-pixel-width
docker build -t seo-pixel-width .
```

## USAGE AND EXAMPLES
To list all services of API, type this endpoint in your web browser : http://localhost:5000/

### FROM A TEXT (TITLE AND/OR DESCRIPTION)
Compute pixels width and remaining width of a title or/and description.

* **URL**

  /pixels

* **Method**

  `POST`

* **Form Data Params**

  **Required (title and/or description):**

  `title=[string]`, the title to analyze  
  `description=[string]`, the description to analyze  

* **Success Response**

  * **Code:** 200 <br />
    **Content:**
    ```
    {
      "description": {
        "pixels": 646,
        "remaining": 604
      },
      "title": {
        "pixels": 413,
        "remaining": 175
      }
    }
    ```

* **Error Response**

  * **Code:** 400 INVALID USAGE <br />


* **Sample Call (with cURL)**

  ```
  curl -X POST -F "description=Full-Stack Developer specialized in new technologies and innovative IT solutions." -F "title=Anthony Sigogne / Freelance / Full-Stack Developer" "http://localhost:5000/pixels"
  ```

### FROM AN URL
Compute pixels width and remaining width of a page title and description.

* **URL**

  /pixels_url

* **Method**

  `POST`

* **Form Data Params**

  **Required:**

  `url=[string]`, the url to analyze  

* **Success Response**

  * **Code:** 200 <br />
    **Content:**
    ```
    {
      "description": {
        "pixels": 1303,
        "remaining": -53
      },
      "title": {
        "pixels": 482,
        "remaining": 106
      }
    }
    ```

* **Error Response**

  * **Code:** 400 INVALID USAGE <br />


* **Sample Call (with cURL)**

  ```
  curl -X POST -F "url=https://www.lemonde.fr" "http://localhost:5000/pixels_url"
  ```

## FUTURE FEATURES
* nothing ?

## LICENCE
MIT
