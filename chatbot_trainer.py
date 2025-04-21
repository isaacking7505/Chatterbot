# chatbot_trainer.py
import os
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import yaml

# Initialize the ChatBot with the correct key for spaCy tagger
chatbot = ChatBot(
    'TriviaBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3',
    language='english'
)

# Prepare trainers
list_trainer   = ListTrainer(chatbot)
corpus_trainer = ChatterBotCorpusTrainer(chatbot)

# Look for trivia_conversations.yml in script directory or a 'data' subfolder
script_dir = os.path.dirname(os.path.abspath(__file__))
search_paths = [
    os.path.join(script_dir, 'trivia_conversations.yml'),
    os.path.join(script_dir, 'data', 'trivia_conversations.yml'),
]

for yml_path in search_paths:
    if os.path.exists(yml_path):
        with open(yml_path, 'r', encoding='utf-8') as f:
            conversations = yaml.safe_load(f).get('conversations', [])
        for conv in conversations:
            list_trainer.train(conv)
        break
else:
    print(f"Warning: none of {search_paths} found, skipping custom data")

# Train with the standard English corpus once
e_corpus = "chatterbot.corpus.english"
corpus_trainer.train(e_corpus)
