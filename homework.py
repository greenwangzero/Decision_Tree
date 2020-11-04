x = [4,4,2]  #坐标
y = [4,5,3]
z = [1,1,-1]  #真值
wx=0  #w
wy=0  #w
b=0   #b
n=1 #学习率
t=0

def cal():
    flag = False
    global wx,wy,b,n,z,t
    global x,y
    for i in range(3):
        if z[i]*(wx*x[i]+wy*y[i]+b) <= 0:
            wx = wx + z[i]*x[i]*n
            wy = wy + z[i]*y[i]*n
            b = b + z[i]*n
            flag = True
            print("迭代次数:",t,"|误分类点：x%d"%(i+1),"|w=(%d %d)" %(wx,wy),"|b=", b,"|w*x+b=%dx+%dx+%d" %(wx,wy,b))
            t = t+1
    return flag

while cal():
    cal()

print("res:wx=", wx)
print("res:wy=", wy)
print("res:b=", b)