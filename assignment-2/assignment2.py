'''Assignment 2

Version 1.0

Please add your code where indicated. You may conduct a superficial test of
your code by executing this file in a python interpreter.

The documentation strings ("docstrings") for each function tells you what the
function should accomplish. If docstrings are unfamiliar to you, consult the
Python Tutorial section on "Documentation Strings".

'''
import re

def argmax(sequence):
    """Return the index of the highest value in a list of numbers.

    This is a warmup exercise.

    Remember that Python uses zero-based numbering of indexes.

    Args:
        sequence (list): A list of numeric values.

    Returns:
        int: The index of the highest value in `sequence`.

    """
    # YOUR CODE HERE
    max_num=0
    max_index=-1
    for index,item in enumerate(sequence):
        if max_num<item:
           max_num=item
           max_index=index
    return max_index


def tokenize(string, lowercase=False):
    """Extract words from a string containing English words.

    Handling of hyphenation, contractions, and numbers is left to your
    discretion.

    Tip: you may want to look into the `re` module.

    Args:
        string (str): A string containing English.
        lowercase (bool, optional): Convert words to lowercase.

    Returns:
        list: A list of words.

    """
    # YOUR CODE HERE
    if lowercase:
       string=string.lower()

    list=re.split("\s",string)

    return list

def shared_words(text1, text2):
    """Identify shared words in two texts written in English.

    Your function must make use of the `tokenize` function above.

    Tip: you should considering using Python `set`s to solve the problem.

    Args:
        text1 (str): A string containing English.
        text2 (str): A string containing English.

    Returns:
        set: A set with words appearing in both `text1` and `text2`.

    """
    # YOUR CODE HERE
    l1=tokenize(text1)
    l2=tokenize(text2)
    return set(l1).intersection(set(l2))

def shared_words_from_filenames(filename1, filename2):
    """Identify shared words in two texts stored on disk.

    Your function must make use of the `tokenize` function above. You should
    considering using Python `set`s to solve the problem.

    For each filename you will need to `open` file and read the file's
    contents.

    There are two sample text files in the `data/` directory which you can use
    to practice on.

    Args:
        filename1 (str): Filename of a file containing English text.
        filename2 (str): Filename of a file containing English text.

    Returns:
        set: A set with words appearing in both texts.

    """
    # YOUR CODE HERE
    with open(filename1, 'r') as myfile:
    	 string1=myfile.read().replace('\n', '')
    with open(filename2, 'r') as myfile:
   	 string2=myfile.read().replace('\n', '')
	
    return shared_words(string1,string2)

def text2wordfreq(string, lowercase=False):
    """Calculate word frequencies for a text written in English.

    Handling of hyphenation and contractions is left to your discretion.

    Your function must make use of the `tokenize` function above.

    Args:
        string (str): A string containing English.
        lowercase (bool, optional): Convert words to lowercase before calculating their
            frequency.

    Returns:
        dict: A dictionary with words as keys and frequencies as values.

    """
    # YOUR CODE HERE
    l=tokenize(string,lowercase)
    dict={}
    for word in l:
        if word in dict:
           continue 
        else:
           dict[word]=l.count(word)
    return dict

def lexical_density(string):
    """Calculate the lexical density of a string containing English words.

    The lexical density of a sequence is defined to be the number of
    unique words divided by the number of total words. The lexical
    density of the sentence "The dog ate the hat." is 4/5.

    Ignore capitalization. For example, "The" should be counted as the same
    type as "the".

    This function should use the `text2wordfreq` function.

    Args:
        string (str): A string containing English.

    Returns:
        float: Lexical density.

    """
    # YOUR CODE HERE
    dict=text2wordfreq(string)
    unique=0
    total=0

    for key,value in dict.items():
	unique=unique+1	
	total=total+value

    return unique/total

def hashtags(string):
    """Extract hashtags from a string.

    For example, the string `"RT @HouseGOP: The #StateOfTheUnion is strong."`
    contains the hashtag `#StateOfTheUnion`.

    Args:
        string (str): A string containing English.

    Returns:
        list: A list, possibly empty, containing hashtags.

    """
    # YOUR CODE HERE
    shashtags=re.findall(r"#(\w+)",string)
    return shashtags

def jaccard_similarity(text1, text2):
    """Calculate Jaccard Similarity between two texts.

    The Jaccard similarity (coefficient) or Jaccard index is defined to be the
    ratio between the size of the intersection between two sets and the size of
    the union between two sets. In this case, the two sets we consider are the
    set of words extracted from `text1` and `text2` respectively.

    This function should ignore capitalization. A word with a capital
    letter should be treated the same as a word without a capital letter.

    Args:
        text1 (str): A string containing English words.
        text2 (str): A string containing English words.

    Returns:
        float: Jaccard similarity

    """
    # YOUR CODE HERE
    list1=tokenize(text1.lower())
    list2=tokenize(text2.lower())
    common=shared_words(text1.lower(),text2.lower())
    return len(common)/(len(list1)+len(list2))


