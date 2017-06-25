# seo-pixel-width
API to compute the pixel width and remaining width of a page title or description for Google SERP according to source device (laptop, mobile,...).

The goal of this tool is to optimize the writing of titles and descriptions of web pages. If the title or description of your page is too long, Google will automatically cut it to a certain length and add "..." at the end. This decreases the chance that a visitor will visit your site.

The source device used in this tool is a laptop with Chrome web browser :
user agent -> Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36

In this configuration, the maximum width of the title is 588 pixels, and 1250 pixels for the description.

## INSTALL
```
pip install -r requirements.txt
FLASK_APP=index.py flask run
```

To launch in debug mode :
```
FLASK_APP=index.py FLASK_DEBUG=1 flask run
```

## USAGE
To list services of API, type this endpoint in your web browser : "http://localhost:5000/"

## GOOGLE SERP
Below, a sample of Google SERP. The title and description of the first result have been cut by Google, while the third result is perfect .

![Google SERP](images/google.png?raw=true "Google SERP" )
