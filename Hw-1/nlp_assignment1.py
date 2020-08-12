from collections import Counter
import re
import random
import math

globals()
bigrams = []
trigrams = []
unigram_tokens = {'': ''}
unigram_probabilities = {'': ''}
bigram_tokens = {'': ''}
bigram_probabilities = {'': ''}
trigram_tokens = {'': ''}
trigram_probabilities = {'': ''}

#split sentences to unigram tokens
def unigram(sentences):
    unigrams = []
    for i in range(0, len(sentences)):
        tokens = sentences[i].split(" ")
        tokens.insert(0, "<s>")
        tokens.insert(len(tokens), "</s>")
        for k in tokens:
            if k == "":
                tokens.remove(k)
        unigrams.extend([(tokens[i]) for i in range(0, len(tokens))])
    global unigram_tokens
    unigram_tokens = Counter(unigrams)

    global unigram_probabilities

    unigram_probabilities = Counter(unigrams)
    array = unigram_probabilities.values()
    sumofallwords = 0
    for g in array:
        sumofallwords += g

    del unigram_probabilities['']

    for word in unigram_probabilities:
        unigram_probabilities[word] = unigram_probabilities[word] / sumofallwords

#split sentences to bigram tokens
def bigram(sentences):
    global bigrams

    for i in range(0, len(sentences)):
        tokens = sentences[i].split(" ")
        tokens.insert(0, "<s>")
        tokens.insert(len(tokens), "</s>")
        for k in tokens:
            if k == "":
                tokens.remove(k)

        bigrams.extend([(tokens[i + 1] + "|" + tokens[i]) for i in range(0, len(tokens) - 1)])

    global bigram_tokens
    global bigram_probabilities
    bigram_tokens = Counter(bigrams)

    bigram_probabilities.update(bigram_tokens)
    del bigram_probabilities[""]
    array = bigram_tokens.values()

    sumofallwords = 0
    for g in array:
        sumofallwords += g

#split sentences to trigram tokens
def trigram(sentences):
    global trigrams
    for i in range(0, len(sentences)):
        tokens = sentences[i].split(" ")
        tokens.insert(0, "<s>")
        tokens.insert(0, "<s>")
        tokens.insert(len(tokens), "</s>")
        tokens.insert(len(tokens), "</s>")
        for k in tokens:
            if k == "":
                tokens.remove(k)

        trigrams.extend([(tokens[i + 2] + "|" + tokens[i] + " " + tokens[i + 1]) for i in range(0, len(tokens) - 2)])
    global trigram_tokens
    trigram_tokens = Counter(trigrams)
    global trigram_probabilities

    trigram_probabilities.update(trigram_tokens)
    del trigram_probabilities[""]
    array = trigram_tokens.values()

    sumofallwords = 0
    for g in array:
        sumofallwords += g

    for word in trigram_probabilities:
        trigram_probabilities[word] = trigram_probabilities[word] / sumofallwords

#calculate smooted probability of generated sentence
def sprob(sentence):
    bigram_probability = 0
    splitted_sentence = sentence.split(' ')
    if splitted_sentence.__contains__(''):
        splitted_sentence.remove('')

    prob_array_bigram = []
    for i in range(0, len(splitted_sentence) - 1):
        prob_array_bigram.append(bigrams.count(splitted_sentence[i + 1] + "|" + splitted_sentence[i]) + 1 / (unigram_tokens[splitted_sentence[i]] + len(unigram_tokens)))

    for j in prob_array_bigram:
        bigram_probability = bigram_probability + math.log2(j)
    # trigram
    trigram_probability = 0
    sentence_trigram = '<s>' + sentence + '</s>'
    splitted_sentence2 = sentence_trigram.split(' ')
    if splitted_sentence2.__contains__(''):
        splitted_sentence2.remove('')

    prob_array_trigram = []
    for i in range(0, len(splitted_sentence2) - 2):
        prob_array_trigram.append(trigrams.count(
            splitted_sentence2[i + 2] + "|" + splitted_sentence2[i] + " " + splitted_sentence2[i + 1]) + 1 / (bigrams.count(splitted_sentence2[i] + " " + splitted_sentence2[i + 1]) + len(bigram_tokens)))
    for j in prob_array_trigram:
        trigram_probability = trigram_probability + math.log2(j)

    array = [bigram_probability, trigram_probability]
    return array

