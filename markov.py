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
import random, sys, os, re, argparse
from nltk.tokenize import sent_tokenize, word_tokenize

# order used for chain e.g. order-1 maps 1 word prefixes
# to a list of every suffix that occurs for that prefix
ORDER = 2
# maximum length of each generated sentence
MAX_LEN = 100

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
        self.last_words = []
        self.sentence_len = 15
        self.read_file(file)

    def read_file(self, directory):
        # case the user wants to generate text
        # based on a single file
        if os.path.isfile(directory):
            print("single file only")
            with open(directory, "r") as file:
                self.sentences = sent_tokenize(file.read())
                self.construct_dict()
                print(len(self.dict.keys()))
        # case of generating text from directory of files
        else:
            print("directory of files")
            for file in os.listdir(directory):
                with open(os.path.join(os.getcwd(), directory, file), "r", encoding='utf-8') as data:
                    self.sentences = sent_tokenize(data.read())
                    self.construct_dict()
    
    def construct_dict(self):
        # iterate over all sentences, mapping pairs of sequential words
        # to the next word, and its count
        for i, sentence in enumerate(self.sentences):
            removePunctuation = re.compile(".*[a-zA-Z0-9!.].*")
            words = [w.lower() for w in sentence.split() if removePunctuation.match(w)]
            #words = word_tokenize(sentence)
            #self.sentence_len += len(words)
            if len(words) > ORDER:
                self.first_words.append(words[0:ORDER])
                self.last_words.append(words[len(words) - 1])
            # if we iterate up to ORDER words from the end of
            # the sentence, we can construct a sequence of length
            # ORDER, and get the successor, which is ORDER indices
            # ahead of the beginning of the sequence
            for i in range(len(words) - ORDER - 1):
                # get next sequence of ORDER words
                sequence = " ".join(words[i:i + ORDER])
                # get the successor to the sequence of words
                successor = words[i + ORDER]
                # update number of ocurrences of this word
                # sequence, and the number of ocurrences of
                # this successor word to the specified sequence
                if not sequence in self.dict.keys():
                    self.dict[sequence] = [successor]
                    self.seq_count[sequence] = 1
                else:
                    self.seq_count[sequence] += 1
                    self.dict[sequence].append(successor)


class Writer:
    def __init__(self, reader):
        self.reader = reader
    
    def write(self, sentences):
        for i in range(sentences):
            res = self.writeSentence()
            print("tweet " + str(i + 1) + ": " + res + "\n")
    
    def writeSentence(self):
        # choose a first word for the sentence randomly
        res = []
        # store the current prefix
        prefix = random.choice(list(self.reader.dict.keys()))
        for _ in range(MAX_LEN):
            # choose a random suffix for the current prefix, the
            # probability distribution is naturally weighted by the
            # number of ocurrences of each unique suffix after the
            # current prefix, update the current prefix as well
            try:

                # split first word of prefix from remaining
                # words of order-n prefix, output first word
                # and generate suffix for the prefix
                prefix_split = prefix.split()
                word = prefix_split[0]
                prefix_remain = " ".join(prefix_split[1:])
                # add first word from prefix to sentence
                res.append(word)

                # generate suffix for current prefix
                suffix = random.choice(self.reader.dict[prefix])
                # update prefix appending new suffix to end
                # replacing the first word of the prefix
                prefix = prefix_remain + " " + suffix
            # break on words that have n
            except:
                break                 

        # output the produced sentence
        return " ".join(res)
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, help='an input file')
    parser.add_argument('--order', type=int, help='the markov chain order')
    parser.add_argument('--length', type=int, help='the maximum length of each sentence')
    parser.add_argument('--sentences', type=int, help='the number of sentences to generate')
    parser.add_argument('--dir', type=str, help='an input file directory')
    args = parser.parse_args()
    if args.file is None and args.dir is None:
        print("must provide an input file, or file directory (if both provided, will prioritize directory")
        parser.print_usage()
        return
    if args.dir is not None:
        reader = Reader(args.dir)
    else:
        reader = Reader(args.file)
    writer = Writer(reader)
    if args.order is not None:
        ORDER = args.order
    if args.length is not None:
        MAX_LEN = args.length
    # write up to the user-specified number of generated sentences
    writer.write(10 if args.sentences is None else args.sentences)


if __name__ == '__main__':
    
    main()

