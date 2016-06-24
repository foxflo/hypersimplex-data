import os
def parse():
    for i in xrange(3,9):
        f = open("chowbetti_sqpy_"+str(i)+".polynomial",'w')
        vertices = open("sqpy"+str(i),'r').read().strip().split('\n')
        temp = [x.split(" ")[1::] for x in vertices]
        temp1 = [[str(int(y)+2) for y in x] for x in temp]
        temp2 = [[chr(97+j)+x[j] for j in xrange(len(x))] for x in temp1]
        temp3 = [reduce(lambda x,y:x+y,z) for z in temp2]
        temp4 = reduce(lambda x,y:x+"+"+y, temp3)
        ring = "Q["+reduce(lambda x,y:x+","+y,[chr(97+j) for j in xrange(len(temp1[0]))])+"]\n"
        f.write(ring)
        f.write("{"+temp4+"}")
        
def chowbetti():
    for i in xrange(3,9):
        os.system("gfan_tropicalintersection < chowbetti_sqpy_"+str(i)+".polynomial > chowbetti_sqpy_"+str(i)+".normalfan")
        os.system("gfan_chowbetti -i chowbetti_sqpy_"+str(i)+".normalfan >>data")

chowbetti()
