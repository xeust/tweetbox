# A Hackable Twitter Bookmarking System

Tweetbox is a bookmarking system for Tweets. 

I learned the hard way (disappearing bookmarks) that there is a hard limit on the number of tweets that fit in Twitter's native bookmarker.

That coupled with the inability to add any context or find certain tweets inspired this project.

Tweetbox is made up of two servers that talk to one database to store tweet data.

- `tweetbox` receives the payloads from liked tweets via Twitter webhook, storing them in a database (open endpoint)
- `tweetbox_client` serves the tweets to a UI


## Configuration & Deployment

### Creating the tweetbox server
This app runs on [Deta](https://www.deta.sh/), but can be easily modified to run elsewhere, you will need a database.

Clone this repository and enter the `tweetbox` sub-directory.

Install the [`deta cli`](https://docs.deta.sh/docs/cli/install) and use the `deta new` command to create the `tweetbox` server.

Note the url of `tweetbox` for the next step.

### Creating a Twitter App, Permissions & Grabbing Tokens

This application requires you to create an app from the [Twitter Developer Portal](https://developer.twitter.com/).

In the Twitter app creation form paste the `tweetbox` url from the last step into the `website url` field.

Once you've created your app, you need to set the permissions and grab the authentication tokens from Twitter. 

#### Permissions

Navigate to the app's `Permissions` panel and change the permissions setting to `Read, write, and Direct Messages`. This permission level is necessary to subscribe to the account activity webhook.

#### Grabbing the Tokens

Navigate to the app's `Keys and Tokens` panel, then generate (if necessary) and copy 4 tokens:

Consumer API Keys
- `API key`
- `API secret key`

Access Token and Access Token Secret
- `Access Token`
- `Access Token Secret`

#### Creating the Twitter Dev Environment

Navigate to the Twitter Dev Environments page (https://developer.twitter.com/en/account/environments) and set up the `Account Activity API / Sandbox` environment with the label `dev`.

#### Creating the .env file

Now you have all the information to create the .env file in the `tweetbox` directory.

```
TWITTER_CONSUMER_KEY=<API Key>
TWITTER_CONSUMER_SECRET=<API Secret Key>
TWITTER_ACCESS_TOKEN=<Access Toek>
TWITTER_ACCESS_TOKEN_SECRET=<Access Token Secret>
TWITTER_WEBHOOK_ENV=dev
```

From this directory, add these env vars to the server with the command:

```
deta update -e .env
```

#### Creating The Webhook & Subscription

Twitter requires you to create the Webhook and Subcription to the account activity via api calls.

For this, a public endpoint is required.

Open your server by typing in:

```
deta auth disable
```

From the `tweetbox` directory, create the webhook with the command `deta run create`. 

Then subscribe to your account activity with the command `deta run subscribe`.

If these two commands were successful, you can start liking tweets, which will save them to your tweetbox.


### Creating the tweetbox client

Navigate to the `tweetbox_client` sub directory and enter the command `deta new`.

You can visit the client url and all your saved tweets should display.