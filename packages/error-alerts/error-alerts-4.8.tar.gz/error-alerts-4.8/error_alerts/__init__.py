import traceback
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

DEFAULT_IGNORED_ERRORS = [
    'The service is currently unavailable', # Google sheets API down
    'Could not authenticate you', # Twitter app suspended
    ]

class alerts(Bot):
    def __init__(self, token=None, channel=None, logger=None, full_error=True, raise_error=False, resend_repeat_errors=True):
        if token:
            self.bot = super()
            self.bot.__init__(token=token)
            self.message = bot.send_message

        self.channel = channel
        if logger:
            self.log, self.current_time = logger.log, logger.current_time
        else:
            self.log = None
        self.full_error = full_error
        self.raise_error = raise_error
        self.resend_repeat_errors = resend_repeat_errors
        self.last_error = None

    def send(self, title='Error', exception=None, channel=None):
        if not channel:
            channel = self.channel
        if self.full_error:
            error = traceback.format_exc()
        else:
            error = str(exception)
        message = f'{title}: {error}'
        
        self.printer(message, level='error')

        if error != self.last_error or self.resend_repeat_errors:

            if channel:
                if all(ignored_error not in error for ignored_error in DEFAULT_IGNORED_ERRORS):
                    self.last_error = error

                    try:
                        self.message(channel, message[:4096])
                    except Exception as telegram_error:
                        self.printer('Error sending alert message to Telegram:', telegram_error, level='error')

        if self.raise_error:
            raise Exception('Raiser') from exception

    def send_message(self, *messages, print_message=True, current_time=True, channel=None, buttons_dict={}):
        if not channel:
            channel = self.channel
        final_message = ''
        for message in messages:
            final_message += message
            final_message += ' '
        if print_message:
            self.printer(final_message, current_time=current_time)
        if channel:
            buttons_markup = self.convert_dict_to_buttons(buttons_dict)
            try:
                message = self.message(channel, final_message[:4096], reply_markup=buttons_markup)
                return message
            except Exception as telegram_error:
                self.printer('Error sending message to Telegram:', telegram_error, level='error')
        return None

    def convert_dict_to_buttons(self, buttons_dict):
        buttons = []
        for key in buttons_dict:
            button = [InlineKeyboardButton(text=key, callback_data=buttons_dict[key])]
            buttons.append(button)
        buttons_markup = InlineKeyboardMarkup(buttons)
        return buttons_markup
    
    def printer(self, *items, level='info', current_time=True):
        if self.log:
            if current_time:
                self.current_time(*items, level=level)
            else:
                self.log(*items, level=level)
            self.log(level=level)
        elif level != 'debug': # Don't print debug only messages
            print(*items)
            print()

class telegram:
    def __init__(self, token=None, channel=None, logger=None, full_error=True, raise_error=False, resend_repeat_errors=True):
        alerts(token, channel, logger, full_error, raise_error, resend_repeat_errors)