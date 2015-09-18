
critics = {'Lisa Rose': {'Lady in the Water': 2.5,'Snakes on a Plane': 3.5,'Just My Luck':3.0,'Superman Returns':3.5,'You, Me and Dupree':2.5,'The Night Listener':3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 3.5},
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0,
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

from math import sqrt
#Returs a distance-based similarity score for person 1 and person 2
def sim_distance(prefs,person1,person2):
	#get the list of shared-items
	si={}
	for item in prefs[person1]:
		if item in prefs[person2]:
			si[item]=1
	#if the have no ratings in common, return 0
	if len(si)==0: return 0

	#Add up the squares of all the differences
	sum_of_squares = sum([pow(prefs[person1][item]-prefs[person2][item],2)
						for item in prefs[person1] if item in prefs[person2]])
	return 1/(1+sum_of_squares)


	# Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(prefs,p1,p2):
	si={}
	for item in prefs[p1]:
		if item in prefs[p2]: si[item]=1
 	# Find the number of elements
	n=len(si)
	# if they are no ratings in common, return 0
	if n==0: return 0
	# Add up all the preferences
	sum1=sum([prefs[p1][it] for it in si])
 	sum2=sum([prefs[p2][it] for it in si])
 	# Sum up the squares
 	sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
 	sum2Sq=sum([pow(prefs[p2][it],2) for it in si])
 	# Sum up the products
 	pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])
 	# Calculate Pearson score
 	num=pSum-(sum1*sum2/n)
 	den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
 	if den==0: return 0
 	r=num/den
 	return r


def topMatches(prefs,person,n=5,similarity=sim_pearson):
	scores=[(similarity(prefs,person,other),other)
	for other in prefs if other!=person]

	#sort the list so that highest appears at top
	scores.sort()
	scores.reverse()
	return scores[0:n]
def itemRecommender(prefs,itemMatch,user):
	userRatings=prefs[user]
	totals={}
	totalSim={}
	for (item,rating) in userRatings.items():
		for (similarity,item2) in itemMatch[item]:
			if item2 in userRatings:continue
			totals.setdefault(item2,0)
			totals[item2]+=similarity*rating

			totalSim.setdefault(item2,0)
			totalSim[item2]+=similarity

	rankings=[(totals/totalSim[item],item)for item,totals in totals.items()]

	rankings.sort()
	rankings.reverse()
	return rankings


def myRecommender(prefs,person,similarity=sim_pearson):
	totals={}
	simSums={}
	for other in prefs:
		if other==person:
			continue
		sim=similarity(prefs,person,other)
		if sim<=0 : continue
		for item in prefs[other]:
			if item not in prefs[person] or prefs[person][item]==0:
				totals.setdefault(item,0)
				totals[item]+=prefs[other][item]*sim
				simSums.setdefault(item,0)
				simSums[item]+=sim
	rankings = [(total/simSums[item],item) for item,total in totals.items()]		
	rankings.sort()
	rankings.reverse()
	return rankings
def transformPrefs(prefs):
	result={}
	for person in prefs:
		for item in prefs[person]:
			result.setdefault(item,{})
			result[item][person]=prefs[person][item]
	return result


def similar_items(prefs,n=4):
	result={}
	item_prefs=transformPrefs(prefs)
	for item in item_prefs:
		scores=topMatches(item_prefs,item,n=4,similarity=sim_pearson)
		result[item]=scores
	return result

def loadMovieLens(path='C:\Users\Aadarsh\Desktop\MovieLens'):
	movies={}
	for line in open(path+'/u.item'):
		(id,title)=line.split('|')[0:2]
		movies[id]=title

	prefs={}
	for line in open(path+'/u.data'):
		(user,movieid,rating,ts)=line.split('\t')
		prefs.setdefault(user,{})
		prefs[user][movies[movieid]]=float(rating)
	return prefs