import os
import re
import sys
import time
import json
import pickle
import logging

from .trie import Trie
from .utils import calculate_time

logging.basicConfig(level=logging.DEBUG)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class AutoComplete:
    """
    A class for implementing Autocomplete

    ...

    Attributes
    ----------
    _dataset : Trie
        the data structure for word word pairs

    Methods
    -------
    query(word=str)
        Finds all matches by weight order and returns it.
    """
    __slots__ = ('_dataset', '_serialized_file')

    def __init__(self, word_pairs=None):
        self._serialized_file = 'serialized.pickle'
        self._dataset = self.get_trie(word_pairs)

    @calculate_time(title='Data Load Time')
    def get_trie(self, data=None) -> Trie:
        """Gets Trie Data Structures for the words

        Trie is built from the list of word pairs. After creation the object
        is serialized for future reload without reconstruction.

        If the argument `data` isn't passed in, trie is created from 
        the serialized trie object. Exception is thrown if serialized
        object is not found

        Parameters
        ----------
        data : list, optional
            List of Tuple pairs of word and weight  (default is None)

        Raises
        ------
        Exception
            If serialized data is not found when 'data` isn't passed.

        Returns
        -------
        Trie: Data structure containing word, weight pairs
        """
        logging.info('Loading Data')
        trie = None

        if data is None:
            # check for serialized data
            trie = self.load_serialized_file()
            if not trie:
                raise Exception('Serialized Data not found')
        else:
            logging.info('Creating Trie DS')
            trie = self.make_trie(data)

            # serialize the structure
            logging.info('Serializing Trie DS')
            try:
                self.write_serialized_file(trie)
            except MemoryError as e:
                logging.warn('Skipping Serialization')

        return trie

    def make_trie(self, data: list) -> Trie:
        """Creates Trie Data Structures for the words

        Parameters
        ----------
        data : list
            List of Tuple pairs of word and weight

        Returns
        -------
        Trie: Data structure containing word, weight pairs
        """
        trie = Trie('')

        for item in data:
            test = item[0]
            # for substring matches split the string
            if '_' in test:
                words = test.split('_')
                trie.add(test, item[1])
                trie.add((words[1] + '_'), 8, prefix=(words[0] + '_'))
            else:
                trie.add(*item)
        return trie

    @calculate_time('Query Time')
    def query(self, q: str, n: int=10):
        """Gets matching words from trie, sorts it based on weight 
           and returns the top `n` words

        Parameters
        ----------
        q : str
            The query to search
        n: int, optional
            The number of top results to return

        Returns
        -------
        list: if matches are found 
        str: if no match is found
        """
        result = self._dataset.search(q)
        if result is not False:
            sorted_res = self.weight_sort(result)[:n]
            words = list(zip(*sorted_res))
            return words[0]
        return 'No match found'

    def weight_sort(self, arr):
        """Sorts based on weight

        Parameters
        ----------
        arr : list
            List of word, weight pairs

        Returns
        -------
        list: Sorted tuple pairs
        """
        arr.sort(key=lambda x: x[1], reverse=True)
        return arr

    def load_serialized_file(self):
        """Loads trie from serialized file

        Attempts to create trie from serialized file if file is found

        Returns
        -------
        Trie: if file is found
        """
        logging.info('Loading from serialized file')
        for entry in os.scandir(BASE_DIR):
            if entry.name == self._serialized_file:
                with open(entry.path, 'rb') as f:
                    data = pickle.load(f)
                    return data
        return False

    def write_serialized_file(self, data):
        """Create serialized file from object

        Converts the given trie object into serialized form and stores it in a file

        """
        serialized_obj = pickle.dumps(data, protocol=4)

        logging.info('Creating Serialized file')
        with open(os.path.join(BASE_DIR, self._serialized_file), 'wb') as f:
            f.write(serialized_obj)
