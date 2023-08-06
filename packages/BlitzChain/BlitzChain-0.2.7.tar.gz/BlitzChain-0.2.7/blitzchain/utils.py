"""Utility functions for BlitzChain.
"""
import sys

def split_documents(documents, chunksize=20):
    for i in range(0, len(documents), chunksize):
        yield documents[i:i+chunksize]

def get_size(obj):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if isinstance(obj, dict):
        return size + sum([get_size(v) for v in obj.values()]) + sum([get_size(k) for k in obj.keys()])
        
    elif hasattr(obj, '__dict__'):
        return size + get_size(obj.__dict__)
        
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        return size + sum([get_size(i) for i in obj])
        
    return size

def get_dictionary_size_in_mb(dict_obj):
    return get_size(dict_obj) / 1024 / 1024
