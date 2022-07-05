# file = open("naver_test.txt","a")

test = {
    1 : [1,2],
    2 : ["hi"],
    21: [],
    3 : [3, 'hiih']}

# print(test[21])

for i in test:
    if test[i]:
        print(str(i) + "is not empty")
    else: 
        print(str(i) + "is empty")

print(test.get(5) == None)  


  
    
# file.close