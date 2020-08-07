from math import sqrt

def loadMovieLens():
    str1 = 'movielens/u.item'
    
    movies = {}
    for line in open(str1, encoding = "ISO-8859-1", mode='r'):
        print(line)
        (id,title) = line.split('|')[0:2]   
        movies[id] = title
       
    prefer = {}
    for line in open('movielens/u.data'):
        (user, movieid, rating,ts) = line.split('\t')   
        prefer.setdefault(user, {})    
        prefer[user][movies[movieid]] = float(rating)
    
    return prefer


def sim_distance(prefer, person1, person2):   
    sim = {}
    for item in prefer[person1]:
        if item in prefer[person2]:
            sim[item] = 1       
    if len(sim)==0:         

        return 0

    sum_all = sum([pow(prefer[person1][item]-prefer[person2][item], 2)

                   for item in sim])

    return 1/(1+sqrt(sum_all))

def sim_pearson(prefer, person1, person2):
    sim = {}
    for item in prefer[person1]:
        if item in prefer[person2]:
            sim[item] = 1           
    n = len(sim)
    if len(sim)==0:
        return -1
    sum1 = sum([prefer[person1][item] for item in sim])  
    sum2 = sum([prefer[person2][item] for item in sim])  
    sum1Sq = sum( [pow(prefer[person1][item] ,2) for item in sim] )
    sum2Sq = sum( [pow(prefer[person2][item] ,2) for item in sim] )
    sumMulti = sum([prefer[person1][item]*prefer[person2][item] for item in sim])
    num1 = sumMulti - (sum1*sum2/n)
    num2 = sqrt( (sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
    if num2==0:
        return 0
    return num1/num2


def topMatches(prefer, person, n=2, similarity=sim_pearson):
    scores=[ (similarity(prefer,person,other),other) for other in prefer if other!=person ]
  
    scores.sort()    
    scores.reverse()
    return scores[0:n]              


def getRecommendations(prefer, person, similarity=sim_pearson):
    totals = {}
    simSums = {}
    for other in prefer:
        if other == person:
            continue
        else:
            sim = similarity(prefer, person, other)   
        if sim<=0: continue
        for item in prefer[other]:
            if item not in prefer[person]:
               
                totals.setdefault(item,0) 
                totals[item] += prefer[other][item]*sim
              
                simSums.setdefault(item,0)
                simSums[item] += sim

    ranks = [ (total/simSums[item],item) for item,total in totals.items() ]
   
    ranks.sort()
    ranks.reverse()
    return ranks

print("\n-------------------MovieLens test system--------------------")
prefers =  loadMovieLens()
print("\n1.*********recommend according to user **********\n")
print("for user 87:",prefers['87'])
print("\n**********Recommend movies*********\n")
recomends = getRecommendations(prefers, '87')[0:20]
print(recomends)