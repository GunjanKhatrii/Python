#!/usr/bin/env python
# coding: utf-8

# ## Control flow in python(simple programs to understand Syntax)

# In[3]:


a=int(input("Enter any number: "))
if a>10:
    print(">10")
    print("Inside the top if")
    if a>20:
        print(">20")
        print("Inside the nested if")
    else:
        print("<20")
        print("Inside the else part of nested if")
print("Outside all ifs")


# In[6]:


a = int(input("Enter an integer between 0-100: "))
if a>0 and a<=100:
    
    if a % 2 ==0:
        print("the number is even")
    else:
        print("The number is odd")
else:
    print("The number is out of range")


# In[13]:


# Single line comment 

"""
User will enter a float number let say 238.915 . Your task is
to find out the integer portion before the point 
(in this case 238)and then check if that integer portion 
is even number or not.
"""

x=float(input("Enter a real number: "))
y=round(x)
if x>0:
    if y>x:
        intportion = y-1
    else:
        intportion = y
else:
    if y<x:
        intportion = y+1
    else:
        intportion = y
        
print(intportion)
if intportion % 2 == 0:
    print(intportion, "is even")
else:
    print("Integer portion is odd")


# # loops

# In[17]:


n=int(input("Enter the number of iterations you want: "))
i=1
while(i<n):
    if i%2 == 0:
        print(i)
    else:
        pass
    i+=1
print("done")


# Break statement asks to exit the loop immediately and brings you outside the body of the loop.
# Continue statement brings the next iteration loaded regardless of the body of the loop. 

# In[2]:


n=int(input("Enter the number of iterations you want: "))
i=1
while True:
    if i%9 == 0:
        print("Inside if")
        break
    else:
        print("Inside else")
        i = i+1
print("Done")


# In[1]:


i=1
while True:
    if i%9 !=0:
        print("Inside if")
        i +=1
        continue
    print("Here i is divisible by 9")
    break
    
print("Done ho gaya")


# In[ ]:


L=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday',
   'Sunday','Blue','Green','Yellow','Invalid','Grey']
D=[]
C=[]
i=0
word=L[i]
while True:
    if word=='Invalid':
        break
        
    if word=='Monday' or 'Tuesday' or 'Wednesday' or 'Thursday' or 'Friday' or 'Saturday' or 'Sunday':
        D.append(word)
        i+=1
        continue
    
    
    C.append(word)
    i+=1
        
print(D)
print(C)
print("Lists updated")
        


# In[1]:


L=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday',
   'Sunday','Blue','Green','Yellow','Invalid','Grey']
D=[]
C=[]
i=0
while True:
    if L[i] == "Invalid":
        break
    if i<7:
        D.append(L[i])
        i+=1
        continue
    C.append(L[i])
    i+=1
    
print(D)
print(C)
    


# In[8]:


L=[]
for i in range(0,10,2): #range(start,stop-1,jump)
    print(i)
    L.append(i**2)
print(L)


# In[2]:


''' Fibonacci series fn=f(n-1)+f(n-2)< By addition of previous 2 elements the next element is calculated'''
L=[]
n=int(input("Enter the number of enteries you want: "))
L.append(0)
L.append(1)
for i in range(2,n+1):
    L.append(L[i-1]+L[i-2])
print(L)


# In[24]:


#else in for loop
#When for completes its iterations then else part is executed
S={"apple",4.9,"cherry"}
i=1
for x in S:
    print(x)
else:
    print("Loop terminated")
print("out of the loop")


# In[25]:


''' In what case would else be not executed?-- if we use any break statement in the loop'''

S={'apple',4.9,"cherry"}
i=1
for x in S:
    print(x)
    i+=1
    if i==3:
        break
    else:
        pass
else:
    print("Loop terminated")
print("Out of loop")


# In[4]:


#for loop is very helpfull to iterate over a dictionary
D={"apple":44,"cherry":"game"}
for x in D:
    print(x,D[x])


# In[47]:


