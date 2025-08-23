import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from functools import reduce
from itertools import groupby
from operator import itemgetter
import pandas as pd
import time
import logging
logging.basicConfig(format = '%(asctime)s: %(levelname)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
import traceback

# Ensure required tokenizer is available
nltk.download('punkt')

class Chunker:
    def __init__(self, chunk_size=100):
        """
        Initialize the SentenceChunker with a maximum word count per chunk.
        
        Args:
            chunk_size (int): Maximum words allowed per chunk.
        """
        self.chunk_size = chunk_size

    def _assign_chunks(self, word_counts):
        """
        Assigns chunk IDs to each sentence based on word count limits.
        """
        def reducer(acc, wc):
            last_idx, total_words, chunk_ids = acc
            if total_words + wc > self.chunk_size:
                last_idx += 1
                total_words = wc
            else:
                total_words += wc
            chunk_ids.append(last_idx)
            return (last_idx, total_words, chunk_ids)

        _, _, chunk_indices = reduce(
            lambda acc, wc: reducer(acc, wc),
            word_counts,
            (0, 0, [])
        )
        return chunk_indices

    def chunk(self, text):
        """
        Chunks the input text into sentence-based chunks.

        Args:
            text (str): Input text.

        Returns:
            list[str]: List of text chunks.
        """
        sentences = sent_tokenize(text)
        word_counts = list(map(lambda s: len(word_tokenize(s)), sentences))
        chunk_ids = self._assign_chunks(word_counts)

        grouped = groupby(
            sorted(zip(chunk_ids, sentences), key=itemgetter(0)),
            key=itemgetter(0)
        )

        chunks = [' '.join(sentence for _, sentence in group) for _, group in grouped]
        return chunks
    
    def vanilla_chunks_generation(self,df):
        start = time.time()        
        logger.info(f"Starting Vanilla Chunking")
        try:
            if len(df['text'].iloc[0]) == "":
                raise ValueError("Text is empty")
            
            df['sentences'] = df['text'].apply(lambda x: sent_tokenize(x))
            df = df.explode('sentences')
            df['word_len'] = df['sentences'].apply(lambda x : len(x.split()) if isinstance(x,str) else 0)
            df['cumulative_len'] = df['word_len'].cumsum()

            
            df['chunk_id'] = (df['cumulative_len'] // self.chunk_size).astype(int)

            # Aggregate sentences into chunks
            chunks = df.groupby('chunk_id')['sentences'].apply(lambda x: ''.join(x))

            del df
            end = time.time()
            logger.info(f"Done Vanilla Chunking in {end-start}secs")
            return chunks, None
        
        except Exception as e:
            logger.error(traceback.format_exc(), exc_info=True)
            return None, traceback.format_exc()



if __name__ == "__main__":
    text = (
        "Natural language processing (NLP) is a subfield of linguistics, computer science, "
        "and artificial intelligence concerned with the interactions between computers and human language. "
        "In particular, how to program computers to process and analyze large amounts of natural language data. "
        "The result is a computer capable of understanding the contents of documents. "
        "This includes the contextual nuances of the language within them. "
        "The technology can then accurately extract information and insights contained in the documents. "
        "It can also categorize and organize the documents themselves."
        "Natural language processing (NLP) is a subfield of linguistics, computer science, "
        "and artificial intelligence concerned with the interactions between computers and human language. "
        "In particular, how to program computers to process and analyze large amounts of natural language data. "
        "The result is a computer capable of understanding the contents of documents. "
        "This includes the contextual nuances of the language within them. "
        "The technology can then accurately extract information and insights contained in the documents. "
        "It can also categorize and organize the documents themselves."     
    )
    df = pd.DataFrame({
        "text": [
            text
    ]})

    chunker = Chunker(chunk_size=100)
    chunks, error = chunker.vanilla_chunks_generation(df)

    for i, chunk in enumerate(chunks, 1):
        print(f"\n--- Chunk {i} ---\n{chunk}")


# # Example usage
# if __name__ == "__main__":
#     text = (
#         "Natural language processing (NLP) is a subfield of linguistics, computer science, "
#         "and artificial intelligence concerned with the interactions between computers and human language. "
#         "In particular, how to program computers to process and analyze large amounts of natural language data. "
#         "The result is a computer capable of understanding the contents of documents. "
#         "This includes the contextual nuances of the language within them. "
#         "The technology can then accurately extract information and insights contained in the documents. "
#         "It can also categorize and organize the documents themselves."
#     )

#     chunker = SentenceChunker(chunk_size=100)
#     chunks = chunker.chunk(text)

#     for i, chunk in enumerate(chunks, 1):
#         print(f"\n--- Chunk {i} ---\n{chunk}")
