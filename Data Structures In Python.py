#!/usr/bin/env python
# coding: utf-8

# # DATA STRUCTURES IN PYTHON
# 

# In[6]:


L=[1,3,4.9,"name",3]
T=(1,3,4.9,"name",3)
S={1,3,4.9,"name",3}
D={23:"twothree",'B':43,'C':"CCD"}
print("The type of L is:",type(L))
print("The type of T is:",type(T))
print("The type of S is:",type(S))
print("The type of D is:",type(D))


# In[14]:


print(L[1])
print(T[1])
print(3 in S) #Would return a true or false
print(D[23])
print(D['B'])
S #no duplicates would be printed becausse no duplicates are allowed in S


# In[17]:


L


# In[18]:


L[1:3]


# In[19]:


L[::-1]


# In[20]:


T[:3] #till the 4th element


# In[84]:


List=["Hello","everybody","let's","learn"]
Tup=("Hello","everybode","let's","learn")
Set={"Hello","everybode","let's","learn"}
Dict={1:"Hello",2:"everybody",3:"let's",4:"learn"}

List=List+["insertion"]
print(List)

# Or we can use .append function to add an elemnt at the end of any list
#List.append("insertion")
#print(List)


Tup2=("insertion",)#"insertion"==("insertion"); so add a comma just to show that it is a tuple
Tup3=()
Tup3=Tup+Tup2
print(Tup3)

Set.add("insertion")
print(Set)

Dict[5]="insertion"
print(Dict)

#Concatenation caanot happen for a dictionary
Dict2={6:"six",7:"seven"}
#Dict3=Dict+Dict2
#print(Dict3)

# but we can use update function and add a whole new dictionary into an already existing dictionary
print("\n")
Dict.update(Dict2)
print(Dict)


# In[53]:


del List[4]


# In[54]:


List


# In[71]:


Set


# In[72]:


Set.remove('insertion')


# In[73]:


Set


# In[75]:


del Dict[5]


# In[76]:


Dict


# In[85]:


List2=List


# In[86]:


List2


# In[93]:


'''Now if I make changes in List2 then List would also be changed because both variables are pointing toward
Same memory'''
List2[3]="Gunjan"
List2
#This is called referencing


# In[94]:


List


# In[97]:


#If you don't want this to happen then call copy function
List3=List.copy()
print(List3)


# In[98]:


List3[2]=44
List3


# In[100]:


List#Same concept for Sets and dictionaries


# In[101]:


List3[2:5]
List3
#this way List# is already a copy and both DONOT point to the same memory. 
#Hence if we make changes to List3 it wont efect List
#in Numpy it is not true


# In[104]:


L1=["start","def","9.6","jdfjd","end"]
L2=L1[::-2]
L2


# In[105]:


L2.pop()


# In[106]:


L2


# In[107]:


L2.append("start")


# In[108]:


L2


# In[109]:


get_ipython().run_line_magic('pinfo', 'L2.insert')


# In[110]:


L2.insert(0,"hello")


# In[111]:


L2


# In[112]:


Set


# In[124]:


A = {1, 2, 3}
B = {2}

#C = A.difference(B)      # returns a new set: {1, 3}
A.difference_update(B)   # modifies A to: {1, 3}
print(A)
print(B)
print(C)


# In[127]:


L


# In[128]:


S


# In[129]:


T


# In[130]:


D


# In[131]:


D2={'A':L,'B':S,'C':T,'D':D}


# In[132]:


D2


# In[134]:


D2['A'][2]


# In[141]:


K=D2['D']


# In[142]:


for i in K:
    print(i,K[i])


# In[147]:


L4=[L,T,D,"game",33]
type(L4[3])


# In[152]:


L5=[x**2 for x in range(0,10)]#go from 0 to 10 do not include 10
L5


# In[154]:


S3={x**2 for x in range(0,20,2)}# go from 0 to 20 do not include 20 with the step of 3 
S3


# In[7]:


'''You are a teacher and you have different student recordes containing id of a student and mark lists 
in each subject where each student has taken different number of subjects. All these records are in hard copy. 
You want to enter all the data in computer and want to compute average marks of each student 
display'''

def getDataFromUser():
    D={}
    while True:
        studentId = input("Enter student id: ")
        marksList = input("Enter the marks separated by comma: ")
        moreStudents = input("Enter 'no' to quit insertion:  ")
        if studentId in D:
            print(studentId, " is already inserted")
        else:
            D[studentId] = marksList.split(",")
        if moreStudents.lower() == "no":
            return D


# In[12]:


data = getDataFromUser()


# In[13]:


data


# In[16]:


def getAvgMarks(D):
    avgMarks = {}
    for x in D:
        L= D[x]
        s=0
        for marks in L:
            s+=int(marks)
        avgMarks[x]=s/len(L)
    return avgMarks


# In[17]:


avgM = getAvgMarks(data)


# In[18]:


for x in avgM:
    print("Student: ",x,"got :",avgM[x]," of average marks")


# In[34]:


#take the given string make it "Life is too short dont loose any time" 
mystring="life si oot, short dont loose, yna time   "
mystring = mystring.capitalize()
mystring = mystring.strip()
mystring = mystring.replace(","," ")
myList = mystring.split()
myList[1]=myList[1][::-1]
myList[2]=myList[2][::-1]
myList[6]=myList[6][::-1]

myList



# In[ ]:




