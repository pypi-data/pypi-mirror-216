#!/usr/bin/env python3
#coding:utf-8
# update:  2023/6/14
'''
通用基础库 版本: v0.1

'''

__author__ = 'xmxoxo'

import argparse
import sys
import os
import re
import json
import hashlib
import random
import time
import string
import pandas as pd
import numpy as np
import traceback
import logging

#from CharsetFilter import *

pl = lambda x='', y='-': print(y*40) if x=='' else print(str(x)) if x[-3:]=='...' or y=='' else print(str(x).center(40, y))
pr = lambda x: print('%s:%s' % (x, eval(x)))
pt = lambda x, y=60: (print('\r%s'% (' '*y), end=''), print('\r%s'%x, end=''))


def rand_filename(path='', pre='', ext=''):
    '''按时间戳生成文件名'''

    import random
    nowtime = time.time()
    fmttxt = time.strftime('%Y%m%d%H%M%S', time.localtime(nowtime))
    # dt = int((nowtime - int(nowtime))*1000)
    dt = random.randint(100, 999)
    filename = '%s%s%03d%s' % (pre, fmttxt, dt, ext)
    fname = os.path.join(path, filename)
    return fname

def mkfold(new_dir):
    '''创建目录，支持多级子目录
    '''

    if not os.path.exists(new_dir):
        os.makedirs(new_dir, exist_ok=True)

def readtxtfile(fname, encoding='utf-8'):
    ''' 读取文本文件, 自动识别编码 '''
    
    try:
        with open(fname, 'r', encoding=encoding) as f:  
            data = f.read()
        return data
    except UnicodeDecodeError  as e:
        with open(fname,'r',encoding='gb2312') as f:
            data = f.read()
        return data
    except Exception as e:
        return ''

def readtxt(fname, encoding='utf-8'):
    ''' 读入文件   '''
    
    try:
        with open(fname, 'r', encoding=encoding) as f:  
            data = f.read()
        return data
    except Exception as e:
        return ''

def savetofile(txt, filename, encoding='utf-8', method='w'):
    '''保存文本信息到文件'''

    try:
        with open(filename, method, encoding=encoding) as f:  
            f.write(str(txt))
        return 1
    except Exception as e:
        print(e)
        return 0

def readbin(fname):
    '''读取二进制文件'''

    try:# 保存文本信息到文件
        with open(fname, "rb") as f:
            byte_data = f.read()
        return byte_data
    except Exception as e:
        return b''

def savetobin(dat,filename, method='wb'):
    '''按二进制保存文件
    '''

    try:
        with open(filename, method) as f:  
            f.write(dat)
        return 1
    except Exception as e:
        return 0

def templace_replace(template:str, fields:dict):
    ''' 按模板替换
    template: 模板，形如:"这是一个$count模板"
    fields: 变量字典，形如{'count':2,'secret':'abc'}
    '''

    ret = template
    for field, value in fields.items():
        field = field.strip()
        key = '$%s' % field
        if type(value) == list:
            value = "','".join(map(str, value))
        else:
            value = str(value)

        ret = ret.replace(key, str(value))
    return ret

def pathsplit (fullpath):
    '''将路径拆分为目录，文件，扩展名三个部分'''
    
    try:
        (filepath,tempfilename) = os.path.split(fullpath)
        (filename,extension) = os.path.splitext(tempfilename)
        return filepath,filename,extension
    except Exception as e:
        return '', '' ,''

def replace_dict (txt, dictKey, isreg=0):
    '''按字典进行批量替换
    isreg: 是否启用正则
    '''

    for k,v in dictKey.items():
        if isreg:
            txt = re.sub(k, v, txt)
        else:
            txt = txt.replace(k,v)
    return txt    


