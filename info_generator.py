# -*- coding:utf-8 –*-
import info_struct
import os
import codecs
import ngram
import numpy as np
import cPickle as pickle
import jieba
#定义参数
category_num=8
dict_dimension=1000

#获取训练集
s=os.getcwd()
path=s+'/Train'
list_of_documents=os.listdir(path)
print list_of_documents
#定义训练集信息代数格式并打开键值文件
t=np.zeros((category_num+1,dict_dimension,dict_dimension),dtype=int)            #token频度矩阵
#w=np.zeros((category_num+1,dict_dimension,dict_dimension),dtype=unicode)                         #token内容向量：！！！暂时使用单字作为单词，日后应当考虑使用分词结果作为单词
w =[[-999999 for x in range(1000)] for y in range(1000)]   #二维list，第二维存每个类别的word
c=np.zeros((category_num+1,1),dtype=int)                                          #类别频度
file=[]
for i in range(0,category_num+1):
    a=codecs.open('Key/%d' % i, 'w+','u8')
    file.append(a)

key_exist={}

#更新训练集构成的矩阵信息：针对每一个训练集文件
for i in range(0,len(list_of_documents)):
    #读入训练集文件并获取单行及其标签
    f=open(path+'/'+list_of_documents[i],'r')
    text=f.read()
    f.close()
    text=info_struct.strdecode(text)
    line_info=info_struct.get_line(text)
    info_struct.extract_tag(line_info)
    #存储key值对应的关键字（下标从1开始）
    for ca in range(0,category_num+1):
        temp=info_struct.search_key(line_info,ca)
     #   f=codecs.open('Key/%d' % ca, 'w+','u8')
        #往表中写key值 用hash算法判断key是否已经在表中
        for s in range(0,len(temp)):
            if key_exist.has_key(temp[s].content):
                continue
            file[ca].write('%s\n'%temp[s].content)
            key_exist[temp[s].content]=1
    #存储value值带来的词语频度变化（下标从1开始）
    for ca in range(0,category_num+1):
        temp=info_struct.search_value(line_info,ca)
        #debug
       # print ca
        for m in range(len(temp)):
            sentence=temp[m].content
            print sentence
            #切分单字
            #uni=ngram.NGram(N=1)
            #l_1=list(uni.split(sentence))
            l_1=jieba.cut(sentence)
            words_list=[]
            for words in l_1:
                words_list.append(words)
                index=info_struct.train_search_for_word(w[ca],words)
                t[ca,index,index]+=1#！！！这里对于每一个出现的单字都做增1处理
             #   print words, "下标是", index
            #切分双字
            #bi=ngram.NGram(N=2)
            #l_2=list(bi.split(sentence))
            for i in range(len(words_list)):
            #    ld=list(uni.split(words))
             #   p=ld[0]
                if(i+1==len(words_list)):
                    break
                p=words_list[i]
                q=words_list[i+1]
                index_p=info_struct.train_search_for_word(w[ca],p)
             #   print p,"下标是",index_p
             #   q=ld[1]
                index_q=info_struct.train_search_for_word(w[ca],q)
             #   print p,q
             #   print q, "下标是", index_q
                t[ca,index_p,index_q]+=1
        c[ca]+=len(temp)


#存储训练集信息
f=open('Value_Dict/train.pkl', 'w')
pickle.dump((t,w,c),f)
f.close()
for i in range(0,category_num+1):
    file[i].close()
