"""Utility functions for BlitzChain.
"""

def split_documents(documents, chunksize=20):
    for i in range(0, len(documents), chunksize):
        yield documents[i:i+chunksize]
