import matplotlib.pyplot as plt
import  math
import pandas as pd
# # 绘制直方图
# plt.subplot(222)    #  分成2*2，占用第二个，即第一行第二列的子图
# df=pd.DataFrame()
# population_ages = [6.0,  5.9,  3.5,  2.9,  8.7,  7.9 , 7.1  ,5.0  ,5.2,  3.9,
# 3.7  ,6.1  ,5.8 , 4.1 , 5.8  ,6.4  ,3.8 , 4.9  ,5.7  ,5.5,
# 6.9 , 4.0 , 4.8  ,5.1 , 4.3 , 5.4,  6.8 , 5.9 , 6.9  ,5.4,
# 2.4 , 4.9  ,7.2 , 4.2 , 6.2  ,5.8,  3.8 , 6.2  ,5.7  ,6.8,
# 3.4  ,5.0 , 5.2,  5.3 , 3.0 , 3.6 , 3.8  ,5.8 , 4.9 , 3.7
# ]
#
# bins = [0,1,2,3,4,5,6,7,8,9,10]
# plt.rcParams['font.sans-serif']=['SimHei']
# plt.rcParams['axes.unicode_minus'] = False
# plt.hist(population_ages, bins, histtype='bar', label='销售额',rwidth=0.8)
# plt.legend()
# plt.title("相对频率直方图")
# plt.show()
#
# # 绘制箱须图
# df['销售额']= population_ages
# plt.boxplot(x=df.values,labels=df.columns,whis=1.5)
# plt.show()
#
# # 绘制正态概率分布图
# population_ages.sort()
# plt.style.use("ggplot")
# plt.rcParams['axes.unicode_minus'] = False
# plt.rcParams['font.sans-serif']=['SimHei']
# #新建一个空的DataFrame
# xx = []
# yy = []
# for x in range(50):
#     key = population_ages[x]
#     cnt = 0
#     for y in range(50):
#         if population_ages[y] <= key:
#             cnt = cnt + 1
#     xx.append(key)
#     yy.append(cnt/50)
# plt.plot(xx,yy,'o-')
# plt.grid(True)
# plt.title('正态概率分布图')
# plt.show()

x =[2.	,5	,6	,7	,22	,25	,28	,30	,22	,18]
y=[75.	,90	,148,	183	,242,	263	,278,	318	,256	,200]

plt.scatter(x,y)
b=float(83.117)
a = float(7.405)
y_line=[]
avg=0
for xx in x:
    avg = avg +xx
    y_line.append(a*xx+b)
plt.plot(x, y_line, color='r')
avg = avg/len(x)
s =0
for xx in x:
    s = s+(xx-avg)*(xx-avg)
print("s=",math.sqrt(4890.7748/8))
sss= math.sqrt(4890.7748/8)
print("sqrt(s)=",math.sqrt(s))
res = 22.115096*2.306/math.sqrt(s)
print("y=",math.sqrt(1.1+(35-(avg))*((35-(avg)))/s)*2.306*sss)
yyy=math.sqrt(1.1+(35-(avg))*((35-(avg)))/s)*2.306*sss
print("yyy=",yyy)
print("x1=",a*35+b-yyy,"x2=",a*35+b+yyy)
#plt.show()
sum = 0
for i in range(len(x)):
    print(y[i])
    print(y_line[i])
    sum = sum + (y[i]-y_line[i])*(y[i]-y_line[i])
print(math.sqrt(sum/len(x)))