import os
import sys
import xmltodict
from fractions import Fraction

def extractData(fan_property):
    nums = set(["FAN_AMBIENT_DIM","LINEALITY_DIM","N_RAYS"])
    if fan_property['@name'] in nums:
        return fan_property['@value']+""
    elif fan_property['@name'] == "RAYS":
        return "\n".join(fan_property['m']['v'])
    elif fan_property['@name'] == "LINEALITY_SPACE":
        if fan_property['m'] == None:
            return ""
        else:
            temp=[]
            temp.append(fan_property['m']['v'])
            return "\n".join(temp)
    elif fan_property['@name'] == "MAXIMAL_CONES":
        return "{"+"}\n{".join(fan_property['m']['v'])+"}"
    else:
        print "probably unicode set checking error"
        return ""

def gcd(a,b):
    if a == 0: return b
    if b == 0: return a
    return gcd(b, a % b)

def intRays(fanfile,outfile):
    fan = open(fanfile,"r")
    int_fan = open(".normalfan/"+outfile+".normalfan","w")
    line = fan.readline()
    while line != "RAYS\n":
        int_fan.write(line)
        line = fan.readline()
    int_fan.write(line)
    line = fan.readline()
    while line != "\n":
        values = map(Fraction,line.strip().split(" "))
        lcm = reduce(lambda x,y:(x*y)/gcd(x,y),[f.denominator for f in values])
        values = [str(value*lcm) for value in values]
        int_fan.write(reduce(lambda x,y:str(x)+" "+str(y),values)+"\n")
        line = fan.readline()
    int_fan.write(line)
    
    rest = fan.read()
    int_fan.write(rest)
    int_fan.flush()
    int_fan.close()
    
#polymake script won't deal with vertex input files for some reason
fname=sys.argv[-1]
os.system("cp "+fname+" temp")
if fname[-5:]!=".poly":
    os.system("polymake temp VERTICES > /dev/null")
else:
    fname = sys.argv[-1][:-5]
os.system("polymake --script getFan temp")
os.system("rm temp")

gfanfile = open("tempfile",'w')
#header
gfanfile.write("_application fan\n_version 2.2\n_type SymmetricFan\n\n")

gfan_properties = {'FAN_AMBIENT_DIM':'AMBIENT_DIM','LINEALITY_DIM':'LINEALITY_DIM','RAYS':'RAYS','N_RAYS':'N_RAYS','LINEALITY_SPACE':'LINEALITY_SPACE','MAXIMAL_CONES':'MAXIMAL_CONES'}
ordered = ['FAN_AMBIENT_DIM','LINEALITY_DIM','RAYS','N_RAYS','LINEALITY_SPACE','MAXIMAL_CONES']
properties={}

#need to convert normal fan from polymake to gfan format
fanxml = xmltodict.parse(open("temp.fan").read())
fanxml = fanxml['object']['property']
for prop in fanxml:
    if prop['@name'] in gfan_properties:
        properties[prop['@name']]=extractData(prop)

for attribute in ordered:
    gfanfile.write(gfan_properties[attribute]+"\n")
    gfanfile.write(properties[attribute]+"\n\n")
gfanfile.flush()
gfanfile.close()

os.system("rm temp.fan")
intRays("tempfile",fname)
os.system("rm tempfile")
os.system("gfan _chowbetti -i .normalfan/"+fname+".normalfan")
