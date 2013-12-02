from flask import Flask, jsonify, render_template
import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs
import settings

app = Flask(__name__)

@app.route("/")
def get():
    """
        Return the main page with the most recent status populated
    """
    return get_by_index(0)

@app.route("/<int:index>/")
def get_by_index(index):
    """
        Return the main page with the nth most recent status populated
    """
    statuses = retrieve_statuses()
    last_post = statuses[index]
    image = choose_image(last_post)
    model = {"title": "Twitter Feed", 
            "status":last_post,
            "image":image,
    }
    return render_template('index.html', **model)

@app.route("/last/")
def get_last_status():
    """
        Get JSON record of last status
    """
    statuses = retrieve_statuses()
    return jsonify(statuses[0])

@app.route("/last/<int:index>")
def get_status_by_index(index):
    """
        Get JSON record of nth last status
    """
    statuses = retrieve_statuses()
    return jsonify(statuses[index])

def retrieve_statuses():
    request = requests.get(url=settings.TWITTER_ENDPOINT, auth=get_oauth())
    print request.headers
    return request.json()['statuses']

def choose_image(status):
    media = status["entities"].get("media", None)
    if media:
        targeted_media = media[0]
        image = {
                    "url" : targeted_media["media_url"]+":large",
                    "width": targeted_media["sizes"]["large"]["w"],
                    "height": targeted_media["sizes"]["large"]["h"],
                }
    else:
        image = {}
    return image

def get_oauth():
    oauth = OAuth1(settings.CONSUMER_KEY,
                client_secret=settings.CONSUMER_SECRET)
    return oauth

if __name__ == "__main__":
    app.run(debug=settings.DEBUG)