# -*- coding:utf-8 –*-
import ngram
import re

string_length=10
class line_info:
    def __init__(self):
        self.attribute = 0     # 行属性，初始值为0，若为KEY则置1，若为VALUE则置2
        self.category = 0     # 行类别，初始值为0，1-6值
        self.length = 0      # 行长度
        self.content = ''    # 行内容
a = line_info() # 定义结构对象

def strdecode(sentence):
    if not isinstance(sentence, unicode):
        try:
            sentence = sentence.decode('utf-8')
        except UnicodeDecodeError:
            sentence = sentence.decode('gbk', 'ignore')
    return sentence

def get_line(text):
    line=[]
    a=line_info()
    j=0
    tag=0
    for i in range(0,len(text)):
        if text[i]=='\n':
            a.length = j
            if j > 0:
                line.append(a)
            a = line_info()
            j = 0
            if i==len(text):
                tag=1
            continue
        j+=1
        a.content+=text[i]
    if tag==0:
        line.append(a)
    return line

def extract_tag(line):
    line_t=line
    a=0
    b=0
    for i in range(0,len(line_t)):
        if re.search('\d#',line_t[i].content):
            tag=re.search('\d#',line_t[i].content)
            a=tag.group(0)[0]
            line_t[i].attribute=a
            b=tag.group(0)[2]
            line_t[i].category=b
            line_t[i].content=re.sub('\d,\d###','',line_t[i].content)
        else:
            line_t[i].attribute=a
            line_t[i].category=b
    return line_t

def search_key(line_info,n):
    list=[]
    for i in range(0,len(line_info)):
        if line_info[i].attribute=='0':
            if line_info[i].category=='%s'%n:
                list.append(line_info[i])
    return list

def search_value(line_info,n):
    list=[]
    for i in range(0,len(line_info)):
        if line_info[i].attribute=='1':
            if line_info[i].category=='%s'%n:
                list.append(line_info[i])
    return list


def train_search_for_word(array,word):
    for i in range(len(array)):
    #    print array[i],"***",word
        if array[i]==word:
            return i
        elif array[i]==-999999:
            array[i]=word
            return i
    return -1


def classify_search_for_word(array,word):
    for i in range(len(array)):
        if array[i]==word:
            return i
    return -1


def count_not_occur(words,grams,n,t):
    c=len(grams)
    if n==1:
        for gram in grams:
            if classify_search_for_word(words,gram)<>-1:
                c-=1
    else:
        length=len(grams)
        for i in range(length):
            if i+1==length:
                break
            cur=grams[i]
            nex=grams[i+1]
            index_p=classify_search_for_word(words,cur)
            index_q=classify_search_for_word(words,nex)
            if index_p<>-1&index_q<>-1&t[index_p,index_q]>0:
                c-=1
    return c


