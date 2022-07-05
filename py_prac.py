import json



day =[]
test = {
    
    1 : [1, day, 3],
    2 : ["hi"],
    21: [],
    3 : [3, 'hiih']}

 
t = {}
t[1] = [1, [2,3], 4]
print(type(t[1]))
t[1][1].append(5)
t[1].append([4])

print(t[1])

# file = open("py_test.json","w")
# json.dump(test, file, separators=(',', ':'))
    
# file.close