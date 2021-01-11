# This is a code that beautify case of oracle sql file
'''
    VERSION 1.0 : First version, run the code directly, and execute the convert
'''
import re

def getKeyword(url_key):
    '''
    :param url_key: the path of keyword file
    :return: dict
    '''
    try:
        fKey = open(url_key, encoding='UTF-8')
    except:
        print('keyword file no exists')
    dict_key = dict()
    for i in fKey:
        dict_key[i.strip()] = None
    return dict_key

url_src = r'C:\Users\514\Desktop\Jerry\Work\pys\src_file\handle_history.sql'      # source file path
url_dest = r'C:\Users\514\Desktop\Jerry\Work\pys\desc_file\handle_history.sql'    # destination file path
url_key = r'C:\Users\514\Desktop\Jerry\Work\pys\src_file\keyword.txt'             # keyword file path

try:
    f1 = open(url_src,encoding='UTF-8')
except:
    print('source file no exists')
try:
    f2 = open(url_dest,'w',encoding='UTF-8')
except:
    print('destination file no exists')
dict_key = getKeyword(url_key)
line1 = f1.readlines()
f1.close()
for i in line1:
    spt1 = i.split(' ')
    #print(spt1)
    for j in spt1:
        spt2 = [t.strip() for t in re.findall(r"[\w']+|[().,!?;*-|/、，：]", j)]
        print(spt2)
        for k in spt2:
            if k.upper() in dict_key:
                f2.write(k.upper())
            else:
                if '\'' in k:
                    f2.write(k)
                else:
                    f2.write(k.lower())
        # 判断j是否为当前行最后一个，是就跳过
        if j != spt1[-1]:
            f2.write(' ')
    f2.write('\n')
f2.close()