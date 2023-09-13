
""" Here I wil setup the way replymarkup buttons should work"""

class InlineKeyboardButton:
    def __init__(self, text, callback_data):
        self.text = text
        self.callback_data = callback_data 
    
    def __dict__(self):
        return {"text": self.text, "callback_data": self.callback_data}

class Keyboard:
    def __init__(self,):
        pass
    