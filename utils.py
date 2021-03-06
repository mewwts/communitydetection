"""
This module defines an Enum and some namedtuples for use throughout
the whole lib. 

"""

from collections import namedtuple
from enum import Enum
from operator import itemgetter

Method = Enum('Method', 'luv rank dissolve prop')

Arguments = namedtuple('Arguments', 
    ['exporter',
    'cytowriter',
    'analyzer',
    'tsh',
    'verbose',
    'dump',
    'method']
    )

Graph = namedtuple('Graph', ['A', 'm', 'n', 'k'])

def rank(sequence):
    """ 
    Return the index from the original sequence the element
    has in the sorted array.

    """
    ranked = zip(*sorted(enumerate(sequence), key=itemgetter(1))[::-1])[0]
    return list(ranked)
