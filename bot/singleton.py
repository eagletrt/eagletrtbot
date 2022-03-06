from telegram import Bot


class BotWrapper:
    wrappee: Bot

    def __init__(self):
        self.wrappee = None

    def set(self, wrappee):
        if self.wrappee is None:
            self.wrappee = wrappee
        else:
            raise RuntimeError("Bot already set")

    def get(self) -> Bot:
        return self.wrappee

    def __getattr__(self, attr):
        return getattr(self.wrappee, attr)


BOT: Bot = BotWrapper()
