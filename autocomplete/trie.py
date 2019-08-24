class TrieNode:
    """
    A class used to represent node in Trie Data Structure

    ...

    Attributes
    ----------
    _value : str
        the value of the root node
    _word_end : str
        the end of word
    _weight : int
        the weight of the word
    _prefix : str
        the prefix of the word for substring matches
    children : dict
        the child nodes

    Methods
    -------
    set_end(value=str)
        Marks the node as end by setting word_end and weight
    add_prefix(prefix=str)
        Adds prefix
    get_prefix()
        Returns prefix
    get_weight()
        Returns weight
    is_end_of_word()
        Returns whether end of word
    """
    __slots__ = ('_value', '_word_end', 'children', '_weight', '_prefix')

    def __init__(self, value: str):
        """
        Parameters
        ----------
        value : str
            the value of the root node
        """
        self._value = value
        self._word_end = False
        self._prefix = ''
        self._weight = -1
        self.children = {}

    def set_end(self, weight: int):
        """Marks the node as end and sets word weight.

        Parameters
        ----------
        weight : str
            The weight of the word
        """
        self._word_end = True
        self._weight = weight

    def add_prefix(self, prefix: str):
        """Marks the node as end and sets word weight.

        Parameters
        ----------
        prefix : str
            The prefix of the word
        """
        self._prefix = prefix

    def get_prefix(self):
        """Returns the prefix of the word.
        """
        return self._prefix

    def get_weight(self):
        """Returns the weight of the word.
        """
        return self._weight

    def is_end_of_word(self):
        """Returns boolean describing the end of the word.
        """
        return self._word_end


class Trie:
    """
    A class used to create Trie Data Structure

    ...

    Attributes
    ----------
    _root : TrieNode
        the root node of the Structure

    Methods
    -------
    add(word=str)
        Adds the given string
    search(query=str)
        Searches the trie for all words and substring matches 
        and returns the result based on word weight
    """
    __slots__ = ('_root')

    def __init__(self, root_value):
        """
        Parameters
        ----------
        value : str
            the value of the root node
        """
        self._root = self.get_node(root_value)

    def get_root(self):
        """Returns the root node.
        """
        return self._root

    def get_node(self, root_value):
        """Creates root node and returns it.

        Parameters
        ----------
        root_value : str
            The root value
        """
        return TrieNode(root_value)

    def add(self, word: str, weight: int = -1, prefix: str = '') -> None:
        """Adds word to the trie.

        Parameters
        ----------
        word : str
            The word to add
        weight : int, optional
            The weight of the word (default is -1)
        prefix : str, optional
            The prefix of the word (default is '')

        Raises
        ------
        Exception
            If empty string is passed
            parameter.
        """
        if len(word) == 0:
            raise Exception('Invalid string')

        start = self.get_root()
        
        for char in word:
            # add node if it doesn't already exist
            node = start.children.setdefault(char, TrieNode(char))
            start = node

        start.set_end(weight)

        if len(prefix):
            start.add_prefix(prefix)

    def search(self, query: str) -> list:
        """Searches the trie for possible words.

        Parameters
        ----------
        query : str
            The string to match

        Returns
        ------
        Array of tuple pairs containing words and its weight
            
        """
        words = []

        # Adds all the words recursively starting from given node
        def get_all_words(start, node):
            if node.is_end_of_word():
                word = start
                prefix = node.get_prefix()
                if prefix:
                    # concatenate prefix if found
                    word = prefix + start[:-1]
                words.append((word, node.get_weight()))

            for char in node.children.keys():
                # recursively find all words from each children
                get_all_words((start + char), node.children[char])

        if len(query) == 0:
            return False

        # start from root
        start = self.get_root()

        # check for each char in query
        for char in query:
            node = start.children

            if char in node:
                start = node[char]
            else:
                return False

        # start from the last node that matches the last char of query
        get_all_words(query, start)
        return words
