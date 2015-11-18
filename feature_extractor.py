__author__ = 'Joe'
# extract features to classify if the tweeter user is an individual nurse or not(like organizations or nurse students)
import nltk
import re
import string
import csv
import operator
from nltk import word_tokenize
from nltk.stem.porter import *
from nltk.corpus import stopwords

def fun_feature_extrator():
    stemmer = PorterStemmer()
    yes_list_file = open('auto_yes_list_file.txt', 'r')
    no_list_file = open('auto_no_list_file.txt', 'r')

    yes_name_file = open('auto_yes_name_file.txt', 'r')
    no_name_file = open('auto_no_name_file.txt', 'r')

    from_file_list_automatic_freq_no = []
    from_file_list_automatic_freq_yes = []

    from_file_name_automatic_freq_no = []
    from_file_name_automatic_freq_yes = []

    # remove new line
    for word in yes_list_file.readlines():
        word = word.replace('\n', '')
        from_file_list_automatic_freq_yes.append(word)

    for word in no_list_file.readlines():
        word = word.replace('\n', '')
        from_file_list_automatic_freq_no.append(word)

    for word in yes_name_file.readlines():
        word = word.replace('\n', '')
        from_file_name_automatic_freq_yes.append(word)

    for word in no_name_file.readlines():
        word = word.replace('\n', '')
        from_file_name_automatic_freq_no.append(word)

    yes_list_file.close()
    no_list_file.close()
    yes_name_file.close()
    no_name_file.close()

    # count NNP tags number
    def func_tags_NNP(tag_sequence):
        count_nnp = 0
        for tup in tag_sequence:
            if tup[1] == 'NNP':
                count_nnp += 1
        return count_nnp

    ##########################################################################################
    # count PRP tag number
    def func_tags_PRP(tag_sequence):
        count_prp = 0
        for tup in tag_sequence:
            if tup[1] == 'PRP':
                count_prp += 1
        return count_prp

    ##########################################################################################
    list_automatic_freq_no = from_file_list_automatic_freq_no[:]
    list_automatic_freq_yes = from_file_list_automatic_freq_yes[:]

    name_automatic_freq_no = from_file_name_automatic_freq_no[:]
    name_automatic_freq_yes = from_file_name_automatic_freq_yes[:]
    print("bio frequency no:")
    print(list_automatic_freq_no)
    print("bio frequency yes:")
    print(list_automatic_freq_yes)
    print("name frequency no:")
    print(name_automatic_freq_no)
    print("name frequency yes:")
    print(name_automatic_freq_yes)

    ##########################################################################################
    def automatic_freq_no(text, no_list):
        count_words = 0

        for word in text:
            word1 = stemmer.stem(word.lower())
            if word1 in no_list:
                count_words += 1
        return count_words

    ########################################################################################

    def automatic_freq_yes(text, yes_list):
        count_words = 0

        for word in text:
            word1 = stemmer.stem(word.lower())
            if word1 in yes_list:
                count_words += 1
        return count_words


    ##########################################################################################

    def bio_func_No_freq_terms(text):
        count_words = 0
        no_freq_terms = ['best', 'certified', 'future', 'assistant', 'health', 'credit', 'free', 'safety',
                         'clinical', 'organization']
        for word in text:
            if word in no_freq_terms:
                count_words += 1
        return count_words

    ##########################################################################################
    '''def name_func_No_freq_terms(text):
        count_words = 0
        no_freq_terms = ['enterprise']
        for word in text:
            if word in no_freq_terms:
                count_words += 1
        return count_words'''
    ##########################################################################################

    def bio_func_Yes_freq_terms(text):
        count_words = 0
        yes_freq_terms = ['registered', 'student', 'love', 'wife', 'health', 'university', 'my', 'proud', 'lover',
                          'girl', 'fan', 'family', 'mental', 'daughter', 'school', 'singer', 'sister', 'food']
        for word in text:
            if word in yes_freq_terms:
                count_words += 1
        return count_words

    ##########################################################################################

    '''def name_func_Yes_freq_terms(text):
        count_words = 0
        yes_freq_terms = ['registered', 'student', 'love', 'wife', 'health', 'university', 'my', 'proud', 'lover',
                          'girl', 'fan', 'family', 'mental', 'daughter', 'school', 'singer', 'sister', 'food']
        for word in text:
            if word in yes_freq_terms:
                count_words += 1
        return count_words'''
    ##########################################################################################

    csv_name = 'annotated.csv'
    file_pronouns = 'pronouns.txt'
    output_file = 'features.csv'
    feature_writer = csv.writer(open(output_file, 'w', newline=''))
    annotated_file = open(csv_name, 'r', encoding='utf-8', errors='ignore')
    annotated_reader = csv.reader(annotated_file)

    f_pronouns = open(file_pronouns, 'r')
    f_output = open(output_file, 'w')

    ##################################################################

    list_pronouns = word_tokenize(f_pronouns.read())


    #################################################################
    # write the first row
    feature_writer.writerow(['screen_name', 'followers_count', 'following_count', 'bio_pronouns_count',
                             'bio_NNP_tags',  'bio_PRP_tags',
                             'bio_Yes_freq_terms', 'bio_No_freq_terms',
                             'bio_auto_Yes_freq_terms', 'name_auto_Yes_freq_terms',
                             'bio_auto_No_freq_terms', 'name_auto_No_freq_terms', 'class'])

    #################################################################
    # for each line of csv reader, extract the feature into a new csv file "features.csv"
    for line in annotated_reader:
        if annotated_reader.line_num == 1:
            continue  # skip the first row
        the_vector = []

        bio_string = line[7]
        bio_string = re.sub(r'[^\x00-\x7f]', r' ', bio_string)

        name_string = line[2]
        name_string = re.sub(r'[^\x00-\x7f]', r' ', name_string)

        bio_text = word_tokenize(bio_string)
        name_text = word_tokenize(name_string)
        bio_tag_sequence = nltk.pos_tag(bio_text)
        name_tag_sequence = nltk.pos_tag(name_string)

        ###########################################################################

        print('########################################################')
        print('########################################################')
        print('########################################################')
        print('########################################################')
        print('########################################################')
        print('########################################################')
        print('########################################################')
        print('########################################################')
        print('########################################################')
        print('########################################################')

        #####################################################################
        bio_pronouns_count = 0
        for token in bio_text:
            if token in list_pronouns:
                print('@@@@@@@@@@@@@@@@@begin')
                print(token)
                print('@@@@@@@@@@@@@@@@@@end')
                bio_pronouns_count += 1

        #####################################################################
        screen_name = line[1]
        followers_count = line[4]
        following_count = line[5]
        bio_pronouns_count = bio_pronouns_count
        bio_NNP_tags = func_tags_NNP(bio_tag_sequence)
        bio_PRP_tags = func_tags_PRP(bio_tag_sequence)
        bio_Yes_freq_terms = bio_func_Yes_freq_terms(bio_text)
        # name_Yes_freq_terms = func_Yes_freq_terms(name_text)
        bio_No_freq_terms = bio_func_No_freq_terms(bio_text)
        # name_No_freq_terms = func_No_freq_terms(name_text)
        bio_auto_Yes_freq_terms = automatic_freq_yes(bio_text, list_automatic_freq_yes)
        name_auto_Yes_freq_terms = automatic_freq_yes(name_text, name_automatic_freq_yes)
        bio_auto_No_freq_terms = automatic_freq_no(bio_text, list_automatic_freq_no)
        name_auto_No_freq_terms = automatic_freq_no(name_text, name_automatic_freq_no)

        claatype = line[0]

        the_vector = [screen_name, followers_count, following_count, bio_pronouns_count, bio_NNP_tags,
                      bio_PRP_tags, bio_Yes_freq_terms, bio_No_freq_terms, bio_auto_Yes_freq_terms,
                      name_auto_Yes_freq_terms, bio_auto_No_freq_terms, name_auto_No_freq_terms,
                      claatype]

        ############################################################

        print('###################################################')
        print(line)
        print(bio_string)
        print(bio_text)
        print(name_text)
        print(bio_tag_sequence)
        print(name_tag_sequence)
        print(the_vector)
        print('###################################################')

        feature_writer.writerow(the_vector)


    ##################################################################

    ##################################################################

    f_pronouns.close()
    f_output.close()
    print('<<<<<<<<<<<<<DONE>>>>>>>>>>>')


def main():
    fun_feature_extrator()

if __name__ == "__main__":
    main()