def fmtText (txt):
    '''文本内容清洗（含HTML）
    '''

    # 删除HTML代码
    '''
    # 表格自动添加换行
    p = re.compile(r'(<((/t[rh])|br)(.*?)>)', re.S)
    txt = re.sub(p, r"\1\n", txt)
    '''

    # 删除HTML标签
    p = re.compile(r'(<(style|script)[^>]*?>[^>]+</\2>)|(<!--.+?-->)|(<[^>]+>)', re.S)
    txt = re.sub(p, r"", txt)

    # HTML实体替换
    dictKey = {
            '&quot;': '"',
            '&#034;': '"',
            '&apos;': '\'',
            '&amp;': '&',
            '&lt;':'<',
            '&gt;':'>',
            }
    txt = replace_dict(txt,dictKey)
    # 删除其它HTML实体
    txt = re.sub('(&[#\w\d]+;)',r"",txt)
    # 空格，制表符换成半角空格
    txt = re.sub('([　\t]+)',r" ",txt)  
    # 多个连续的空格换成一个空格
    txt = re.sub('([ "?\t]{2,})',r" ", txt)  
    # 删除空行
    txt = re.sub('(\n\s+)',r"\n",txt)
    # 中文之间的空格 [\u4e00-\u9fa5]
    #txt = re.sub('(\n\s+)',r"\1\2",txt)
    return txt

def cut_sent1(txt):
    '''切分句子，多种符号分割。'''

    txt = re.sub('([　\t]+)',r" ",txt)  #去掉特殊字符
    txt = re.sub('([ "?\t]{2,})',r" ",txt)  #多个连续的空格换成一个空格
    txt = re.sub('(\n\s*\n)',r"\n",txt)  # blank line

    txt = re.sub('([;；。！？\?])([^”])',r"\1\n\2",txt) # 单字符断句符，加入中英文分号
    txt = re.sub('(\.{6})([^”])',r"\1\n\2",txt) # 英文省略号
    txt = re.sub('(\…{2})([^”])',r"\1\n\2",txt) # 中文省略号
    #txt = re.sub('(”)','”\n',txt)   # 把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    txt = txt.rstrip()       # 段尾如果有多余的\n就去掉它
    nlist = txt.split("\n") 
    nnlist = [x for x in nlist if x.strip()!='']  # 过滤掉空行
    return nnlist

def delspace(txt):
    '''预处理: 去空行 空格
    '''

    txt = re.sub('([　\t]+)',r" ",txt)  #去掉特殊字符
    txt = re.sub('([ "?\t]{2,})',r" ",txt)  #多个连续的空格换成一个空格
    txt = re.sub('(\n\s*\n)',r"\n",txt)  # blank line
    #全角替换 
    #txt = txt.replace('％','%')
    #txt = txt.replace('、','')    
    return txt


def cut_sent(txt):
    ''' 切分句子，仅按句号分割。
    '''

    txt = delspace(txt)
    txt = re.sub('([。])',r"\1\n",txt) # 单字符断句符，加入中英文分号
    #txt = re.sub('(\.{6})([^”])',r"\1\n\2",txt) # 英文省略号
    #txt = re.sub('(\…{2})([^”])',r"\1\n\2",txt) # 中文省略号
    #txt = re.sub('(”)','”\n',txt)   # 把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    txt = txt.rstrip()       # 段尾如果有多余的\n就去掉它
    #txt = re.sub('(\n"|"\n)',r"\n",txt)  #行开头与行结尾的引号去掉
    #txt = re.sub('(["])',r'""',txt)    #剩下的引号换成2个
    #nlist = txt.split("\n") 
    nlist = txt.splitlines()
    nlist = [x for x in nlist if x.strip()!='']  # 过滤掉空行
    return nlist

def cut_segment_text(text, ret_length=512, segment=4):
    '''从长文本中分段截取并合返回指定长度的文本；
    '''

    # 计算文本总长
    total = len(text)
    # 实际长度小于返回长度时 直接返回
    if total < ret_length:
        return text
    
    # 实际长度小于返回长度2倍，直接从前面截断
    if total < ret_length * 2:
        ret = text[:ret_length]
        return ret 
    
    seg_len = ret_length // segment
    segs = (total - seg_len) // (segment -1)
    # 计算位置
    pos = list(range(0, total, segs))
    # 分段截取
    cut_txt = []
    for i in pos:
        cut_txt.append(text[i: i+seg_len])
    
    # 组合
    ret = ';'.join(cut_txt)
    return ret


