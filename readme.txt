Car Review Project file description:
1. car_review.pkl is the scrapped reviews from website, in the format of dictionary
2. car_sa_review.csv is the re-constructed data file, with sentimental analysis implemented and attached as feature 'sentiment xxx'.
3. data_processing.py provides some useful tools for NLP data cleaning.
4. lda_core.py provides the core idea of LDA model in this project.
5. main.py is the file conducting analysis, web scrapping and visualization.
6. sa_core.py provides ideas for sentimental analysis.
7. stop_words.txt gives a list of stop words.
8. web_core.py implements the core idea of our scrapper.

Environment Requirement:
1. python: 3.7.6
2. IDE: PyCharm Community Edition 19.3
3. snownlp 0.12.3
4. numpy 1.18.1
5. pandas 1.0.1
6. cfscrape 2.1.1
7. gensim 3.8.3
8. textblob 0.15.3, after install textblob, run terminal code ''