from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# TODO: Customize name and logic 
chatbot = ChatBot('StudyBot')

def train_basic():
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train("chatterbot.corpus.english")  # Pre-built data
    # TODO: Add custom training data