def getFiles (workpath, fileExt=[]):
    ''' 单目录遍历，返回所有子目录和文件
    get all files and floders in a path
    fileExt: ['.png','.jpg','.jpeg']
    return: 
       return a list , include floders and files , like [['./aa'],['./aa/abc.txt']]
    '''

    try:
        lstFiles = []
        lstFloders = []

        if os.path.isdir(workpath):
            for dirname in os.listdir(workpath):
                file_path = os.path.join(workpath, dirname)
                if os.path.isfile(file_path):
                    if fileExt:
                        ext = os.path.splitext(dirname)[1]
                        if ext in fileExt:
                           lstFiles.append (file_path)
                    else:
                        lstFiles.append (file_path)
                if os.path.isdir(file_path):
                    lstFloders.append (file_path)
                    #a, b = getFiles(file_path, fileExt)

        elif os.path.isfile(workpath):
            lstFiles.append(workpath)
        else:
            return None
        
        lstRet = [lstFloders, lstFiles]
        return lstRet
    except Exception as e :
        return None

def getAllFiles_Generator (workpath, fileExt=[]):
    '''返回目录下的所有文件，包括子目录
    get all files in a folder, include subfolders
    fileExt: ['png','jpg','jpeg']
    return: 
       return a Generator ,include all files , like ['./a/abc.txt','./b/bb.txt']
    '''
    fileExt = [x.lower() for x in fileExt]
    try:
        if os.path.isdir(workpath):
            #if workpath[-1]!='/': workpath+='/'
            for dirname in os.listdir(workpath):
                file_path = os.path.join(workpath, dirname)
                if os.path.isfile( file_path ):
                    if fileExt:
                        ext = os.path.splitext(dirname)[1][1:].lower()
                        if ext in fileExt:
                           yield file_path
                    else:
                        yield file_path
                if os.path.isdir(file_path):
                    yield from getAllFiles_Generator(file_path, fileExt)
    except Exception as e :
        print(e)
        pass

# -----------------------------------------
class TimeCount():
    '''简单计时器 '''

    def __init__(self):
        self.clean()

    def begin(self):
        ''' 开始计时
        '''

        self.ntime = time.time()
                
    def pause(self):
        ''' 记录当前计时，返回开始到当前的时间: 毫秒
        '''
        n = (time.time() - self.ntime)*1000
        self.time_list.append(n)
        return n

    def tcount(self):
        ''' 返回计时器所有清单
        '''

        return self.time_list
    
    def show(self):
        ''' 计时并显示时间
        '''

        et = self.pause()
        txt = '用时:%f (毫秒)'% et
        print(txt)
        return txt
        
    def clean(self):
        ''' 重置计时器
        '''

        self.ntime = 0
        self.time_list = []

    def stop(self):
        ''' 停止计时器
        '''

        self.clean()

# -----------------------------------------
def api_post_data (url, data, timeout=10, data_format='json'):
    ''' 向URL发送数据并返回json格式化结果
    '''

    import requests
    import json
    try:
        if data_format=='form':
            res = requests.post(url, data=data, timeout=timeout)
        if data_format=='json':
            res = requests.post(url, json=data, timeout=timeout)
        res.encoding = 'utf-8'
        res = json.loads(res.text)
        return res
    except Exception as e:
        print(e)
        return None

# -----------------------------------------

def pre_format (path):
    '''对目录下的文件遍历，处理文本内容清洗（含HTML格式去除）
    '''


    intTotalLines = 0
    lstF = getFiles(path)

    for fname in lstF[1] :
        print('Processing file:%s' % (fname))
        txt = readtxtfile(fname)
        txt = fmtText(txt)
        savetofile(txt, fname)  
    print('Total: %d File(s)' % (len(lstF[1]) ) )

def pre_clean (path):
    '''批量处理目录下文件，对文本字符清洗 '''

    intTotalLines = 0
    lstF = getFiles(path)

    for fname in lstF[1] :
        print('Processing file:%s' % (fname))
        txt = readtxtfile(fname)
        txt = txtfilter(txt)
        savetofile(txt, fname)  
    print('Total: %d File(s)' % (len(lstF[1]) ) )


