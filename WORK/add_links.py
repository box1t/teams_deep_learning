import os
import json
import re
from typing import Dict
from pymorphy3 import MorphAnalyzer

PAGES_DIR = '../KIDBOOK_LIFE_STAGES/'
CONCEPTS_PATH = 'concepts.json'
morph = MorphAnalyzer()

def get_pages(folder: str) -> Dict[str, str]:
    pages = {}
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        with open(path, 'r') as f:
            pages[filename] = f.read()
    return pages

def get_concepts(path: str) -> Dict[str, str]:
    concepts = {}
    with open(path, 'r') as f:
        d = json.load(f)
        for file in d['concepts']:
            concepts[normalize(file['title'].lower())] = file['file']
    return concepts

def normalize(word: str) -> str:
    return morph.parse(word)[0].normal_form

def add_links(pages: Dict[str, str], concepts: Dict[str, str]) -> Dict[str, str]:
    new_pages = {}
    found_words = []
    for filename, text in pages.items():
        words = re.findall(r'\b\w+\b', text)
        for word in words:
            normal_word = normalize(word.lower())
            if normal_word in concepts and concepts[normal_word] != filename and normal_word not in found_words:
                print(filename, normal_word)
                text = re.sub(rf'\b{re.escape(word)}\b', f"[{word}]({concepts[normal_word]})", text)
                found_words.append(normal_word)
        new_pages[filename] = text
    return new_pages

def save_files(folder, pages):
    for filename, text in pages.items():
        path = os.path.join(folder, filename)
        with open(path, 'w') as f:
            f.write(text)

if __name__ == '__main__':
    pages = get_pages(PAGES_DIR)
    concepts = get_concepts(CONCEPTS_PATH)
    new_pages = add_links(pages, concepts)
    save_files(PAGES_DIR, new_pages)