#calculate probability of generated sentence
def prob(sentence):
    probability = 0
    unigram_probability = 0
    bigram_probability = 0
    trigram_probability = 0
    probabilities = []
    all_probabilities = []
    # probability for unigram
    splitted_sentence = sentence.split(' ')
    if splitted_sentence.__contains__(''):
        splitted_sentence.remove('')

    for word in splitted_sentence:
        unigram_probability = unigram_probability + math.log2(unigram_probabilities[word])

    # probability for bigram

    splitted_sentence = sentence.split(' ')
    if splitted_sentence.__contains__(''):
        splitted_sentence.remove('')

    prob_array_bigram = []
    for i in range(0, len(splitted_sentence) - 1):
        if bigrams.count(splitted_sentence[i + 1] + "|" + splitted_sentence[i]) == 0 or unigram_tokens[splitted_sentence[i]] == 0:
            probabilities = sprob(sentence)
            bigram_probability = probabilities[0]
        else:
            prob_array_bigram.append(
                bigrams.count(splitted_sentence[i + 1] + "|" + splitted_sentence[i]) / unigram_tokens[splitted_sentence[i]])
            if i == len(splitted_sentence) - 1:
                for j in prob_array_bigram:
                    bigram_probability = bigram_probability + math.log2(j)

    # probability for trigram
    sentence_trigram = sentence

    splitted_sentence = sentence_trigram.split(' ')
    if splitted_sentence.__contains__(''):
        splitted_sentence.remove('')
    prob_array_trigram = []
    for i in range(0, len(splitted_sentence) - 2):

        if trigrams.count(splitted_sentence[i + 2] + "|" + splitted_sentence[i] + " " + splitted_sentence[i + 1]) == 0 or bigrams.count(splitted_sentence[i] + " " + splitted_sentence[i + 1]) == 0:
            sprob(sentence)
            probabilities = sprob(sentence)
            bigram_probability = probabilities[0]
            trigram_probability = probabilities[1]
        else:

            prob_array_trigram.append(trigrams.count(splitted_sentence[i + 2] + "|" + splitted_sentence[i] + " " + splitted_sentence[i + 1]) / bigrams.count(splitted_sentence[i] + " " + splitted_sentence[i + 1]))
            if i == len(splitted_sentence) - 2:
                for j in prob_array_trigram:
                    trigram_probability = trigram_probability + math.log2(j)
    all_probabilities = [unigram_probability, bigram_probability, trigram_probability]
    return all_probabilities

#calculate perplexity of generated sentence
def ppl(sentence):
    probabilities = []
    perplexities = []
    probabilities = prob(sentence)
    unigram_perplexity = pow(2, (-1 / len(sentence)) * probabilities[0])
    bigram_perplexity = pow(2, (-1 / len(sentence) - 2) * probabilities[1])
    trigram_perplexity = pow(2, (-1 / len(sentence) - 2) * probabilities[2])
    perplexities = [unigram_perplexity, bigram_perplexity, trigram_perplexity]
    return probabilities, perplexities


def dataset(path):
    with open(path) as f:
        read_data = f.read()
    splitted = re.split(' \.\n| \?\n| \!\n|\n', read_data)
    characters_to_remove = ".,!:;`-_\t|'\"?0123456789"

    for i in range(0, len(splitted)):
        for character in characters_to_remove:
            splitted[i] = splitted[i].replace(character, " ")
            splitted[i] = splitted[i].replace("   ", " ")
            splitted[i] = splitted[i].replace("  ", " ")
            splitted[i] = splitted[i].replace(" s ", "'s ")
            splitted[i] = splitted[i].replace("XXXXX", "")

    return splitted


