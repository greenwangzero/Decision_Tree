import matplotlib.pyplot as plt
# -*- coding: utf-8 -*-
import  math
import pandas as pd
from selectTable import select_table
import pygraphviz as pgv
file = pd.read_excel('watermelon20.xlsx')
index = file.columns.values
G = pgv.AGraph(directed=True, rankdir="TB",
               compound=True, normalize=True, encoding='UTF-8')
cnt = 0
print(index)
cases_num = float(file.shape[0])
feature_num = file.shape[1]-1
print("data_num=",cases_num,"feature=",feature_num)

hd = 0.
h_feature = {}
use_feature={}
use_feature_Leaf={}
def calEntropy(confidition,feature):
    h_feature = {}
    h_a_feature = {}
    data = select_table(confidition)
    cases = len(data)
    num_good = float(data.count(('是',)))
    num_bad = float(len(data)-num_good)
    hd = - (math.log(num_good/cases,2)*\
            num_good/cases +\
            math.log(num_bad/cases,2)*num_bad/cases)
    for idx in feature:
        labels = []
        if idx == "编号" or idx == "好瓜":
            continue
        for label in select_table(confidition, label=idx, distict=True):
            if len(label) == 1:
                labels.append(label[0])
        for label in labels:
            now_confidition = confidition
            if not now_confidition:
                now_confidition = " where "
            else:
                now_confidition = now_confidition + " and "
            now_confidition = now_confidition + " " + idx + " == '" +label+"'"
            feature_data = select_table(condition=now_confidition)
            #print("condition",now_confidition)
            k_ = float(len(feature_data))/cases
            label_good = float(feature_data.count(('是',)))
            #print("feature_data",feature_data)
            m_ = float(label_good)/len(feature_data) # 好瓜率
            # 只有好瓜，坏瓜两种情况，直接加
            hk = 0
            hf = 0
            if label_good != 0: # good
                hk = m_ *math.log(m_,2)
            if len(feature_data)-label_good != 0: # bad
                hk = hk + (1-m_) *math.log((1-m_),2)
            h_feature[idx] = h_feature.get(idx, 0) + k_ * hk
            if k_:
                h_a_feature[idx] = h_a_feature.get(idx,0) + k_* math.log(k_,2)
        h_feature[idx] = h_feature.get(idx, 0) * -1
        h_a_feature[idx]= h_a_feature.get(idx,0)* -1
        h_feature[idx] = (hd - h_feature[idx])/h_a_feature[idx]
    return h_feature


def checkSameLable(confidition):
    data = select_table(condition=confidition)
    cases = len(data)
    num_good = float(data.count(('是',)))
    if num_good == cases:
        return True,'好瓜'
    elif num_good ==0:
        return True, '坏瓜'
    else:
        return False,None


# bfs
def buildId3Tree(confidition,root,feature):
    # 移除 root from 特征集
    global  cnt
    feature.remove(root)
    # get labels
    labels = []
    for label in select_table(confidition, label=root, distict=True):
        if len(label) == 1:
            labels.append(label[0])
    for label in labels:
        now_confidition = confidition
        if not now_confidition:
            now_confidition =  " where "
        else:
            now_confidition = now_confidition + " and "
        now_confidition = now_confidition + " " + root + " = '" +label+"'"
        # 如果属于同一类返回
        flag, nflag = checkSameLable(now_confidition)
        if flag:
            nflag = "LeafNode:"+str(cnt)+" "+nflag
            G.add_node(nflag,fontname="SimHei")
            G.add_edge(root, nflag, label=label,fontname="SimHei",color="black", style="dashed", penwidth=1.5)
            cnt = cnt + 1
            continue
        # 计算增益比
        h_feature = calEntropy(now_confidition, feature)
        # 选增益比最大的特征作为节点
        maxidx = max(h_feature, key=h_feature.get)
        print("maxidx=",maxidx)
        # 以该节点为根构建子树
        G.add_node((maxidx),label=label)
        G.add_edge(root, maxidx,label=label)
        buildId3Tree(now_confidition, root, feature)

def createId3TreeRoot():
    # 遍历完所有的特征时, 返回出现次数最多的标签（叶子）
    # 计算增益比
    h_feature = calEntropy(None, index)
    # 选增益比最大的特征作为节点
    maxidx = max(h_feature, key=h_feature.get)
    G.add_node(maxidx,fontname="SimHei")
    return maxidx

def init():
    global use_feature
    for x in index:
        use_feature[x]=False
        use_feature_Leaf[x] = 0


init()
root = createId3TreeRoot()
print("root=",root)
buildId3Tree(None, root, index.tolist())
G.layout()
G.draw("c45.png", prog="dot")