def brename (path, intBegin=1):
    '''
    文件批量重命名，对目录下(不含子目录)的所有文件按序号开始命名；
    序号会根据文件的数量自动在前面补0，例如有1000个文件，则第一个文件名为：0001.txt
    执行过程中将输出重命名信息，例如：
       [./dat/akdjf.txt] =rename=> [./dat/0023.txt]
    参数：
       path        目录。不会处理子目录；
       intBegin    开始序号。默认=1，即从1开始命名。
    返回
       无返回值
    '''

    # 命名的开始序号, intBegin = 1
    lstF = getFiles(path)
    lstRen = []
    intFNWidth = len(str(len(lstF[1])))
    for f in lstF[1] :
        #扩展名
        if f.rfind('.')>=0:
            strExt = f[f.rindex ('.'):]
        else:
            strExt = ''

        #生成新的文件名
        # 2019/1/16 按最大长度在前面补0，这样文件名排序看起来方便；例如：0023
        nfname = os.path.join(path , str(intBegin).zfill(intFNWidth)) + strExt
        print('[%s] =rename=> [%s]' %(f,nfname))
        intBegin += 1

        # 判断是否目标与源文件同名, 例如 1.txt==>1.txt
        if f == nfname:
            continue

        # 判断是否在重复列表中
        if f in lstRen :
            f = f + '.ren'
        
        # To do 判断是否会重名，也就是判断是否已经存在目标文件，存在则重命名
        if os.path.exists(nfname):
            #添加到重名列表中,然后改名
            lstRen.append(nfname)
            os.rename(nfname, nfname + '.ren' )

        os.rename(f, nfname)

        # 调试用
        if intBegin>10:
            pass
            #break


# 判断是否为空文件 空文件是替换了空格，制表符
def blankfile (fname):
    pass
    txt = readtxtfile(fname)
    txt = delspace(txt)
    txt = txt.replace('\n','')
    txt = txt.replace('\r','')
    if txt == "":
        return fname
    else:
        return ''

# 删除目录下的空文件 
def delblankfile (path, isDel = False):
    lstF = getFiles(path)
    for f in lstF[1] :
        print('\rfile:%s' % f,end = '')
        #print('file:%s' % f)
        if blankfile(f):
            print('\rblank file: %s' % f)
            if isDel:
                os.remove(f)
            else:
                os.rename(f, f+'.del')
    print('\r'+' '*60)


# 计算文本的MD5值
def txtmd5 (txt):
    strMD5 = hashlib.md5(txt.encode(encoding='UTF-8')).hexdigest()
    return strMD5


def SameFile (dicHash, strFileName, strBody):
    '''
    判断内容相同的文件，使用MD5进行计算
    参数：
        dicHash        哈希表，用来存放文件名与哈希值对应关系；
        strFileName    文件名，用来标识文件，也可用完整路径；
        strBody        文件内容
    返回：
        None 则表示没有重复，并且会更新哈希表
        重复时返回重复的文件名  
    '''
    
    strMD5 = txtmd5(strBody)
    if strMD5 in dicHash.keys():
        #冲突表示重复了
        return dicHash[strMD5]
    else:
        dicHash[strMD5] = strFileName
        return None


def FindSameFile (path, isDel = False):
    '''
    检查目录下文件内容是否相同,使用MD5值来判断文件的相同。
    相同的文件可以直接删除或者改名为"原文件名.same",
    同时输出提示信息,例如：
        File [./dat/1.txt] =same=> [./dat/92.txt] 
    参数:
       path    要检查的目录；只检查该目录不包含子目录；
       isDel   是否要删除，默认为否。 为“是”时直接删除文件，为“否”时将文件改名
    返回：
       无

    '''

    dicHash = {}
    lstF = getFiles(path)
    for fname in lstF[1] :
        print('\rcheck file:%s' % fname,end = '')
        txt = readtxtfile(fname)
        strSame = SameFile(dicHash,fname,txt)
        if strSame:
            print('\rFile [%s] =same=> [%s] ' % (fname,strSame))
            if isDel:
                os.remove(fname)
            else:
                os.rename(fname, fname + '.same')
            #break
    print('\r'+' '*60)


