# Fritz

[![CodeQL](https://github.com/psychon-night/Fritz-for-Discord/actions/workflows/codeql.yml/badge.svg)](https://github.com/psychon-night/Fritz-for-Discord/actions/workflows/codeql.yml)

A Discord bot intended for fun and utility

Requires Python 3.10+

`scripts/api/discord.py` is pretty nifty, it adds some bindings to the Discord API in a very user-friendly way. Also, it lets you do simple crap (like getting guild info) which PyCord seeems ***INCAPABLE*** of doing correctly. Also it's reasonably self-documenting and understandable (again, looking at you PyCord, your docs are so far out of date it's not even funny)

### Command Documentation
> `pp_users query_string`: Query Pronouns Page for a user\
> `pp_terms query_string`: Query Pronouns Page for a term

> `seasify song_title count`: Search Spotify for a song\
*count*: int between 1 and 25

> `chatgpt prompt legacy_mode`: Interact with ChatGPT\
*legacy_mode*: allows you to use a legacy LLM. See built-in autocomplete for options

> `cai message character reset`: Interact with a Character AI character\
*character*: defines what character totalk to. See built-in autocomplete for options\
*reset*: whether to continue the current conversation (keep memory) or reset it

> `qr create data style`: Create a QR code\
*data*: the data to encode into the QR code\
*style*: which QR style to use. Default is stylised. Set to `compatible` to make a generic QR code

> `qr scan url`: Scan a QR code.  Must be publically available on the internet (such as on imgur)\
*url*: link to an image containing the QR code

> `givecat`: Get a random cat image

> `joke`: Get a random joke from the internet

> `check_nsfw_allowed`

> `ping`: Check the bot's ping in milliseconds

> `about`: Get the bot's current version

> `invite`: Get the bot's invite URL