def next(word):
    # bigram next word
    if not word.__contains__(' '):
        next_word = ''
        new_bigram_tokens = {'': ''}

        for a in bigram_tokens:
            value = bigram_tokens[a]
            a = a.split("|")

            if a[1] == word:
                new_bigram_tokens[a[0]] = value
        del new_bigram_tokens[""]

        sum = 0

        for i in new_bigram_tokens:
            sum = sum + new_bigram_tokens[i]
        counter = 0
        for key in new_bigram_tokens:
            new_bigram_tokens[key] = new_bigram_tokens[key] / sum

            if counter != 0:
                new_bigram_tokens[key] = new_bigram_tokens[key] + list(new_bigram_tokens.items())[counter - 1][1]
            counter = counter + 1
        number = random.randrange(1, 100, 1)
        number = number / 100
        smalllist = []
        biglist = []
        if number >= 0.5:

            if len(new_bigram_tokens) == 1:
                next_word = key
            else:
                for key in new_bigram_tokens:
                    if new_bigram_tokens[key] >= number:
                        biglist.append(new_bigram_tokens[key])
                    if new_bigram_tokens[key] <= number:
                        smalllist.append(new_bigram_tokens[key])

                for key in new_bigram_tokens:
                    if len(biglist) == 0:
                        for key in new_bigram_tokens:
                            if new_bigram_tokens[key] is max(smalllist):
                                next_word = key
                    else:
                        if new_bigram_tokens[key] is min(biglist):
                            next_word = key

        elif number < 0.5:

            if len(new_bigram_tokens) == 1:
                next_word = key
            else:
                for key in new_bigram_tokens:
                    if new_bigram_tokens[key] <= number:
                        smalllist.append(new_bigram_tokens[key])
                    if new_bigram_tokens[key] >= number:
                        biglist.append(new_bigram_tokens[key])
                for key in new_bigram_tokens:
                    if len(smalllist) == 0:
                        for key in new_bigram_tokens:
                            if new_bigram_tokens[key] is min(biglist):
                                next_word = key
                    else:
                        if new_bigram_tokens[key] is max(smalllist):
                            next_word = key

        return next_word

    # trigram next word
    else:


        next_word = ''
        new_trigram_tokens = {'': ''}
        for a in trigram_tokens:
            value = trigram_tokens[a]
            a = a.split("|")
            if a[1] == word:
                new_trigram_tokens[a[0]] = value
        del new_trigram_tokens[""]
        sum = 0

        for i in new_trigram_tokens:
            sum = sum + new_trigram_tokens[i]
        counter = 0
        for key in new_trigram_tokens:
            new_trigram_tokens[key] = new_trigram_tokens[key] / sum

            if counter != 0:
                new_trigram_tokens[key] = new_trigram_tokens[key] + list(new_trigram_tokens.items())[counter - 1][1]
            counter = counter + 1
        number = random.randrange(1, 100, 1)
        number = number / 100
        smalllist = []
        biglist = []
        if number >= 0.5:

            if len(new_trigram_tokens) == 1:
                next_word = key
            else:
                for key in new_trigram_tokens:
                    if new_trigram_tokens[key] >= number:
                        biglist.append(new_trigram_tokens[key])
                    if new_trigram_tokens[key] <= number:
                        smalllist.append(new_trigram_tokens[key])

                for key in new_trigram_tokens:
                    if len(biglist) == 0:
                        for key in new_trigram_tokens:
                            if new_trigram_tokens[key] is max(smalllist):
                                next_word = key
                    else:
                        if new_trigram_tokens[key] is min(biglist):
                            next_word = key

        elif number < 0.5:

            if len(new_trigram_tokens) == 1:
                next_word = key
            else:
                for key in new_trigram_tokens:
                    if new_trigram_tokens[key] <= number:
                        smalllist.append(new_trigram_tokens[key])
                    if new_trigram_tokens[key] >= number:
                        biglist.append(new_trigram_tokens[key])
                for key in new_trigram_tokens:
                    if len(smalllist) == 0:
                        for key in new_trigram_tokens:
                            if new_trigram_tokens[key] is min(biglist):
                                next_word = key
                    else:
                        if new_trigram_tokens[key] is max(smalllist):
                            next_word = key
        return next_word