'''Given a list of numbers i.e[1,2,4,-5,7,9,3,2], make 
another list that contains all the items in sorted order from min
to max .'''
L=[1,2,4,-5,7,9,3,2]
for j in range(len(L)):
    m=L[j]
    idx=j
    c=j
    for i in range(j,len(L)):
        if L[i]<m:
            m=L[i]
            idx=c
        c+=1
    tmp = L[j]
    L[j] = m
    L[idx] = tmp
print(L)


# In[43]:


L=[1,2,4,-5,7,9,3,2]
m=L[0]
idx=0
c=0
for i in L:
    if i<m:
        m=i
        idx=c
    c+=1
tmp=L[0]
L[0]=m
L[idx]=tmp
print(L)


# # functions
# 

# In[1]:


def printsuccess():
    '''This string does nothing'''
    print("The task was successfully executed")
    print("The function works as well,yayyy")


# In[49]:


printsuccess()


# In[3]:


get_ipython().run_line_magic('pinfo2', 'printsuccess')


# In[7]:


def printmsg(msg):
    """The function prints the message supplied by the user or 
    prints the message is not in the form of the string"""
    if isinstance(msg,str):
        print(msg)
    else:
        print("Your message is not a string")
        print("Here is what you have provided",msg)
        print("The type of your input is:",type(msg))
printmsg(998)
    
   


# In[9]:


def mypow(a,b):
    """This function computes just like builtin poaw function"""
    c=a**b
    print(c)
mypow(3,4)


# In[12]:


def checkargs(a,b,c):
    if isinstance(a,(int,float)) and isinstance(b,(int,float)) and isinstance(c,(int,float)):
        print((a+b+c)**2)
    else:
        print("Error : the input arguments are not of the expected types")
checkargs(2,3,4)
    


# In[13]:


checkargs(2.3,4,6)


# In[14]:


checkargs(3,4,"g")


# In[15]:


ckeckargs(2,3)


# In[4]:


from math import pi
def areaofcircle(rad):
    if isinstance(rad,(int,float)):
        area= pi * rad**2
        print("Area of the circle is: "+ str(area))#type casting and string concatenation
    else:
        print("Error: You entered a wrong input.")
areaofcircle(3)
areaofcircle(8.9)
areaofcircle('hello')


# In[8]:


#default arguments
def f(a,b,c):
    print("A is :",a)
    print("B is :",b)
    print("C is :",c)


# In[9]:


f(2,3,"Game")


# In[10]:


f(c="game",a=2,b=3)


# In[7]:


#scope of a variable
def myadd(a,b):
    sumval = a+b
    return sumval


# In[8]:


d = myadd(2,3)
print(d)


# In[4]:


variableoutsidethefunction=3
def g():
    variableoutsidethefunction=7
    #print(variableoutsidethefunction)
g()


# In[18]:


print(g())
type(g())


# In[15]:


print(variableoutsidethefunction)


# In[8]:


#return works like a break statement in a loop 
#as soon as it occurs it exits the function
def h():
    print("A")
    a=3
    b=5
    c=a+b
    print("something")
    return c
    print("B")
    print("C")


# In[9]:


h()


# In[10]:


#return statement can return multiple values
def r():
    a = 5
    b = 7
    c = "something"
    return a,b,c


# In[11]:


x,y,z = r()
print(x,y,z)


# In[14]:


#variable number of arguments
def add(*args):
    sum = 0
    for i in range(len(args)):
         sum+=args[i]#sum=sum+args[i]
    return sum
        


# In[16]:


add(3,4,5,6,4.6,55)


# In[24]:


def oddeven(*args):
    odd = 0
    even = 0
    for i in range(len(args)):
        if args[i]%2==0:
            even+=1
        else:
            odd+=1
    print("Number of even numbers are: ",even)
    print("Number of odd numbers are: ",odd)


# In[25]:


oddeven(2,3,4,5)


# In[26]:


#variable number of arguments as a dictionary 

def printallvariablenamesandvalues(**args):
    
    for x in args:
        print("The variable is: ",x," And its value is: ",args[x])
        
