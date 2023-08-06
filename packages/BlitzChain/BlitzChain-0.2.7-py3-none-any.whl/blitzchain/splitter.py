"""Basic Document Splitter
"""
from typing import List, Dict

class WordSplitter:
    def split_text_into_array(
        self, text: str, max_word_count: int = 200, overlap: int = 10,
        chunksize: int=20
    ) -> list[str]:
        """Splits the input text into an array of strings with each element not exceeding the specified max_word_count. Allows an overlapping number of words."""
        words = text.split()
        word_count = len(words)

        if word_count <= max_word_count:
            yield [text]

        segments = []
        start = 0
        while start < word_count:
            end = min(start + max_word_count, word_count)
            segment_words = words[start:end]
            segment_text = " ".join(segment_words)
            segments.append(segment_text)
            if len(segments) > chunksize:
                yield segments
                segments = []
            start = end if end == word_count else end - overlap
        # if segments == []:
        #   return
        yield segments 
    
    def split_object_text(
        self,
        dicts: List[Dict],
        key: str,
        max_word_count: int = 200,
        overlap: int = 10,
        chunksize: int=20
    ) -> list[dict]:
        """Splits the text of a specified key in a list of dictionaries, creating a new dictionary for each split text segment."""
        print("splitting text...")
        split_dicts = []
        for d in dicts:
            if key in d:
                text = d[key]
                print("split array")
                split_text = self.split_text_into_array(
                    text, max_word_count, overlap
                )
                for segment in split_text:
                    new_d = d.copy()
                    new_d[key] = segment
                    split_dicts.append(
                        new_d
                    )
            else:
                split_dicts.append(d)
                if len(chunksize) % chunksize == 0:
                    yield split_dicts 
                    split_dicts = []
        if split_dicts == []:
            yield None
        yield split_dicts