def generate(count, length):
    index = 0
    counter = 0
    added_unigram_probabilities = unigram_probabilities
    for word in added_unigram_probabilities:
        if counter != 0:
            added_unigram_probabilities[word] = added_unigram_probabilities[word] + \
                                                list(added_unigram_probabilities.items())[counter - 1][1]

        counter = counter + 1

  #------------------------------------------------GENERATE UNIGRAM SENTENCES---------------------------------------------------
    for i in range(0, count):
        unigram_sentence = ''
        finish_token = 0
        sentence_length = 0
        while sentence_length != length:
            number = random.randrange(1, 100, 1)
            number = number/100
            biglist = []
            smalllist = []
            if number >= 0.5:

                for word in added_unigram_probabilities:
                    if added_unigram_probabilities[word] >= number:
                        biglist.append(added_unigram_probabilities[word])
                    if added_unigram_probabilities[word] <= number:
                        smalllist.append(added_unigram_probabilities[word])

                for word in added_unigram_probabilities:
                    if len(biglist) == 0:
                        if added_unigram_probabilities[word] is max(smalllist):
                            if word == '</s>':
                                break

                            if word != '<s>' and word != '</s>':
                                unigram_sentence = unigram_sentence + " " + word
                                sentence_length = sentence_length + 1
                    else:
                        if added_unigram_probabilities[word] is min(biglist):

                            if word == '</s>':
                                break

                            if word != '<s>' and word != '</s>':
                                unigram_sentence = unigram_sentence+" "+word
                                sentence_length = sentence_length+1
            if number < 0.5:

                for word in added_unigram_probabilities:
                    if added_unigram_probabilities[word] <= number:
                        smalllist.append(added_unigram_probabilities[word])
                    if added_unigram_probabilities[word] >= number:
                        biglist.append(added_unigram_probabilities[word])

                for word in added_unigram_probabilities:
                    if len(smalllist) == 0:
                        if added_unigram_probabilities[word] is min(biglist):

                            if word == '</s>':
                                finish_token = 1

                            if word != '<s>' and word != '</s>':
                                unigram_sentence = unigram_sentence + " " + word
                                sentence_length = sentence_length + 1
                    else:
                        if added_unigram_probabilities[word] is max(smalllist):
                            if word == '</s>':
                                finish_token = 1

                            if word != '<s>' and word != '</s>':
                                unigram_sentence = unigram_sentence+" "+ word
                                sentence_length = sentence_length + 1

        results_unigram = []
        results_unigram=ppl(unigram_sentence)
        print(index+1,". UNIGRAM SENTENCE :"+unigram_sentence)
        print("Unigram Probability:",results_unigram[0][0])
        print("Unigram Perplexity:",results_unigram[1][0])
        print("Bigram Probability:", results_unigram[0][1])
        print("Bigram Perplexity:", results_unigram[1][1])
        print("Trigram Probability:", results_unigram[0][2])
        print("Trigram Perplexity:", results_unigram[1][2])
        index = index + 1



     #------------------------------------------------GENERATE BIGRAM SENTENCES---------------------------------------------------

    index = 0
    for i in range(0, count):
        bigram_sentence = '<s>'
        finish_token = 0
        bigram_length = 0
        next_word = ''
        while bigram_length != length and finish_token == 0:
            if bigram_length > 0:
                next_word = next(next_word)

                if next_word == '</s>':
                    finish_token = 1
                else:
                    bigram_length = bigram_length+1
                    bigram_sentence = bigram_sentence+" "+next_word

            if bigram_length == 0:
                next_word = next('<s>')
                if next_word == '</s>':
                    finish_token = 1
                else:
                    bigram_length = bigram_length+1
                    bigram_sentence = bigram_sentence+" "+next_word

        bigram_sentence = bigram_sentence+" </s>"
        results_bigram = []
        results_bigram = ppl(bigram_sentence)
        print(index + 1, ". BIGRAM SENTENCE : " + bigram_sentence)
        print("Unigram Probability:", results_bigram[0][0])
        print("Unigram Perplexity:", results_bigram[1][0])
        print("Bigram Probability:", results_bigram[0][1])
        print("Bigram Perplexity:", results_bigram[1][1])
        print("Trigram Probability:", results_bigram[0][2])
        print("Trigram Perplexity:", results_bigram[1][2])
        index = index + 1

    index = 0

    #------------------------------------------------GENERATE TRIGRAM SENTENCES---------------------------------------------------
    for i in range(0, count):
        trigram_sentence = '<s> <s>'
        finish_token = 0
        trigram_length = 0
        next_word_second = ''
        next_word_first = ''
        while trigram_length != length and finish_token == 0:
            if trigram_length > 0:


                a=next_word_second
                next_word_second = next(next_word_first+" "+next_word_second)
                next_word_first=a

                if next_word_second == '</s>':
                    finish_token = 1
                else:
                    trigram_length=trigram_length+1
                    trigram_sentence = trigram_sentence+" "+next_word_second

            if trigram_length == 0:
                next_word_second = next('<s> <s>')
                next_word_first= '<s>'
                if next_word_second == '</s>':
                    finish_token = 1
                else:
                    trigram_length=trigram_length+1
                    trigram_sentence = trigram_sentence+" "+next_word_second

        trigram_sentence = trigram_sentence+" </s> </s>"
        results_trigram = []
        results_trigram = ppl(trigram_sentence)
        print(index + 1, ". TRIGRAM SENTENCE : " + trigram_sentence)
        print("Unigram Probability:", results_trigram[0][0])
        print("Unigram Perplexity:", results_trigram[1][0])
        print("Bigram Probability:", results_trigram[0][1])
        print("Bigram Perplexity:", results_trigram[1][1])
        print("Trigram Probability:", results_trigram[0][2])
        print("Trigram Perplexity:", results_trigram[1][2])
        index = index + 1





sentences = dataset("dataset.txt")
sentences.remove('')
unigram(sentences)
bigram(sentences)
trigram(sentences)
generate(3,20)