def char_ngrams(string, n, lowercase=False):
    """Extract character n-grams from a string.

    For example, the string `"RT @HouseGOP: The #StateOfTheUnion is strong."`
    contains, among other 4-grams, 'ouse', 'rong', 'stro', 'tate'.

    Handling of word boundaries, beginning of string, and end of string is left
    up to you. Any reasonable solution will be accepted.

    Args:
        string (str): A string containing English.
        n (int): This number of adjacent characters count as a token. If `n`
            is 3, 3-grams will be generated (e.g., 'str', 'tro', 'ron', ...).
            If `n` is 4 then 4-grams will be generated.
        lowercase (bool, optional): Convert string to lowercase before
            extracting ngrams.

    Returns:
        list: A list, possibly empty, containing ngrams.

    """
    # YOUR CODE HERE
    list=[]
    for word in string.split():
         length=len(word)
         if length<n :
	    continue
	 else:
            for x in xrange(length-n):
	        list.append(word[x:x+n])
    return list

# Challenge exercise
def estimate_gender(given_name, names_dataset_filename):
    """Return a likely gender given a person's given name.

    In the United States it is often easy to make a provisional guess about an
    individual's gender identity based on their given name. For example, very
    few individuals identifying as women use the given name "John".

    Use the "baby names" dataset to make an informed guess at an individual's
    gender given their given name. (The dataset is found in this repository.)

    Args:
        given_name (str): a given name (e.g., "John", "Ashwini").
        names_dataset_filename (str): path to `names.csv`

    Returns:
        str: one of {'man', 'woman', 'other'}
    """
    # YOUR CODE HERE
    file = open(names_dataset_filename, 'r')
    result="other" 
    for line in file: 
        temp=line.split(",")
        if temp[1]==given_name:
            if temp[2]=='M':
	       result='man'
	    else:
	       result='woman'
	else:
	  continue
    return result

# DO NOT EDIT CODE BELOW THIS LINE

import os
import unittest

import numpy as np


class TestAssignment2(unittest.TestCase):

    def test_argmax(self):
        self.assertEqual(argmax([0, 1, 2]), 2)
        self.assertEqual(argmax([3, 1, 2]), 0)

    def test_tokenize(self):
        words = tokenize('Colorless green ideas sleep furiously.', True)
        self.assertIn('green', words)
        self.assertIn('colorless', words)
        words = tokenize('The rain  in spain is  mainly in the plain.', False)
        self.assertIn('The', words)
        self.assertIn('rain', words)

    def test_text2wordfreq(self):
        counts = text2wordfreq('Colorless green ideas sleep furiously. Green ideas in trees.', True)
        self.assertEqual(counts['green'], 2)
        self.assertEqual(counts['sleep'], 1)
        self.assertIn('colorless', counts)
        self.assertNotIn('hello', counts)

    def test_shared_words(self):
        self.assertEqual(shared_words('the hat', 'red hat'), {'hat'})

    def test_shared_words_from_filenames(self):
        # the use of the os.path functions is required so that filenames work
        # on Windows and Unix/Linux systems.
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        filename1 = os.path.join(data_dir, '1984-chp01.txt')
        filename2 = os.path.join(data_dir, 'animal-farm-chp01.txt')
        words = shared_words_from_filenames(filename1, filename2)
        self.assertGreater(len(words), 3)
        self.assertIn('already', words)

    def test_lexical_density(self):
        self.assertAlmostEqual(lexical_density("The cat"), 1)
        self.assertAlmostEqual(lexical_density("The cat in the hat."), 4/5)

        tweet = """RT @HouseGOP: The #StateOfTheUnion isn't strong for the 8.7 million Americans out of work. #SOTU http://t.co/aa7FWRCdyn"""
        self.assertEqual(len(hashtags(tweet)), 2)

    def test_jaccard_similarity(self):
        text1 = "Eight million Americans"
        text2 = "Americans in the South"
        self.assertAlmostEqual(jaccard_similarity(text1, text2), 1/6)

    def test_hashtags(self):
        tweet = """RT @HouseGOP: The #StateOfTheUnion isn't strong for the 8.7 million Americans out of work. #SOTU http://t.co/aa7FWRCdyn"""
        self.assertEqual(len(hashtags(tweet)), 2)

    def test_char_ngrams(self):
        tweet = """RT @HouseGOP: The #StateOfTheUnion isn't strong for the 8.7 million Americans out of work. #SOTU http://t.co/aa7FWRCdyn"""
        self.assertIn('mil', char_ngrams(tweet, 3))
        self.assertIn('ill', char_ngrams(tweet, 3))

    def test_estimate_gender(self):
        self.assertEqual('woman', estimate_gender('Emma', 'data/names.csv'))
        self.assertEqual('man', estimate_gender('John', 'data/names.csv'))


if __name__ == '__main__':
    unittest.main()
