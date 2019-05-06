'''Assignment 3 (Version 1.3)

Please add your code where indicated. You may conduct a superficial test of
your code by executing this file in a python interpreter.

The documentation strings ("docstrings") for each function tells you what the
function should accomplish. If docstrings are unfamiliar to you, consult the
Python Tutorial section on "Documentation Strings".

This assignment requires the following packages:

- numpy
- pandas

'''

import os
import string
import unittest

import numpy as np
import pandas as pd
import re
from sklearn.metrics import jaccard_similarity_score


def extract_mentions(tweet):
    """Extract @mentions from a string.

    For example, the string `"RT @HouseGOP: The #StateOfTheUnion is strong."`
    contains the mention ``@HouseGOP``.

    The method used here needs to be robust. For example, the following tweet
    does not contain an @mention: "This tweet contains an email address,
    user@example.net."

    Args:
        tweet (str): A tweet in English.

    Returns:
        list: A list, possibly empty, containing @mentions.

    """
    # YOUR CODE HERE
    result=re.findall(r"(@\w+[^gmail|hotmail|yahoo]):",tweet)

    return result


def normalize_document_term_matrix(document_term_matrix):
    """Normalize a document-term matrix by length.

    Each row in `document_term_matrix` is a vector of counts. Divide each
    vector by its length. Length, in this context, is just the sum of the
    counts or the Manhattan norm.

    For example, a single vector $(0, 1, 0, 1)$ normalized by length is $(0,
    0.5, 0, 0.5)$.

    Normalizing documents by length is often done to help make comparisons
    among documents of different length.

    Args:
        document_term_matrix (array): A document-term matrix of counts

    Returns:
        array: A length-normalized document-term matrix of counts

    """
    # ADD YOUR CODE HERE
    arr=np.array(document_term_matrix,dtype=float)
    row_count=-1
    
    for row in arr:
        total=np.sum(row)
        row_count+=1
        arr[row_count]/=total
        # print(arr[row_count,:])
    return arr


def distance_matrix(document_term_matrix):
    """Calculate a NxN distance matrix given a document-term matrix with N rows.

    Each row in `document_term_matrix` is a vector of counts. Calculate the
    Euclidean distance between each pair of rows.

    Args:
        document_term_matrix (array): A document-term matrix of counts

    Returns:
        array: A square matrix of distances.

    """
    # ADD YOUR CODE HERE
    row=-1
    size=len(document_term_matrix)
    result=np.zeros((size,size),dtype=int)
    # print (result.shape)
    arr=np.array(document_term_matrix)
    # print (arr.shape)
    for orow in arr:
        row=row+1
        column=-1
        for irow in arr:
            column=column+1
            distance=np.linalg.norm(orow-irow)
            result[row][column]=distance
    # print(result)
    return result
    


def jaccard_similarity_matrix(document_term_matrix):
    """Calculate a NxN similarity matrix given a document-term matrix with N rows.

    Each row in `document_term_matrix` is a vector of counts. Calculate the
    Jaccard similarity between each pair of rows.

    Tip: you are working with an array not a list of words or a dictionary of
    word frequencies. While you are free to convert the rows back into
    pseudo-word lists or dictionary of pseudo-word frequencies, you may wish to
    look at the functions ``numpy.logical_and`` and ``numpy.logical_or``.

    Args:
        document_term_matrix (array): A document-term matrix of counts

    Returns:
        array: A square matrix of similarities.

    """
    # ADD YOUR CODE HERE
    row=-1
    size=len(document_term_matrix)
    result=np.zeros((size,size),dtype=int)
    # print (result.shape)
    arr=np.array(document_term_matrix)
    # print (arr.shape)
    for orow in arr:
        row=row+1
        column=-1
        for irow in arr:
            column=column+1
            intersection = np.logical_and(orow, irow)
            union = np.logical_or(orow, irow)
            result[row][column]=(intersection.sum() / union.sum())
            # print(result[row][column])
    return result
  
           
def nearest_neighbors_classifier(new_vector, document_term_matrix, labels):
    """Return a predicted label for `new_vector`.

    You may use either Euclidean distance or Jaccard similarity.

    Args:
        new_vector (array): A array of length V
        document_term_matrix (array): An array with shape (N, V)
        labels (list of str): List of N labels for the rows of `document_term_matrix`.

    Returns:
        str: Label predicted by the nearest neighbor classifier.

    """
    # ADD YOUR CODE HERE
    # print (new_vector)
    arr=np.array(document_term_matrix)
    max=-99
    for row in arr:
        temp=jaccard_similarity_score(row, new_vector)
        row_count+=1
        if temp>max:
            max=temp
            result_index=row_count
            print (row)

    result_label = labels[result_index]
    return result_label 
        



