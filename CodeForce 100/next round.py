# separated value of n and k
a = input("")
n = a.split(" ")[0]
k = a.split(" ")[1]


# the sequence of scores
scores = input("")
score = scores.split(" ")
score_of_k = int((score[int(k)-1]))

count = 0 
for i in score:
    if int(i) >= score_of_k and int(i) != 0:
        count += 1
print(count)