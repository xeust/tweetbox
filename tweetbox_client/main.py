import requests
from deta import App, Deta
from fastapi import FastAPI
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from jinja2 import Template


fast = FastAPI()

app = App(fast)

deta = Deta()

tweet_db = deta.Base("tweetbox")


@app.get("/")
def html_handler():
    tweets = next(tweet_db.fetch([]))
    tweetHtml = {}
    for tweet in tweets:
        tweet_id = tweet.get("tweet_id")
        tweetHtml[tweet_id] = tweet.get("html")
    home_template = Template((open("index.html").read()))
    home_css = open("style.css").read()
    home_hyper = open("home.js").read()
    home_tweetcard = open("tweetcard.js").read()
    return HTMLResponse(home_template.render(home_js=home_hyper, tweets=tweetHtml, css=home_css, tweetcard=home_tweetcard))


    
@app.lib.run("del")
def runner(event):
    note_name = event.json.get("name")
    key = urlsafe_key(note_name)
    note = notes.get(key)
    print(note)
    return notes.delete(note["key"])


@app.lib.run("get")
def runner(event):
    note_name = event.json.get("name")
    key = urlsafe_key(note_name)
    note = notes.get(key)
    return note