# 根据系统返回换行符
def sysCRLF ():
    if os.name == 'nt':
        strCRLF = '\n'
    else:
        strCRLF = '\r\n'
    return strCRLF

def get_randstr (strlen=10):
    '''
    生成随机的字符串，可用于文件名等
    参数：
        strlen  字符串长度，默认为10
    返回： 
        成功返回 生成的字符串
        失败返回 None
    '''

    try:
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, random.randint(strlen, strlen)))
        return ran_str
    except Exception as e :
        logging.error('Error in get_randstr: '+ traceback.format_exc())
        return None


def autoFileName (pre='', ext=''):
    '''根据时间自动生成文件名， pre为前缀，ext为后缀
    '''
    
    s = list(range(48,58)) + list(range(65,91)) + list(range(97,123))
    tmp = ''.join(map(chr, random.sample(s, 5)))
    filename = '%s%s%s' % (pre, time.strftime('%Y%m%d%H%M%S',time.localtime()) + tmp, ext)
    return filename

def pre_process (path,addFirstLine = 0):
    '''
    文本预处理，删除文件中的空格，空行，并按句子分行，然后在每句前面加上标签0；
    '''

    i = 0 
    lstF = getFiles(path)
    for fname in lstF[1] :
        #print('\rProcessing file:%s' % fname,end = '')
        print('Processing file:%s' % fname)
        txt = readtxtfile(fname)
        #按句子拆分
        lstLine = cut_sent(txt)

        if addFirstLine:
            #2019/1/17 加上分类列
            #lstLine = [ '0\t'+x for x in lstLine ]
            #2019/1/22改为调用函数实现
            lstLine = pre_addcolumn(lstLine)

        # 2019/1/17 发现一个坑,linux下和windows下的"\n"竟然不一样,只好用os.name来判断，
        strCRLF = sysCRLF()
        txt = strCRLF.join(lstLine)
        
        #保存到文件
        if addFirstLine:
            txt = "label\ttxt\n" + txt

        savetofile(txt, fname )  
        i += 1
        #if i>9:
        #    pass
            #break
    #print('\r'+' '*60)
    print('Total files: %d' % i)

def pre_NER (txt):
    '''
    NER标注处理，一个字一行
    '''

    lstL = list(txt)
    strRet = sysCRLF().join(lstL)
    return strRet

def pre_addcolumn (lsttxt,lineBegin = 1):
    '''
    每行加上空列，参数可指定空列在行首还是行尾,默认为行首
    参数： lsttxt 每行的list
    '''
    pass
    if lineBegin:
        lstLine = [ '0\t'+x for x in lsttxt ]
    else:
        lstLine = [ x+'\t0' for x in lsttxt ]
    return lstLine

def pre_allzero (lsttxt,lineNo = 1):
    '''
    判断数据文件第N列是否全为0 ，默认N=1
    '''
    
    ret = True
    for line in lsttxt:
        lstW = line.split('\t')
        if lstW[lineNo-1] != 0:
            ret = False
            break
    return ret

def pd_datCheck (lstFile, drop_dup=0, header=None):
    '''
    使用pandas对样本数据文件进行检查；
    drop_dup=1删除重复数据
    '''
    try:
        print("正在检查数据文件: %s \n" % lstFile)
        print(header)
        df = pd.read_csv(lstFile, delimiter="\t", header=header)
        print("数据基本情况".center(30,'-'))
        print(df.index)
        print(df.columns)
        #print(df.head())
        print('正在检查重复数据：...')
        dfrep = df[df.duplicated()]
        print('重复数据行数:%d ' % len(dfrep))
        if len(dfrep)>0:
            print(dfrep)
        if drop_dup and len(dfrep) :
            print('正在删除重复数据：...')
            df = df.drop_duplicates()
            df.to_csv(lstFile, index=0, sep='\t')
        print('-'*30)
        print("数据分布情况".center(30,'-'))
        dfc = df[df.columns[0]].value_counts()
        print('数值分类个数：%d' % len(dfc))
        print('-'*30)
        print(dfc)
        print('\n')
        print("空值情况".center(30,'-'))
        dfn = df[df.isnull().values==True]
        print('空值记录条数: %d ' % len(dfn))
        if len(dfn)>0:
            print('空记录'.center(30,'-'))
            print(dfn.head())
        print('\n')
        return 0
    except Exception as e :
        print("Error in pd_dat:")
        print(e)
        return -1    


