from math import log, exp
from collections import Counter
import random

class TextClassifier:
    """
    In this question, you will implement a classifier that predicts
    the number of stars a reviewer gave a movie from the text of the review.

    You will process the reviews in the dataset we provide, then
    implement a Naive Bayes classifier to do the prediction.

    But first, some math!
    """

    def q0(self):
        """
        Return your full name as it appears in the class roster
        """
        return ['Gabriela Merz', 'Larry Guo']

    def q1(self):
        """
        Suppose you roll a 4-sided die of unknown bias, and you observe
        the following sequence of values:
        3   1   4   4   2   1   2   4   2   1   2   1   1   1   1   4   3   4   4   1
        Given only this information, what are the most likely
        probabilities of rolling each side? (Hardcoding is fine)
        """
        # we have 20 total rolls, so our most likely probabilities
        # are thed number of times a value appears / total number
        # of times we roll 
        return [0.4, 0.2, 0.1, 0.3]

    def q2(self):
        """
        You just fit a multinomial distribution!

        Now suppose you have a prior belief that the die is fair.
        After some omitted math involving a conjugate Dirichlet distribution,
        you realize that you can encode this prior by simply adding
        some "fake" observations of each side. The number of observations
        is the "strength" of your prior belief.
        Using the same observations as in q1 and a prior with a per-side
        "strength" of 2, what are the probabilities of rolling each side??
        """
        # just get back our original values from q1 by multiplying
        # by 20, then add 2 and divide by our new total, 28
        return [(x * 20.0 + 2)/28 for x in self.q1()]

    def q3(self, counts=[1,1,3,8]):
        """
        You might be wondering what dice have to do with NLP.
        We will model each possible rating (one of the five numbers of stars)
        as a die, with each word in the dictionary as a face.

        This is a multinomial Naive Bayes classifier, because the words are
        drawn from a per-rating multinomial distribution and we treat
        each word in a review as independent (conditioned on the rating). That is,
        once the rating has emitted one word to the review, the next word
        has the same distribution over possible values as the first.

        In this question, you will write a function that computes p(word|rating), the
        probability that the rating under question will produce
        each of the four words in our dictionary. We will run this function
        5 times, once for each rating. We pass in the number of times each
        word shows up in any review corresponding to the current rating.
        """
        # we again apply the naive definition of probability 
        return [float(x)/sum(counts) for x in counts]

    def q4(self, infile):
        """
        You'll notice that actual words didn't appear in the last question.
        Array indices are nicer to work with than words, so we typically
        write a dictionary encoding the words as numbers. This turns
        review strings into lists of integers. You will count the occurrences
        of each integer in reviews of each class.

        The infile has one review per line, starting with the rating and then a space.
        Note that the "words" include things like punctuation and numbers. Don't worry
        about this distinction for now; any string that occurs between spaces is a word.

        You must do three things in this question: build the dictionary,
        count the occurrences of each word in each rating and count the number
        of reviews with each rating.
        The words should be numbered sequentially in the order they first appear.
        counts[ranking][word] is the number of times word appears in any of the
        reviews corresponding to ranking
        nrated[ranking] is the total number of reviews with each ranking
        """
        self.nrated = [0 for _ in xrange(5)]
        count = 0
        self.dict = {}
        rankingWords = [Counter() for _ in xrange(5)]
        with open(infile, 'r') as f: 
            for line in f: 
                # parse information 
                words = line.split(' ')
                ranking, words = int(words[0]), [word.strip('\n') for word in words[1:]]

                # update rankings + words in rankings
                self.nrated[ranking] += 1
                rankingWords[ranking].update(words)

                # iterate through words + add them to word -> idx dict
                for word in words: 
                    if word not in self.dict: 
                        self.dict[word] = count 
                        count += 1 
        # initialize 
        self.counts = [[0 for _ in xrange(count)] for _ in xrange(5)]

        # iterate
        for ranking, wordCounter in enumerate(rankingWords): 
            for word in wordCounter.iterkeys():
                self.counts[ranking][self.dict[word]] = wordCounter[word]

    def q5(self, alpha=1):
        """
        Now you'll fit the model. For historical reasons, we'll call it F.
        F[rating][word] is -log(p(word|rating)).
        The ratings run from 0-4 to match array indexing.
        Alpha is the per-word "strength" of the prior (as in q2).
        (What might "fairness" mean here?)
        # """
        model = [[0 for _ in range(len(self.dict))] for _ in xrange(5)]
        for ranking, wordList in enumerate(self.counts):
            wordTotalSum = float(sum(wordList) + len(wordList) * alpha)
            for wordIdx, wordTotal in enumerate(wordList): 
                val = (wordTotal + alpha) / wordTotalSum
                if val != 0: 
                    model[ranking][wordIdx] = -1 * log(val)

        self.F = model

    def q6(self, infile):
        """
        Test time! The infile has the same format as it did before. For each review,
        predict the rating. Ignore words that don't appear in your dictionary.
        Are there any factors that won't affect your prediction?
        You'll report both the list of predicted ratings in order and the accuracy.
        """

        # p(ranking | words) = p(words | ranking)p(ranking)/p(words)
        # p(words) is constant so we don't care
        correctPredictions, totalPredictions = 0,0 
        predictionList = []
        rankingProbs = [float(rTotal) / sum(self.nrated) for rTotal in self.nrated]
        rankingProbs = map(lambda num: -log(num) if num != 0 else 0, rankingProbs)
        with open(infile, 'r') as f: 
            for line in f: 
                words = line.split(' ')
                rating, words = int(words[0]), [word.strip('\n') for word in words[1:]]
                wordsGivenRankings = [0 for _ in xrange(5)]
                for word in words: 
                    if word in self.dict: 
                        for ranking in xrange(5): 
                            # log probability so we add? 
                            wordsGivenRankings[ranking] += self.F[ranking][self.dict[word]]
                finalProbs = [wordsGivenRankings[idx] + rankingProbs[idx]  for idx in xrange(5)]
                prediction = finalProbs.index(min(finalProbs))
                predictionList.append(prediction)
                correctPredictions += int(prediction == rating)
                totalPredictions += 1 
        # print predictionList
        accuracy = correctPredictions / float(totalPredictions)
        return (predictionList, accuracy)

    def q7(self, infile):
        """
        Alpha (q5) is a hyperparameter of this model - a tunable option that affects
        the values that appear in F. Let's tune it!
        We've split the dataset into 3 parts: the training set you use to fit the model
        the validation and test sets you use to evaluate the model. The training set
        is used to optimize the regular parameters, and the validation set is used to
        optimize the hyperparameters. (Why don't you want to set the hyperparameters
        using the test set accuracy?)
        Find and return a good value of alpha (hint: you will want to call q5 and q6).
        What happens when alpha = 0?
        """
        # apparently 2 is pretty good for STSA
        bestAcc = 0
        bestAlpha = 1
        for i in xrange(1, 11):
            newAlpha = i
            self.q5(newAlpha)
            _, newAcc  = self.q6(infile)
            if newAcc >= bestAcc:
                bestAcc = newAcc
                bestAlpha = newAlpha

        return bestAlpha

    def q8(self):
        """
        We can also "hallucinate" reviews for each rating. They won't make sense
        without a language model (for which you'll have to take CS287), but we can
        list the 3 most representative words for each class. Representative here
        means that the marginal information it provides (the minimal difference between
        F[rating][word] and F[rating'][word] across all rating' != rating) is maximal.
        You'll return the strings rather than the indices, and in decreasing order of
        representativeness.
        """
        # Let's initialize some data structures!!!!!
        revDict = {v: k for k, v in self.dict.iteritems()}
        topThree = [[None for _ in xrange(3)] for _ in range(5)]


        for rating, wordList in enumerate(self.F):
            wordDiff = [float('inf') for _ in revDict]
            for ratingP, wordListP in enumerate(self.F):
                if rating == ratingP:
                    continue
                for word, val in enumerate(wordList):
                    diff = wordListP[word] - val
                    if diff < wordDiff[word]:
                        wordDiff[word] = diff

            sortedWordDiff = sorted(list(enumerate(wordDiff)), key=lambda item: item[1], reverse=True)
            for i in xrange(3):
                topThree[rating][i] = revDict[sortedWordDiff[i][0]]
                print topThree[rating][i]

        return topThree

    """
    You did it! If you're curious, the dataset came from (Socher 2013), which describes
    a much more sophisticated model for this task.
    Socher, R., Perelygin, A., Wu, J. Y., Chuang, J., Manning, C. D., Ng, A. Y., and Potts, C. (2013). Recursive deep models for semantic compositionality over a sentiment treebank. In Proceedings of the conference on empirical methods in natural language processing (EMNLP), volume 1631, page 1642. Citeseer.
    """

if __name__ == '__main__':
    c = TextClassifier()
    print "Processing training set..."
    c.q4('mini.train')
    print len(c.dict), "words in dictionary"
    print "Fitting model..."
    c.q5()
    print "Accuracy on validation set:", c.q6('mini.valid')[1]
    print "Good alpha:", c.q7('mini.valid')
    c.q5() #reset alpha
    print "Happy words:", " and ".join(c.q8()[4][:2])
