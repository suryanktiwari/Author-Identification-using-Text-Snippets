# README - Project 
# Project Title - Author Identification Using Text Snippets

This project is inspired by the Kaggle competition Spooky Author Identification.

Aim is to crawl author data off the web and create a corpus of it. To clean the data obtained and make a dataset of authors corresponding to iconic/unique/habitual sentence snippets from their work. Finally to train a ML model to identify authors based on these text snippets.

This project is pursued for Machine Learning Course CSE-543 at IIITD.

List of files submitted:

1. Code(folder)
	-	Dataset Generation(folder)
		*	Crawl Corpus.py
		*	Preprocess Corpus.ipynb
		*	statistics.py
	-	Author Identification.ipynb
	-	visualization.ipynb
2. Dataset(folder)
	-	train.xlsx
	-	test.xlsx
3. Baseline(folder)

The Dataset Generation folder contains all the files needed to web scrap the data from the American Literature website. It also consists of the statistics.py file through the use of we can find various statistics related to our dataset.
Author identification.ipynb consists of all the code necessary to implement the machine learning model ranging from the preprocessing to feature engineering to model application.
visualization.ipynb file contains the visualization code for TSNE plots, UMAP plots, bar plots etc.

The Dataset folder contains two file train.xlsx and test.xlsx which contains the data necessary for training and testing along with gold labels.

How to run these files:

The python files can be simply run in any editor capable of running the python files as these are in the .py format.
The ipynb files can be run on colab or jupyter notebook.

# Name - Suryank Tiwari
# Roll No - MT19019

# Name - Prateek Agarwal
# Roll No - MT19070