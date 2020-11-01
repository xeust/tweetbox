import base64
import hashlib
import hmac
import json
import os
import requests
from deta import App, Deta
from fastapi import FastAPI, Request, Response
from TwitterAPI import TwitterAPI


fast = FastAPI()

app = App(fast)

deta = Deta()

tweet_box = deta.Base("tweetbox")


TWITTER_CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY", None)
TWITTER_CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET", None)
TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN", None)
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET", None)
TWITTER_WEBHOOK_ENV = os.environ.get("TWITTER_WEBHOOK_ENV", None)
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", None)

twitterAPI = TwitterAPI(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)


@app.get("/webhooks/twitter")
def webhook_challenge(crc_token: str):
  
    validation = hmac.new(
        key=bytes(TWITTER_CONSUMER_SECRET, 'utf-8'),
        msg=bytes(crc_token, 'utf-8'),
        digestmod = hashlib.sha256
    )
    digested = base64.b64encode(validation.digest())
    response = {
        'response_token': 'sha256=' + format(str(digested)[2:-1])
    }
    print('responding to CRC call')

    return response


@app.post("/webhooks/twitter")
async def add_tweet(request: Request):
    response = await request.json()
    favorite = response.get("favorite_events", None)
    if favorite:
        tweet_id = favorite[0].get("favorited_status").get("id_str")
        r = twitterAPI.request(f"statuses/show/:{tweet_id}", None, None, "GET")
        tweet_json = json.loads(r.text)
        tweet_storage = {}
        tweet_storage["tweet_id"] = tweet_id
        tweet_storage["created"] = tweet_json.get("created_at")
        tweet_storage["tweet_content"] = tweet_json.get("text")
        tweet_storage["url"] = tweet_json.get("entities").get("urls")[0].get("url")
        tweet_storage["expanded_url"] = tweet_json.get("entities").get("urls")[0].get("expanded_url")
        tweet_storage["user_handle"] = tweet_json.get("user").get("screen_name")
        tweet_storage["user_fullname"] = tweet_json.get("user").get("name")
        tweet_storage["tags"] = []
        tweet_storage["html"] = requests.get(f"https://publish.twitter.com/oembed?url=https://twitter.com/jack/statuses/{tweet_id}").json().get("html")
        resp = tweet_box.put(tweet_storage)
    return {"message": "success"}
    
    
@app.lib.run("subscribe")
def runner(event):
    r = twitterAPI.request(f"account_activity/all/:{TWITTER_WEBHOOK_ENV}/subscriptions", None, None, "POST")
    print(r.status_code)
    print(r.text)
    return


@app.lib.run("create")
def webhook_creator(event):
    r = twitterAPI.request(f"account_activity/all/:{TWITTER_WEBHOOK_ENV}/webhooks", {'url': WEBHOOK_URL})
    print(r.status_code)
    print(r.text)
    return

@app.lib.run("get")
def runner(event):
    r = twitterAPI.request(f"statuses/show/:{TWEET_ID}", None, None, "GET")
    print(json.loads(r.text))
    return