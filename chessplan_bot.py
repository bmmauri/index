import argparse
import logging
import telegram
import yaml
from telegram import Update

from index import core
from telegram.ext import Updater, CommandHandler, Dispatcher

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="Chess Plan bot")
parser.add_argument("token", type=str, help='TOKEN to access to telegram bot')
args = parser.parse_args()


def start(update: Update, context):
    index: core.Index = context.bot.get_index()
    update.message.reply_text(
        f"TITLE: {index.get_document_property('title')}\nDESCRIPTION: {index.get_document_property('description')}"
    )


def get_training_exercise(update: Update, context):
    index: core.Index = context.bot.get_index()
    exercise = index.get_exercise_training()
    update.message.reply_text(f"EXERCISE: {exercise}")


class ChessBot(telegram.Bot):

    def __init__(self, token, index, base_url=None, base_file_url=None, request=None, private_key=None,
                 private_key_password=None, defaults=None):
        self.__index = index
        super().__init__(token, base_url, base_file_url, request, private_key, private_key_password, defaults)

    def get_index(self):
        return self.__index


if __name__ == '__main__':

    _DOCUMENT = yaml.safe_load(open('index.yaml'))
    updater = Updater(
        use_context=True,
        bot=ChessBot(token=args.token, index=core.Index(document=_DOCUMENT))
    )
    dp: Dispatcher = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("get_training_exercise", get_training_exercise))
    updater.start_polling()
    updater.idle()

