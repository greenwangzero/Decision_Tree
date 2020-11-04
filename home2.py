x = [4,4,2]  #坐标
y = [4,5,3]
z = [1,1,-1]  #真值
w = [0,0,0]
b=0   #b
n=1 #学习率
t=0
G = []
for i in range(3):
    temp = []
    for j in range(3):
        temp.append(x[i]*x[j]+y[i]*y[j])
    G.append(temp)
print(G)

def work(index):
    sum = 0
    for i in range(3):
        sum = sum + G[i][index]*z[i]*w[i]
    return sum

def cal():
    flag = False
    global w,b,n,z,t
    global x,y
    for i in range(3):
        if z[i]*(work(i)+b) <= 0:
            w[i] = w[i] + n
            b = b + z[i]*n
            flag = True
            print("迭代次数:",t,"|误分类点：x%d"%(i+1),"|w=(%d %d %d)" %(w[0],w[1],w[2]),"|b=", b)
            t = t+1
    return flag

while cal():
    cal()

print("res:wx=", w[0])
print("res:wy=", w[1])
print("res:wz=", w[2])
print("res:b=", b)