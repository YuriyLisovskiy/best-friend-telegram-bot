# Telegram Bot
| **`License`** | **`Language`** |
|-----------------|---------------------|
| [![PyPi](https://img.shields.io/pypi/l/Django.svg)](LICENSE) | [![PyPI](https://img.shields.io/badge/python-3.5%2C%203.6-blue.svg)](https://github.com/YuriyLisovskiy/NeuralNetwork) |
## Installation
##### Linux:
```bash
$ git clone https://github.com/YuriyLisovskiy/TelegramBot.git
$ cd TelegramBot/
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt 
``` 
##### Windows:
```bash
$ git clone https://github.com/YuriyLisovskiy/TelegramBot.git
$ cd TelegramBot/ 
$ virtualenv venv 
$ venv/Scripts/activate 
$ pip install -r requirements.txt 
``` 
## Usage
- From `bot` package import Bot:
    ```python 
    from bot.telegram_bot import Bot 
    ```
- Using [introduction to bots](https://core.telegram.org/bots) create bot and get it's token.
- Create `local_settings.py` file in `bor` folder and add `TOKEN` variable there, example:
    ```python 
    TOKEN = 'bot_token_here' 
    ```
##### Run: 
```bash 
$ python runner.py 
```
## Author
- **[Yuriy Lisovskiy](https://github.com/YuriyLisovskiy)**
## License
This project is licensed under the BSD-2-Clause License - see the [LICENSE](LICENSE) file for details.