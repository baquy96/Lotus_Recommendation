from Predict_Null_Value import predict
from math import sqrt


def pearson(rating1, rating2):
    sum_xy = 0
    sum_x = 0
    sum_y = 0
    sum_x2 = 0
    sum_y2 = 0
    n = 0
    for key in rating1:
        if key in rating2:
            n += 1
            x = rating1[key]
            y = rating2[key]
            sum_xy += x * y
            sum_x += x
            sum_y += y
            sum_x2 += pow(x, 2)
            sum_y2 += pow(y, 2)
    if n == 0:
        return 0
    # now compute denominator
    denominator = sqrt(sum_x2 - pow(sum_x, 2) / n) * \
                  sqrt(sum_y2 - pow(sum_y, 2) / n)

    if denominator == 0:
        return 0
    else:
        return (sum_xy - (sum_x * sum_y) / n) / denominator


def computeNearestNeighbor(data, username):
    """creates a sorted list of users based on their distance
    to username"""
    distances = []
    for instance in data:
        if instance != username:
            distance = pearson(data[username],
                               data[instance])
            distances.append((instance, distance))
    # sort based on distance -- closest first
    distances.sort(key=lambda artistTuple: artistTuple[1],
                   reverse=True)
    return distances


def recommend(data, user, k):
    """Give list of recommendations"""
    recommendations = {}
    # first get list of users  ordered by nearness
    nearest = computeNearestNeighbor(data, user)
    if len(nearest) < k:
        k = len(nearest)
    #
    # now get the ratings for the user
    #
    userRatings = data[user]
    #print(nearest)
    #
    # determine the total distance
    totalDistance = 0.0
    for i in range(k):
        totalDistance += nearest[i][1]
    # now iterate through the k nearest neighbors
    # accumulating their ratings
    if totalDistance == 0:
        return []
    for i in range(k):
        # compute slice of pie
        weight = nearest[i][1] / totalDistance
        # get the name of the person
        name = nearest[i][0]
        # get the ratings for this person
        neighborRatings = data[name]
        # get the name of the person
        # now find bands neighbor rated that user didn't
        for artist in neighborRatings:
            if not artist in userRatings:
                if artist not in recommendations:
                    recommendations[artist] = neighborRatings[artist] * \
                                              weight
                else:
                    recommendations[artist] = recommendations[artist] + \
                                              neighborRatings[artist] * \
                                              weight
    # now make list from dictionary and only get the first k items
    recommendations = list(recommendations.items())[k]
    recommendations = [(u, v)
                       for (u, v) in recommendations]
    # finally sort and return
    recommendations.sort(key=lambda artistTuple: artistTuple[1],
                         reverse=True)
    return recommendations

def createData():
    data = predict()
    res = {}
    # This factor is just random. It will change later.
    factor = {'sales': 1.6, 'views': 1.4, 'carts': 2, 'sales_effective_rate': 1, 'rating': 1.2, 'comments': 1}
    for (item, rating) in data.items():
        tmp = 0
        for (key, num) in factor.items():
            tmp += rating[key] * num
        res[item] = tmp

    data = {}
    for (item1, rating1) in res.items():
        if item1[0] not in data:
            data.setdefault(item1[0], {})
            data[item1[0]][item1[1]] = rating1
        for (item2, rating2) in res.items():
            if item1[0] == item2[0] and item2[1] not in data[item2[0]]:
                data[item2[0]][item2[1]] = rating2
    return data

def result():
    data = createData()
    for user in data.keys():
        print(recommend(data, user, 10))

result()
