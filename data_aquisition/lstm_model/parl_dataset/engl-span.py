# Count a number of words and lines

from mrjob.job import MRJob
import string

# remove_punct_map = dict.fromkeys(map(ord, string.punctuation)) #thank you Reed

class TextOverview(MRJob):

    def mapper(self, _, line):
        
        # line = line.translate(remove_punct_map)
        # line = line.lower()
        
        yield "total_words", len(line.split())
        yield "lines", 1

    def reducer(self, key, values):
        yield key, sum(values)


if __name__ == '__main__':
    TextOverview.run()

# Count a number of unique words


# from mrjob.job import MRJob
# import string

# remove_punct_map = dict.fromkeys(map(ord, string.punctuation))

# class TextOverview(MRJob):

#     def mapper(self, _, line):

#         line = line.translate(remove_punct_map)
#         line = line.lower()

#         for word in line.split():
#             yield 'unique_words', word

#     def reducer(self, key, values):
#         yield key, len(set(values))
    


# if __name__ == '__main__':
#     TextOverview.run()