import re
import info_struct

def key_category(line,category_num):
    for i in range(0,category_num+1):
        f=open('Key/%d'%i,'r')
        key=f.read()
        key=info_struct.strdecode(key)
        f.close()
        if re.search(line.content,key):
            return i
    return -1