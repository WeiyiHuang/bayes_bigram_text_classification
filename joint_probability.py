# -*- coding:utf-8 –*-
import info_struct
import numpy as np
import cPickle as pickle
import jieba
from math import log

def calculate_joint_prob_for_specific_class(n,line):
    f=open('Value_Dict/train.pkl','r')
    t,w,c=pickle.load(f)
    f.close()

    adjust=1
   # print "<><><><><><><><>"
   # print c[n]
    if c[n]==0:
        return -999999  #该类别不存在，直接返回最小值
    cor_1=log(c[n])-log(np.sum(c))
    p=jieba.cut(line.content) #进行分词 by Raywzy
    words_list=[]
    for tmp in p:
     #   print tmp,"**"
        words_list.append(tmp)
   # index_1=info_struct.search_for_word(w[n,:],line.content[0])  #第一个单词位置
    #uni=ngram.NGram(N=1)
    #bi=ngram.NGram(N=2)
    index_1=info_struct.classify_search_for_word(w[n],words_list[0]) #查第一个词位置
    cor_2_adjust=adjust*info_struct.count_not_occur(w[n],words_list,1,t[n,:,:])
    #l_0=list(uni.split(line.content))
    #l_2=list(bi.split(line.content))
    cor_2=log(t[n,index_1,index_1]+adjust)-log(np.trace(t[n,:,:])+cor_2_adjust)
   # print line.content,index_1
    cor_3=0
    pre=words_list[0]
    cor_3_adjust=adjust*info_struct.count_not_occur(w[n],words_list,2,t[n,:,:])
    for i in range(1,len(words_list),1):
        cur=words_list[i]
        index_p=info_struct.classify_search_for_word(w[n],pre)
        index_q=info_struct.classify_search_for_word(w[n],cur)
        cor_3+=log(t[n,index_p,index_q]+adjust)-log((t[n,index_q,index_q])+cor_3_adjust)
        pre=cur
    prob=(cor_1+cor_2+cor_3)
    return prob