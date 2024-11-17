import json
import os

ARTICLES_FILE = os.path.join(os.path.dirname(__file__), '../articles.json')

def load_articles():
    with open(ARTICLES_FILE, 'r') as file:
        return json.load(file)

def save_articles(articles):
    with open(ARTICLES_FILE, 'w') as file:
        json.dump(articles, file, indent=4)