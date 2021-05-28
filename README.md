# Kotobot2

Discord bot that:
* provides links to subreddits that users mention in their messages
* makes dad jokes

## Environment variables

This project utilizes [PRAW](https://praw.readthedocs.io/) (more specifically, [AsyncPRAW](https://asyncpraw.readthedocs.io/)), so one would need to set up [a Reddit app](https://www.reddit.com/wiki/api).

* `KBOT_REDDIT_CLIENT_ID`: Reddit client ID.
* `KBOT_REDDIT_CLIENT_SECRET`: Reddit client secret.
* `KBOT_TOKEN`: The Discord bot token.