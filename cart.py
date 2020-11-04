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
def calGini(confidition,feature):
    gini_name= {}
    gini_num= {}

    data = select_table(confidition)
    cases = len(data)
    num_good = float(data.count(('是',)))

    for idx in feature:
        labels = []
        if idx == "编号" or idx == "好瓜":
            continue
        for label in select_table(confidition, label=idx, distict=True):
            if len(label) == 1:
                labels.append(label[0])
        minGini = 999
        minName=""
        for label in labels:
            temp = 999
            now_confidition = confidition
            not_confidition = confidition
            if not now_confidition:
                now_confidition = " where "
                not_confidition = " where "
            else:
                now_confidition = now_confidition + " and "
                not_confidition = not_confidition + " and "
            now_confidition = now_confidition + " " + idx + " = '" +label+"'"
            not_confidition = not_confidition + " " + idx + " != '" +label+"'"
            feature_data = select_table(condition=now_confidition)
            other_feature_data = select_table(condition=not_confidition)
            #print("condition",now_confidition)
            k_ = float(len(feature_data))/cases
            label_good = float(feature_data.count(('是',)))
            other_label_good = float(other_feature_data.count(('是',)))
            other_ = float(other_label_good)/len(other_feature_data)
            m_ = float(label_good)/len(feature_data) # 好瓜率
            temp = k_*(2*m_*(1-m_))+(1-k_)*(2*other_*(1-other_))
            if temp<minGini:
                minGini = temp
                minName = label
        gini_name[idx]=  minName
        gini_num[idx]=  minGini
    return gini_num,gini_name


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
def buildGiniTree(confidition,root,label,feature):
    # 移除 root from 特征集
    global cnt
    feature.remove(root)
    # get labels
    labels = ['True','False']

    now_confidition = confidition
    not_confidition = confidition
    if not now_confidition:
        now_confidition =  " where "
        not_confidition =  " where "
    else:
        now_confidition = now_confidition + " and "
        not_confidition = not_confidition + " and "
    now_confidition = now_confidition + " " + root + " = '" +label+"'"
    not_confidition = not_confidition + " " + root + " != '" +label+"'"
    # 如果属于同一类返回
    flag, nflag = checkSameLable(now_confidition)
    not_flag, not_nflag = checkSameLable(not_confidition)
    if flag:
        nflag = "LeafNode:"+str(cnt)+" "+nflag
        G.add_node(nflag,fontname="SimHei")
        G.add_edge(root+label, nflag, label="是",fontname="SimHei",color="black", style="dashed", penwidth=1.5)
        cnt = cnt + 1
        if not not_flag:
            return
    else:
        # 计算gini
        gini_num,gini_name = calGini(now_confidition, feature)
        # 选gini最小的特征作为节点
        minidx = min(gini_num, key=gini_num.get)
        G.add_node(minidx + gini_name[minidx], fontname="SimHei")
        G.add_edge(root+label, minidx + gini_name[minidx], label="否", fontname="SimHei", color="black", style="dashed", penwidth=1.5)

        buildGiniTree(now_confidition,minidx,gini_name[minidx],feature)
    if not_flag:
        nflag = "LeafNode:" + str(cnt) + " " + nflag
        G.add_node(nflag, fontname="SimHei")
        G.add_edge(root+label, nflag, label="否", fontname="SimHei", color="black", style="dashed", penwidth=1.5)
        cnt = cnt + 1
        return
    else:
        # 计算gini
        gini_num, gini_name = calGini(now_confidition, feature)
        # 选gini最小的特征作为节点
        minidx = min(gini_num, key=gini_num.get)
        G.add_node(minidx + gini_name[minidx], fontname="SimHei")
        G.add_edge(root+label, minidx + gini_name[minidx], label="否", fontname="SimHei", color="black", style="dashed", penwidth=1.5)

        buildGiniTree(not_confidition, minidx, gini_name[minidx], feature)

def createTreeRoot():
    # 计算gini
    gini_num, gini_name = calGini(None, index)
    # 选gini最小的特征作为节点
    minidx = min(gini_num, key=gini_num.get)
    G.add_node(minidx + gini_name[minidx], fontname="SimHei")
    return minidx,gini_name[minidx]


root ,label= createTreeRoot()
print("root=",root)
print("label=",label)
buildGiniTree(None, root, label,index.tolist())
G.layout()
G.draw("cart.png", prog="dot")
