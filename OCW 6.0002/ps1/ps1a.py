###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name: Breno
# Collaborators:
# Time: 3h

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    file = open(filename, "r")
    cows_dic = {}
    
    for line in file:
        name, weight = line.split(',')
        cows_dic[name] = int(weight)
        
    file.close()
    
    return cows_dic

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    #create a list with all the cows sorted by their weight
    #whenever it's possible, add another cow to the trip if it's possible
    #
    cows_list = sorted(cows, key=cows.get, reverse=True)
    trips = []
    #while we still have cows remain doing the trip
    while len(cows_list)>0:
        #stablish the max numbers of cows per travel
        #always get the cow with higher weight value first
        actual_trip = []
        weight_limit = limit
        for cow in cows_list:
            if cows[cow] <= weight_limit:
                weight_limit - cows[cow]
                actual_trip.append(cow)
                cows_list.remove(cow)
        trips.append(actual_trip)
    
    return trips
    
# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    weight_limit = limit
    cows_dic_copy = cows.copy()
    cows_list = cows_dic_copy.keys()
    result= []
    actual_result = []
    
    for cows_partition in get_partitions(cows_list):
        max_trips = 0
        for trip in cows_partition:
            actual_weight = 0
            for cow in trip:
                actual_weight += cows[cow]
            if actual_weight <= weight_limit:
                max_trips += 1
        if len(cows_partition) == max_trips:
            actual_result.append(cows_partition)
            break
#    print(len(result[0]))
#    print(result)    
    return result
            
            
            
    
        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    cows_dic = load_cows("ps1_cow_data.txt")
    limit = 10
    
    start_1 = time.time()
    Trips_1 = greedy_cow_transport(cows_dic,limit)
    end_1 = time.time()
    print(end_1 - start_1)
    
    start_2 = time.time()
    Trips_2 = greedy_cow_transport(cows_dic,limit)
    end_2 = time.time()
    print(end_2 - start_2)
    
    
    
if __name__ == '__main__':
    compare_cow_transport_algorithms()    
    
#compare_cow_transport_algorithms()
#cows = load_cows("ps1_cow_data.txt")
#print(greedy_cow_transport(cows,limit=10))
#for partition in get_partitions([1,2,3]):
#    print(partition)
    
#brute_force_cow_transport(cows,limit=10)