def pd_datSample (lstFile):
    '''使用pandas 对数据进行打乱'''

    try:
        print("正在随机化数据: %s" % lstFile)
        df = pd.read_csv(lstFile, delimiter="\t", header=None)
        df = df.sample(frac=1)
        #df.sample(frac=1).reset_index(drop=True)
        df.to_csv(lstFile, index=0, sep = '\t', header=None)
        return 0
    except Exception as e :
        print("Error in pd_datSample:")
        print(e)
        return -1    

def pre_labelcount (lsttxt, columnindex=0, labelvalue='0'):
    '''
    统计文本中某类标签情况
    '''

    intLabel = 0
    for line in lsttxt:
        lstW = line.split('\t')
        if lstW[columnindex] == str(labelvalue):
            intLabel += 1
    return intLabel

def str2List (strText,sp = ',' ):
    '''
    # 字符串转化为整数型List,用于参数传递
    # 默认拆分符号为英文逗号","
    '''
    try:
        ret = strText.split(sp)
        ret = [int(x) for x in ret]
        return ret
    except Exception as e :
        print("Error in str2List:")
        print(e)
        return None    
def splitset(datfile, lstScale =[7,2,1]):
    '''
    将指定的数据文件（文本文件）按指定的比例拆分成三个数据集(train,dev,test)
    默认比例为 train:dev:test = 6:2:2 
    自动将文件保存到当前目录下；
    参数：
    返回：无
    '''
    pass
    if len(lstScale)!=3:
        return -1
    txt = readtxtfile(datfile)
    lstLines = txt.splitlines()
    intLines = len(lstLines)-1
    #取出第一行
    strFirstLine = lstLines[0]
    #切分数据集
    lstS = [sum(lstScale[:x])/sum(lstScale) for x in range(1,len(lstScale)+1)]                        
    lstPos = [0] + [int(x*intLines) for x in lstS] #
    lstFile = ['train','dev','test']
    for i in range (len(lstFile)):
        lstDat = lstLines[lstPos[i]+1:lstPos[i+1]+1]
        if lstDat:
            fName = './%s.tsv' % lstFile[i]
            savetofile(strFirstLine + '\n' + '\n'.join(lstDat),fName)
            print('%d  Lines data save to: %s' % (len(lstDat), fName) )

def LabelCount (path,renfile = 0):
    '''
    统计目录下所有文件的label分布情况
    '''

    pass
    lstF = getFiles(path)
    intTotalLines = 0
    intLabelLines = 0

    for fname in lstF[1] :
        txt = readtxtfile(fname)
        lsttxt = txt.splitlines()
        intLines = len(lsttxt)
        intTotalLines += intLines

        # blnZero = pre_allzero(lsttxt)
        # 统计第0列有多少个"1"
        intLabel = pre_labelcount (lsttxt,0,"1")
        intLabelLines += intLabel
        # 如果renfile开关为1，并且 文件中没有标注，并且文件名不包含"-blank"
        # 那么就改名
        if renfile and not intLabel and (not '-blank' in fname):
            os.rename(fname, fname[:-4] + '-blank' + fname[-4:] )

        print('Processing file:%20s ==> %5d lines, label count: %4d (%2.2f%%) ' % (fname,intLines,intLabel , intLabel*100/intLines ))
    print('%d File(s) ,Total: %d line(s), Laebls: %d (%2.2f%%)' % ( len(lstF[1]),intTotalLines,intLabelLines, intLabelLines*100/intTotalLines ) )

def DatCheck (header=None):
    '''标注数据检查 2019/2/22'''

    lstF = getFiles(path)
    intTotalLines = 0

    for fname in lstF[1] :
        print("Check Dat File: %s" % fname)
        pd_datCheck(fname, header=header)
    return 0

def linesCount (path):
    '''文本行数统计'''

    lstF = getFiles(path)
    intTotalLines = 0

    for fname in lstF[1] :
        txt = readtxtfile(fname)
        intLines = len(txt.splitlines())
        intTotalLines += intLines
        print('Processing file:%s ==> %d lines' % (fname,intLines))
    print('%d File(s) ,Total: %d line(s)' % ( len(lstF[1]),intTotalLines ) )

