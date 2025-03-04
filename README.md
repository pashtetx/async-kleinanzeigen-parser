![Tux, the Linux mascot](/assets/kleinanzeigen-parser.png)

<div align="center">
    <b>Asyncio kleinanzeigen parser based on HTTP requests</b>
</div>

# Kleinanzeigen parser
![Version](https://img.shields.io/badge/1.0-green?style=flat&logo=version&label=version) ![Static Badge](https://img.shields.io/badge/async-blue?style=flat) ![Static Badge](https://img.shields.io/badge/telegram-blue?style=flat&link=https%3A%2F%2Ft.me%2Fprogerfromselo)

**Kleinanzeigen parser** - fast and powerful data scraper that works on asynchronous queries.
## Installation

**!IMPORTANT:** You need python >= 3.11.
Rename `.env TEMPLATE` to `.env` and edit your data in .env file.

```
file: .env TEMPLATE
USER_ID=<Your user id from telegram>
TOKEN=<bot token from telegram>
```

Then follow the instruction:
1. `python -m venv venv`
2. `source venv/bin/activate` (Windows: `venv\Scripts\activate`)
3. `pip install -r requirements.txt`
4. `python run.py`

## TODO
- Details parsing
- User's API
- Proxy support


## License
Kleinanzeigen parser is licensed under the MIT license. [See LICENSE for more information.](https://github.com/pashtetx/async-kleinanzeigen-parser/blob/main/LICENSE)
