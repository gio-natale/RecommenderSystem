from string import *
import random

def opencheckfile(filename):
    try:
        f = open(filename, "r")
    except:
        raise IOError, "The file %s does not exist" %filename
    return f

def valid(value):
    try:
        value = int(value)
        if value <= 0:
             print "Please type a value greater than 0."
             return False
    except:
        if value != "":
            print "Invalid typing. Please enter another value."
            return False
    return True

def insert(item, list):
    if list == []:
        return [item]
    else:
        low = 0
        up = len(list) - 1
        while up - low > 0:
            mid = (low + up + 1)/2
            if item[1] > list[mid][1]:
                up = mid - 1
            else:
                low = mid
        if item[1] > list[low][1]:
            list = list[:low] + [item] + list[low:]
        else:
            list = list[:low+1] + [item] + list[low+1:]
        return list

def rate(ratings):
    toRate = range(len(books))
    for n in range(len(books)/5):
        j = random.randint(0, len(toRate)-1)
        mark = raw_input("%s " %books[toRate[j]][:-1])
        while mark not in ["-5", "-3", "0", "1", "3", "5"]:
            print "Invalid rating. Type again."
            mark = raw_input("%s " %books[toRate[j]][:-1])
        ratings[username][toRate[j]] = int(mark)
        del toRate[j]
    return ratings

#read from files
#dictionary; ratings = { "user" : [rating, ...], ...}
#list; books = ["author, title\n", ...]
inp1 = opencheckfile("ratings.txt") #non existing files
inp1_lines = inp1.readlines()
ratings = {}
for i in range(len(inp1_lines)):
    if i%2 == 0:
        user = inp1_lines[i][:-1]
        ratings[user] = []
    else:
        inp1_lines[i] = split(inp1_lines[i], " ")
        for j in range(len(inp1_lines[i])-1):
            ratings[user] += [int(inp1_lines[i][j])]
inp1.close()
inp2 = open("books.txt", "r")
books = inp2.readlines()
inp2.close()

#ask for username
username = raw_input("Type your username: ")

#ask for rating if user doesn't exist
if username not in ratings:
    ratings[username] = [0]*len(books)
    print "Please rate the following books with these values: 5 if you really liked it, 3 if you liked it, 1 if it was OK, 0 if you haven't read it, -3 if you didn't like it, -5 if you hated it:"
    ratings = rate(ratings)
    while ratings[username] == [0]*len(books):
        print
        print "More ratings are needed to give recommendations."
        ratings = rate(ratings)

#calculate similarity
similarlist = []
for user in ratings:
    if user != username:
        similarity = 0
        for i in range(len(books)):
            similarity += ratings[user][i]*ratings[username][i]
        if similarity > 0:
            similarlist = insert([user, similarity], similarlist)

#ask for no of recommendations
no = raw_input("Type number of recommendations or press 'Enter': ")
while not valid(no):
    no = raw_input("Type number of recommendations or press 'Enter': ")
if no == "":
    no = 10
no = int(no)

#output recommendations from first users
indList = range(len(books))        
j = 0
while j < len(indList):
    if ratings[username][indList[j]] != 0:
        del indList[j]
    else:
        j += 1
i = 0
f = open("output.txt", "w")
f.write("Recommendations for %s:\n" %username)
total = no
while no > 0 and i < len(similarlist):
    recommender = similarlist[i][0]
    j = 0
    while j < len(indList) and no > 0:
        if ratings[recommender][indList[j]] >= 3:
            rec = "\"%s\" recommended by %s" %(books[indList[j]][:-1], recommender)
            f.write(rec+"\n")
            print rec
            del indList[j]
            no -= 1
        else:
            j += 1
    i += 1

if no > 0:
    out = "There are only %s recommendations available." %(total-no)
    print out

f.close()
