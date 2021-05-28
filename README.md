# Kotobot2

Discord bot that:
* provides links to subreddits that users mention in their messages
* makes dad jokes

## Set up

Install the requirements as one does, `pip install -r requirements.txt`. I use Python 3.9, but it would likely work for 3.6 or above (but not 3.5 or below).

Set up the environment variables (see below).

Run `python kbot.py`.

### Environment variables

This project utilizes [PRAW](https://praw.readthedocs.io/) (more specifically, [AsyncPRAW](https://asyncpraw.readthedocs.io/)), so one would need to set up [a Reddit app](https://www.reddit.com/wiki/api).

* `KBOT_REDDIT_CLIENT_ID`: Reddit client ID.
* `KBOT_REDDIT_CLIENT_SECRET`: Reddit client secret.
* `KBOT_TOKEN`: The Discord bot token.