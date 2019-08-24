import os
import sys
import json
import logging

from autocomplete import AutoComplete

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(level=logging.DEBUG)

def get_words_from_file(filename):
    with open(os.path.join(BASE_DIR, filename)) as f:
        data = json.load(f)

        words = []
        for word, weight in data.items():
            words.append((word, weight))
        return words

def main():
    filename = None
    
    if len(sys.argv) > 1:
        filename = sys.argv[1]

        data = get_words_from_file(filename)
        logging.info('Number of word pairs: {0}'.format(len(data)))

    if filename:
        auto = AutoComplete(data)
    else:
        auto = AutoComplete()

    while True:

        query = input('Enter query to search: ')
        res = auto.query(query)
        print(res)

if __name__ == "__main__":
    main()
