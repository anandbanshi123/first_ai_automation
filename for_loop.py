

#till 0
list1=['saturday','sunday','monday','tuesday','wednesday','thursday','friday']

for i in list1:
    print("value using foreach loop:", i)


# for i in range(len(list1)-1, -1, -1):

var="I have python code"
print(var)
var2=var.split() #['I', 'have', 'python', 'code']
print(var2)
for i in range(len(var2)):
    if var2[i]=='python':
        print(var2[i])
        continue
    print("word:", var2[i])
       
