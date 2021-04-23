import os
import pandas as pd
from sklearn.model_selection import train_test_split

path = 'Author Corpus Mini Larger'
count=0
line_vocab = dict()
for folder in os.listdir(path):
    folder_path = path+'\\'+folder
    print(folder_path)
    line_vocab[folder]=[]
    count_files = 0
    length_docs = []
    length_sentence = []
    length_word = []
    for filename in os.listdir(folder_path):
        count_files += 1
        cur_path = folder_path+"\\"+filename
        file  = open(cur_path, "r", encoding='utf-8')
        text = file.read()
        file.close()
        paragraphs = text.split('.')
        count+=len(paragraphs)
        length_docs.append(len(text))
        for line in paragraphs:
            line_vocab[folder].append(line)
            length_sentence.append(len(line))
            words = line.split(" ")
            for word in words:
                length_word.append(len(word))
    
    print('\n\nDoc length statistics of Folder:',folder,'\n\n')
    print('Min length of docs:',min(length_docs))
    print('Max length of docs:',max(length_docs))
    print('Average length of docs:',sum(length_docs)/len(length_docs))
    
    print('\n\nSentence length statistics of Folder:',folder,'\n\n')
    print('Max sentence length:',max(length_sentence))
    print('Min sentence length:',min(length_sentence))
    print('Average sentence length:',sum(length_sentence)/len(length_sentence))

    print('\n\nWord length statistics of Folder:',folder,'\n\n')
    print('Max word length:',max(length_word))
    print('Min word length:',min(length_word))
    print('Average word length:',sum(length_word)/len(length_word))

    print('Number of samples:', len(line_vocab[folder]))
    print('File Count:',count_files)

print(count)

'''Avg  doc length  --done
Avg word length 
Avg sentence length --done
samples per class  --done
largest doc length per class --done
smallest doc length per class --done
number of docs by author  ---done
number of words per author'''
