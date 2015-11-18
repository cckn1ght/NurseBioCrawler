__author__ = 'Joe'

# analysis the most frequency words used by this file
import csv
import operator
from nltk import word_tokenize
from nltk.stem.porter import *
from nltk.corpus import stopwords


def func_frequency_words():
    csv_name = 'annotated.csv'
    stemmer = PorterStemmer()
    stop_words_list = stopwords.words('english')

    # strings for all words and all names
    all_words_string = ''
    all_name_string = ''
    # open annotated file and pass it to csv reader
    annotated_file = open(csv_name, 'r', encoding='utf-8', errors='ignore')
    annotated_reader = csv.reader(annotated_file)

    bio_freq_yes = {}            # yes class dictionary frequency
    bio_freq_no = {}             # no class dictionary frequency
    name_freq_yes = {}
    name_freq_no = {}

    for line in annotated_reader:
        bio_string = line[7]      # The bio information
        # regular expression filter for all US ASCII Character Set
        bio_string = re.sub(r'[^\x00-\x7f]', r' ', bio_string)
        
        name_string = line[2]   # the name info
        name_string = re.sub(r'[^\x00-\x7f]', r' ', name_string)
        # tokenize name string and bio string
        name_text = word_tokenize(name_string)
        all_name_string = all_name_string + ' ' + name_string
        bio_text = word_tokenize(bio_string)
        all_words_string = all_words_string + ' ' + bio_string
        
        # remove the stop words for bio information
        no_stop_bio_text = [t for t in bio_text if t not in stop_words_list]

        if line[0] in ["yes"]:          # line[0] is the class info
            for word in name_text:
                word = word.lower()
                if word in name_freq_yes:       # create the name_freq_yes list for name words frequency counting
                    name_freq_yes[word] += 1
                else:
                    name_freq_yes[word] = 1
                    
            for word in no_stop_bio_text:       # create bio_freq_yes list for bio words frequency counting
                word = word.lower()
                if word in bio_freq_yes:
                    bio_freq_yes[word] += 1
                else:
                    bio_freq_yes[word] = 1

        # do the same thing for no class
        if line[0] in ["no"]:
            for word in name_text:
                word = word.lower()
                if word in name_freq_no:
                    name_freq_no[word] += 1
                else:
                    name_freq_no[word] = 1
            for word in no_stop_bio_text:
                word = word.lower()
                if word in bio_freq_no:
                    bio_freq_no[word] += 1
                else:
                    bio_freq_no[word] = 1

    all_tokens = word_tokenize(all_words_string)
    unique_words = set(all_tokens)
    print(unique_words)
    print(all_words_string)
    print(len(all_words_string))
    print(len(unique_words))
    annotated_file.close()

    # sort the lists
    words_bio_freq_no_sorted = []
    words_bio_freq_yes_sorted = []
    words_name_freq_yes_sorted = []
    words_name_freq_no_sorted = []

    print("no class name words frequency")
    name_freq_no_sorted = sorted(list(name_freq_no.items()), key=operator.itemgetter(1), reverse=True)
    # store the word in to a new list
    for tup in name_freq_no_sorted:
        words_name_freq_no_sorted.append(tup[0])
    print(name_freq_no_sorted[:])
    print("\n")

    print("yes class name words frequency")
    name_freq_yes_sorted = sorted(list(name_freq_yes.items()), key=operator.itemgetter(1), reverse=True)
    for tup in name_freq_yes_sorted:
        words_name_freq_yes_sorted.append(tup[0])
    print(name_freq_yes_sorted[:])
    print("\n")

    print("no class bio words frequency")
    bio_freq_no_sorted = sorted(list(bio_freq_no.items()), key=operator.itemgetter(1), reverse=True)
    for tup in bio_freq_no_sorted:
        words_bio_freq_no_sorted.append(tup[0])
    print(bio_freq_no_sorted[:])
    print("\n")

    print("yes class bio words frequency")
    bio_freq_yes_sorted = sorted(list(bio_freq_yes.items()), key=operator.itemgetter(1), reverse=True)
    for tup in bio_freq_yes_sorted:
        words_bio_freq_yes_sorted.append(tup[0])
    print(bio_freq_yes_sorted[:])
    print("   ")

    list_automatic_freq_yes = []
    list_automatic_freq_no = []
    list_automatic_freq_name_yes = []
    list_automatic_freq_name_no = []

    # automatic no name words
    for word in words_name_freq_no_sorted:
        if word not in words_name_freq_yes_sorted:
            list_automatic_freq_name_no.append(stemmer.stem(word.lower()))
    # automatic yes name words
    for word in words_name_freq_yes_sorted:
        if word not in words_name_freq_no_sorted:
            list_automatic_freq_name_yes.append(stemmer.stem(word.lower()))

    for word in words_bio_freq_no_sorted:
        if word not in words_bio_freq_yes_sorted:
            list_automatic_freq_no.append(stemmer.stem(word.lower()))

    for word in words_bio_freq_yes_sorted:
        if word not in words_bio_freq_no_sorted:
            list_automatic_freq_yes.append(stemmer.stem(word.lower()))

    print("automatic dictionary yes")
    print(list_automatic_freq_yes)
    print("automatic dictionary no")
    print(list_automatic_freq_no)

    print("automatic name yes")
    print(list_automatic_freq_name_yes)
    print("automatic name no")
    print(list_automatic_freq_name_no)

    def fun_create_files_of_word_lists():
        # write name words into file
        yes_name_file = open('auto_yes_name_file.txt', 'w')
        no_name_file = open('auto_no_name_file.txt', 'w')

        for item in list_automatic_freq_name_no:
            no_name_file.write(item)
            no_name_file.write('\n')

        for item in list_automatic_freq_name_yes:
            yes_name_file.write(item)
            yes_name_file.write('\n')

        yes_name_file.close()
        no_name_file.close()

        # write bio words into file
        yes_list_file = open('auto_yes_list_file.txt', 'w')
        no_list_file = open('auto_no_list_file.txt', 'w')

        for item in list_automatic_freq_no:
            no_list_file.write(item)
            no_list_file.write('\n')

        for item in list_automatic_freq_yes:
            yes_list_file.write(item)
            yes_list_file.write('\n')

        yes_list_file.close()
        no_list_file.close()

    fun_create_files_of_word_lists()


def main():
    func_frequency_words()

if __name__ == "__main__":
    main()
