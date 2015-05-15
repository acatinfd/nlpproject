Topics
====
The experiment is similar to that http://www.vladsandulescu.com/topic-prediction-lda-user-reviews/.

Denpendencies:
Get the preprocessed Yelp review data set and import it from the python object file into my local 
MongoDB by running yelp-reviews.py file. Use MongoDB save my time for not writing to a text file 
again. I also use PyMongo, NLTK, NLTK data (in Python run import nltk, then nltk.download()). Brown
Corpus, SentiWordNet, WordNet, as well as the following Models: Treebank Part of Speech Tagger (HMM),
Treebank Part of Speech Tagger (Maximum Entropy), Punkt Tokenizer Models are recommended. Finally,
I installed gensim.


Just run this files in order:
1. yelp/yelp-reviews.py - gets the reviews from the json file and imports them to MongoDB in a collection 
	called Reviews

2. reviews.py/ reviews_parallel.py - loops through all the reviews in the initial dataset and for each 
	review it: splits the review into sentences, removes stopwords, extracts parts-of-speech tags for all 
	the remaining tokens, stores each review, i.e. reviewId, business name, review text and (word,pos tag) 
	pairs vector to a new MongoDB database called Tags, in a collection called Reviews. If you have many 
	reviews, try running reviews_parallel.py, which uses the Python multiprocessing features to parallelize 
	this task and use multiple processed to do the POS tagging. It took me 14 hours to run on my local MAC 
    2.3 GHz Intel Core i7 8GB 1600 MHz DDR3 laptop.

3. corpus.py - loops through all the reviews from the new MongoDB collection in the previous step, filters 
	out all words which are not nouns, uses WordNetLemmatizer to lookup the lemma of each noun, stores 
	each review together with nouns’ lemmas to a new MongoDB collection called Corpus.

4. train.py - feeds the reviews corpus created in the previous step to the gensim LDA model, keeping only 
	the 10000 most frequent tokens and using 50 topics.

5. display.py - loads the saved LDA model from the previous step and displays the extracted topics.

6. predict.py - given a test review set, it predicts wether each sentence in the review is a tip.

7. stopwords.txt - stopwords list created by Gerard Salton and Chris Buckley for the experimental SMART 
	information retrieval system at Cornell University

