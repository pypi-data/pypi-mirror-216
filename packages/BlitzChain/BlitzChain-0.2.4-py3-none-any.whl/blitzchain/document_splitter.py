"""Basic Document Splitter
"""
from typing import List, Dict

class Splitter:
    """Base class for splitter
    """
    
class WordSplitter(Splitter):
    def split_text_into_array(
        self, text: str, max_word_count: int = 200, overlap: int = 10
    ) -> list[str]:
        """Splits the input text into an array of strings with each element not exceeding the specified max_word_count. Allows an overlapping number of words."""
        words = text.split()
        word_count = len(words)

        if word_count <= max_word_count:
            return [text]

        segments = []
        start = 0
        while start < word_count:
            end = min(start + max_word_count, word_count)
            segment_words = words[start:end]
            segment_text = " ".join(segment_words)
            segments.append(segment_text)
            start = end - overlap

        return segments

    def split_dict_text(
        self,
        dicts: List[Dict],
        key: str,
        max_word_count: int = 200,
        overlap: int = 10,
    ) -> list[dict]:
        """Splits the text of a specified key in a list of dictionaries, creating a new dictionary for each split text segment."""
        split_dicts = []
        for d in dicts:
            if key in d:
                text = d[key]
                split_text = self.split_text_into_array(text, max_word_count, overlap)
                for segment in split_text:
                    new_d = d.copy()
                    new_d[key] = segment
                    split_dicts.append(new_d)
            else:
                split_dicts.append(d)
        return split_dicts