def adjacency_matrix_from_edges(pairs):
    """Construct and adjacency matrix from a list of edges.

    An adjacency matrix is a square matrix which records edges between vertices.

    This function turns a list of edges, represented using pairs of comparable
    elements (e.g., strings, integers), into a square adjacency matrix.

    For example, the list of pairs ``[('a', 'b'), ('b', 'c')]`` defines a tree
    with root node 'b' which may be represented by the adjacency matrix:

    ```
    [[0, 1, 0],
     [1, 0, 1],
     [0, 1, 0]]
    ```

    where rows and columns correspond to the vertices ``['a', 'b', 'c']``.

    Vertices should be ordered using the usual Python sorting functions. That
    is vertices with string names should be alphabetically ordered and vertices
    with numeric identifiers should be sorted in ascending order.

    Args:
        pairs (list of [int] or list of [str]): Pairs of edges

    Returns:
        (array, list): Adjacency matrix and list of vertices. Note
            that this function returns *two* separate values, a Numpy
            array and a list.

    """
    # ADD YOUR CODE HERE

    vertices=[]
    for edges in pairs:
        for vertex in edges:
            if vertex not in vertices:
                vertices.append(vertex)
    vertices=sorted(vertices)

    size=len(vertices)
    adj=np.zeros((size,size),dtype=int)
    for edges in pairs:
        v1=edges[0]
        v2=edges[1]
        adj[vertices.index(v1),vertices.index(v2)]=1
        adj[vertices.index(v2),vertices.index(v1)]=1
    # print (adj)

    return adj,vertices
    
# challenge exercise
def k_nearest_neighbors_classifier(new_vector, document_term_matrix, labels, k):
    """Return a predicted label for `new_vector` based on k nearest neighbors.

    You may use either Euclidean distance or Jaccard similarity.

    This function should find the `k` nearest neighbors to `new_vector`, gather
    their labels, and return the most frequent label. Assume `k` is an odd
    integer and the classification problem is a binary one. Hence there will
    be a unique most frequent label.

    Args:
        new_vector (array): A array of length V
        document_term_matrix (array): An array with shape (N, V)
        labels (list of str): List of N labels for the rows of `document_term_matrix`.
        k (int): odd integer, number of nearest neighbors to use.

    Returns:
        str: Label predicted by the k nearest neighbor classifier.

    """
    # ADD YOUR CODE HERE
    # arr=np.array(document_term_matrix)
    # hmap={}
    # for row in arr:
    #     temp=jaccard_similarity_score(row, new_vector)
    #     row_count+=1
    #     hmap(labels[row_count])=temp
        
    # hmap.sort(values)
    # #remove the rest of the part and then based on provided list of labels find which has max count
   

    # return result_label 




# DO NOT EDIT CODE BELOW THIS LINE


# this utility function is only used in tests, please ignore it
def _load_nytimes_document_term_matrix_and_labels():
    """Load New York Times art and music articles.

    Articles are stored in a document-term matrix.

    See ``data/nytimes-art-music-simple.csv`` for the details.

    This function is provided for you. It will return a document-term matrix
    and a list of labels ("music" or "art").

    This function returns a tuple of two values. The Pythonic way to call this
    function is as follows:

        document_term_matrix, labels = _load_nytimes_document_term_matrix_and_labels()

    Returns:
        (array, list): A document term matrix (as a Numpy array) and a list of labels.
    """
    import pandas as pd
    nytimes = pd.read_csv(os.path.join('data', 'nytimes-art-music-simple.csv'), index_col=0)
    labels = [document_name.rstrip(string.digits) for document_name in nytimes.index]
    return nytimes.values, labels



class TestAssignment3(unittest.TestCase):

    def test_extract_mentions1(self):
        tweet = """RT @HouseGOP: The #StateOfTheUnion isn't strong for the 8.7 million Americans out of work. #SOTU http://t.co/aa7FWRCdyn"""
        self.assertEqual(len(extract_mentions(tweet)), 1)
        self.assertIn('@HouseGOP', extract_mentions(tweet))

    def test_adjacency_matrix_from_edges1(self):
        pairs = [['a', 'b'], ['b', 'c']]
        expected = np.array(
            [[0, 1, 0],
             [1, 0, 1],
             [0, 1, 0]])
        A, nodes = adjacency_matrix_from_edges(pairs)
        self.assertEqual(nodes, ['a', 'b', 'c'])
        np.testing.assert_array_almost_equal(A, expected)

    def test_normalize_document_term_matrix1(self):
        dtm, _ = _load_nytimes_document_term_matrix_and_labels()
        self.assertEqual(dtm.shape, normalize_document_term_matrix(dtm).shape)

    def test_distance_matrix1(self):
        dtm, _ = _load_nytimes_document_term_matrix_and_labels()
        dist = distance_matrix(dtm)
        self.assertEqual(dist.shape[0], dist.shape[1])

    def test_jaccard_similarity_matrix(self):
        dtm, _ = _load_nytimes_document_term_matrix_and_labels()
        similarity = jaccard_similarity_matrix(dtm)
        self.assertEqual(similarity.shape[0], similarity.shape[1])


if __name__ == '__main__':
    unittest.main()