printallvariablenamesandvalues(a=3,b="b",c=78.9)


# In[30]:


def giveavg(**args):
    sum=0
    c=0
    for x in args:
        print("The subject is:",x," And marks in this subject are: ",args[x])
        sum+=args[x]
        
    print("The average of marks are:", sum/len(args))
giveavg(Maths = 79,English = 88,Science=65.2,Computer=71.2,Accounting=81)


# In[1]:


import sys
sys.path.append('/Users/gunjankhatri/Downloads')


# In[3]:


import My_Universal_functions as myfs


# In[6]:


c = myfs.addallnumerics(2,3,4,5)
print(c)


# In[7]:


from My_Universal_functions import addallnumerics


# In[9]:


d = addallnumerics(2,3,4,6,5)
print(d)


# In[11]:


myfs.myName


# In[12]:


'''Given a list of numbers i.e[1,2,4,-5,7,9,3,2], make 
another list that contains all the items in sorted order from min
to max .'''


# In[36]:


def findmin(L,startindex):
    m=L[startindex]
    idx=startindex
    for i in range(startindex,len(L)):
        x = L[i]
        if x<m:
            m = x
            idx = i
        else:
            pass
    return  m,idx


# In[38]:


a,b= findmin([2,3,5,4,9],0)


# In[39]:


print(a,b)


# In[40]:


def swapval(L,idx1,idx2):
    tmp = L[idx1]
    L[idx1] = L[idx2]
    L[idx2] = tmp
    return L


# In[41]:


L = [2,3,5,7]
L2 = swapval(L,1,3)
print(L2)


# In[42]:


from My_Universal_functions import checkifnotnumeric
def sortlist(L):
    if not(checknumeric(L)):
        print(" Error: List does not contain numeric values ")
        return
    else:
        c=0
        for x in L:
            m,idx = findmin(L,c)
            L = swapval(L,c,idx)
            c+=1
    return L


# In[43]:


def checknumeric(L):
    for x in L:
        if not(isinstance(x,(int,float))):
            return False
        return True


# 

# In[44]:


L2 = sortlist([2,3,-8,5,6])
print(L2)


# # strings

# In[1]:


s="Python is a good language"
t="It's good for data science"


# In[2]:


type(s)


# In[3]:


print(s)


# In[4]:


print("Hello",12,"hello2",'who are you',5.9)


# In[9]:


v=s+". "+t


# In[10]:


print(v)


# 

# In[11]:


price = 12
s="The price of this book"
v = s + 'is: ' + str(price)
print(v)
print(s," is:",price)


# In[12]:


a="""This is line 1
this is line 2
this is line 3"""
print(a)


# In[16]:


s="How are you and who are you"
print(s[5])
type(s[5])


# In[19]:


s[:9]


# In[21]:


s[-1]


# In[22]:


s[-3]


# In[24]:


s[-12:-3]


# In[27]:


s[8]="e" #This cannot happen and will show an error.
#Hence strings in python are immutable


# In[28]:


s[0:12:2] #s[start:end:step]


# In[30]:


s[::-1]



# In[42]:


mystring="Hello guys whats up?"
a=mystring[::-1]
print(a)


# In[43]:


print(a[10:])


# In[51]:


b=mystring[11:16]
print(b[::-1])


# In[1]:


'''String methods
Those functions that are associated with datastructures and are called using a dot are sometimmes called methods.''' 


# In[2]:


a="    ABC Def hgq  asdnjhi   "
b=a.strip()
print(b)


# In[3]:


a="ABD efk GHF Huf"
b=a.lower()
print(b)


# In[7]:


a="Hubffj ;; jghug HGIIK "
b=a.upper()
print(b)


# In[8]:


d=a.replace(";","*")
print(d)


# In[9]:


a="abd:gehf:tjyu:kjuh:klkhij"
L=a.split(":")
print(L)


# In[10]:


L[2]


# In[13]:


a="life si oot,short dont loose,yna time  "
b=a.strip()
#print(b)
c=b.replace(","," ")
print(c)


# 

# In[ ]:




