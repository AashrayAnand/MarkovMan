# this class implements a Markov Chain, it includes
# the following core functionality

# Reader: implementation of a reader, which reads input
# text data, and creates an order-2 dictionary, mapping
# pairs of two words (that appeared in sequential order)
# to a a list of successor lists, which each include a word
# which succeeded the word pair somewhere in the text, and
# the proportion of ocurrences of the successor out of the
# total ocurrences of the word pair

# Writer: implementation of a writer, which consumes a
# reader generated markov chain, and randomly generates text
# based on the provided sequential relations between words
# in the text
import random, sys, os
from nltk.tokenize import sent_tokenize, word_tokenize

ORDER = 1

class Reader:
    def __init__(self, file):
        # list to store sentence tokenized data
        self.sentences = []
        # dictionary to store [word, word] -> [[word, word_count],...]
        # data
        self.dict = {}
        self.seq_count = {}
        # read the input data
        self.first_words = []
        self.sentence_len = 0
        self.read_file(file)

    def read_file(self, directory):
        for file in os.listdir(directory):
            with open(file, "r", encoding='utf-8') as data:
                self.sentences = sent_tokenize(data.read())
                self.construct_dict()
    
    def construct_dict(self):
        # iterate over all sentences, mapping pairs of sequential words
        # to the next word, and its count
        for i, sentence in enumerate(self.sentences):
            words = word_tokenize(sentence)
            self.sentence_len += len(words)
            if len(words) > 0:
                self.first_words.append(words[0])
            # if we iterate up to ORDER words from the end of
            # the sentence, we can construct a sequence of length
            # ORDER, and get the successor, which is ORDER indices
            # ahead of the beginning of the sequence
            for i in range(len(words) - ORDER):
                # get next sequence of ORDER words
                sequence = words[i]
                # get the successor to the sequence of words
                successor = words[i + 1]
                # update number of ocurrences of this word
                # sequence, and the number of ocurrences of
                # this successor word to the specified sequence
                if not sequence in self.dict.keys():
                    self.dict[sequence] = [successor]
                    self.seq_count[sequence] = 1
                else:
                    self.seq_count[sequence] += 1
                    self.dict[sequence].append(successor)
        self.sentence_len //= len(self.sentences)

class Writer:
    def __init__(self, reader):
        self.reader = reader
    
    def write(self, sentences):
        for _ in range(sentences):
            self.writeSentence()
    
    def writeSentence(self):
        # choose a first word for the sentence randomly
        res = random.choice(self.reader.first_words)
        # store the current prefix
        curr = res
        for _ in range(self.reader.sentence_len):
            # choose a random suffix for the current prefix, the
            # probability distribution is naturally weighted by the
            # number of ocurrences of each unique suffix after the
            # current prefix, update the current prefix as well
            curr = random.choice(self.reader.dict[curr])
            # build the sentence up
            res += " " + curr
        # output the produced sentence
        print(res)
    
def main():
    if len(sys.argv) < 2:
        print("usage: python markov.py <FILE>")
        return
    reader = Reader(sys.argv[1])
    writer = Writer(reader)
    writer.write(10)


if __name__ == '__main__':
    
    main()