def filemerge (path, outfile):
    '''
    文件合并,将目录下的所有文件按行合并（自动处理文件开头与结尾）
    最终结果输出到参数2指定的文件中；
    '''

    if not outfile:
        return 0
    lstF = getFiles(path)
    intTotalLines = 0
    strFline = ''
    with open(outfile, 'a', encoding='utf-8') as fw:
        for fname in lstF[1] :
            txt = readtxtfile(fname)
            lstLines = txt.splitlines()
            intLines = len(lstLines)
            if intTotalLines == 0:
                strFline = lstLines[0] #记录第一个文件的首行
            else:
                # 第2个文件开始,如果首行与第一个文件相同，则删除第一行
                if lstLines[0]==strFline:
                    lstLines = lstLines[1:]
                    txt = '\n'.join(lstLines)
            if intTotalLines>1: #第2个文件开始加换行,否则开头会有一个空行
                fw.write(sysCRLF())
            fw.write(txt)
            intTotalLines += intLines
            #print('Processing file:%s ==> %d lines ' % (fname,intLines), end = '')
            print('Processing file:%s ==> %d lines ' % (fname,intLines))
    print('\n%d File(s) ,Total: %d line(s)' % (len(lstF[1]),intTotalLines ) )
    print('merge files to %s' % outfile)


def batch_doc2txt (path, outpath=''):
    ''' 目录(含子目录)下所有文件批量word转txt
    参数： path:目录；
    '''
    from win32com import client as wc
    try:
        #lstFile = getFiles(path)
        lstFile = getAllFiles_Generator(path)#, ['doc','docx']
        
        strExt = ''
        txtfile = ''
        # 生成目录 txt 用于保存转换后的文件
        if outpath == '':
            new_dir = os.path.join(path, './txt') #'/txt'
        else:
            new_dir = outpath

        if not os.path.exists(new_dir):
            os.mkdir(new_dir)

        wordapp = wc.Dispatch('Word.Application')
        #for ft in lstFile[1]:
        for ft in lstFile:
            #扩展名
            f = os.path.abspath(ft)
            strExt = ''
            if f.rfind('.')>=0:
                strExt = f[f.rindex ('.'):].lower()
                
            if strExt in ['.doc','.docx']:
                print('正在转换: %s' % ft)
                txtfile = ft[:ft.rindex ('.')]+'.txt'
                txtfile = os.path.abspath(os.path.join(new_dir, txtfile))
                #判断是否已转换
                if not os.path.isfile(txtfile):
                    try:
                        #打开文件 
                        doc = wordapp.Documents.Open(f)
                        #为了让python可以在后续操作中r方式读取txt和不产生乱码，参数为4
                        doc.SaveAs(txtfile, 4)
                        doc.Close()
                        print('转换成功：%s' % ( txtfile) )
                    except :
                        print('文件转换失败')
                    finally:
                        pass
                else:
                    print('%s 已存在，跳过。' % txtfile )

    finally:
        wordapp.Quit()


def getFieldFromJson (obj, columns, mainname='items', subname=''):
    ''' 从json格式中读取字段'''

    #total = obj['result']['total']
    
    result = []
    if mainname:
        lstobj = obj['result'][mainname]
        for x in lstobj:
            dt = []
            for col in columns:
                if subname:
                    if col in x[subname].keys(): 
                        dt.append(x[subname][col])
                    else:
                        dt.append("")
                else:
                    if col in x.keys(): 
                        dt.append(x[col])
                    else:
                        dt.append("")
            result.append(dt)
    else:
        #只有一级的情况
        lstobj = obj['result']
        dt = []
        for col in columns:
            if subname:
                if col in lstobj[subname].keys(): 
                    dt.append(lstobj[subname][col])
                else:
                    dt.append("")
            else:
                if col in lstobj.keys(): 
                    dt.append(lstobj[col])
                else:
                    dt.append("")
        result.append(dt)
    return result


if __name__ == '__main__':
    pass    

