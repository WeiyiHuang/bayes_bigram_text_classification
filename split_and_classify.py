# -*- coding:utf-8 –*-
import info_struct
import key_verification
import joint_probability
import numpy as np
import os
import cPickle as pickle
import jieba
#定义参数
category_num=8

#获取测试集
s=os.getcwd()
path=s+'/Test'
l=os.listdir(path)

#获取训练好的数据信息
f=open('Value_Dict/train.pkl','r')
t,w,c=pickle.load(f)
f.close()

#测试集
for cv in l:
    #获取训练集文本信息并转化为行
    f=open('Test/'+cv,'r')
    document_content=f.read()
    document_content=info_struct.strdecode(document_content)
    line_info=info_struct.get_line(document_content)
    info_struct.extract_tag(line_info)
    #以行为单位进行分类操作
    for single_line in line_info:
        #验证是否为key，否则进行Bi-Gram分类（正则）
        key_veri=key_verification.key_category(single_line,category_num)
        if key_veri<>-1:
            single_line.attribute=1
            single_line.category=key_veri
            print '\n#############################################本行内容：\n'
            print single_line.content
            print '本行为Key'
        else:
            prob=np.zeros((category_num+1,1),dtype=float)
            for ca in range(0,category_num+1):
                prob[ca]=joint_probability.calculate_joint_prob_for_specific_class(ca,single_line)
         #       print "fuck"+single_line.content
            print '\n#############################################本行内容：\n'
            print single_line.content
            print '本行为Value'
            print '概率情况'
            print prob
            print '最终分类'
            print np.argmax(prob[:])
    f.close()

