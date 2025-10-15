# -*- coding: utf-8 -*-
"""
Author(s): Linda Su
Consulted:
Date: 2025.04.27
Purpose: Yelp task: Working with dictionaries and tuples and
    real world data. YELP data set covers different metropolitan areas
    in 4 countries (not including Boston).
"""

#---------#
# Imports #
#---------#

# This will be needed to access JSON loading and storing functions.
import json

#---------------------------#
# Write your functions here #
#---------------------------#
def loadData(filename):
    '''load the data'''
    with open(filename, 'r') as f:
        return json.load(f)
    
def getBusinessCount(yelpDict, businessName):
    '''returns an integer count of businesses with businessName in the given Yelp dictionary yelpDict'''
    count = 0
    for bizID in yelpDict:
        if yelpDict[bizID]['name'].lower() == businessName.lower():
            count += 1
    return count

def uniqueCities(yelpDict):
    '''takes a Yelp dictionary,
and returns a list of all cities that appear in it, in alphabetical order,
where each city appears only once in the list'''
    result = []
    for bizID in yelpDict:
        if yelpDict[bizID]['city'] not in result:
            result.append(yelpDict[bizID]['city'])
    new = sorted(result)
    return new

def SortByStar(bus):
    '''sort'''
    return (bus['stars'],bus['name'])

def findBusinesses(yelpDict, category, city, starLimit, minReview, outFilename):
    '''creates a list of business dictionaries with the given category,
located in the given city,
whose stars are at or exceeding the starLimit,
and whose review_count is at or exceeding the minReviews.'''
    result = []
    for bizID in yelpDict:
        if category in yelpDict[bizID]['categories']:
            if yelpDict[bizID]['city'] == city:
                if yelpDict[bizID]['stars'] >= starLimit:
                    if yelpDict[bizID]['review_count'] >= minReview:
                        result.append(yelpDict[bizID])
    new = sorted(result,key=SortByStar)
    with open(outFilename, 'w') as f:
        json.dump(new,f)
        
def findCategories(yelpDict,threshold):
    '''Only categories whose total count meets or exceeds the given threshold should be included in the resulting dictionary.'''
    AllCategories = {}
    for bizID in yelpDict:
        for category in yelpDict[bizID]['categories']:
            if category not in AllCategories:
                AllCategories[category] = 1
            else:
                AllCategories[category] += 1
    SortedCategories = {}
    for item in AllCategories.items():
        if item[1] >= threshold:
           SortedCategories[item[0]] = item[1]
    return SortedCategories

def bestPizzaPlace(yelpDict):
    '''returns a list containing one or more business dictionaries from the given yelpDict with 'Pizza' as a category that have the highest star rating'''
    result = []
    maxStar = 0
    maxReview =  0
    for bizID in yelpDict:
        if 'Pizza' in yelpDict[bizID]['categories']:
            bus = yelpDict[bizID]
            if bus['stars'] == maxStar:
                if bus['review_count'] == maxReview:
                    result.append(bus)
                elif bus['review_count'] > maxReview:
                    result = [bus]
                    maxReview =  bus['review_count']
            elif bus['stars'] > maxStar:
                result = [bus]
                maxStar =  bus['stars']
                maxReview =  bus['review_count']
    return result
        
        

#--------------#
# Testing data #
#--------------#

soloYelp = {
  "XguKrY0dAuaK1W6HUlUQ1Q": {"state": "OH", "address": "547 Sackett Ave", "review_count": 29, "stars": 3.5, "name": "Retz's Laconi's II", "city": "Cuyahoga Falls", "categories": ["Italian", "Restaurants", "Pizza"]}
}

microYelp = {
  "PMH4oUa-bWELKogdtkWewg": {'state': 'ON', 'address': '100 City Centre Dr', 'review_count': 16, 'stars': 2.0, 'name': 'GoodLife Fitness', 'city': 'Mississauga', 'categories': ['Fitness & Instruction', 'Sports Clubs', 'Gyms', 'Trainers', 'Active Life']},
  "XguKrY0dAuaK1W6HUlUQ1Q": {'state': 'OH', 'address': '547 Sackett Ave', 'review_count': 29, 'stars': 3.5, 'name': "Retz's Laconi's II", 'city': 'Cuyahoga Falls', 'categories': ['Italian', 'Restaurants', 'Pizza']},
  "Wpt0sFHcPtV5MO9He7yMKQ": {'state': 'NV', 'address': '3020 E Desert Inn Rd', 'review_count': 20, 'stars': 2.0, 'name': "McDonald's", 'city': 'Las Vegas', 'categories': ['Restaurants', 'Fast Food', 'Burgers']},
  "1K4qrnfyzKzGgJPBEcJaNQ": {'state': 'ON', 'address': '1058 Gerrard Street E', 'review_count': 39, 'stars': 3.5, 'name': 'Chula Taberna Mexicana', 'city': 'Toronto', 'categories': ['Tiki Bars', 'Nightlife', 'Mexican', 'Restaurants', 'Bars']},
  "7gquCdaFoHZCcLYDttpHtw": {'state': 'SC', 'address': '8439 Charlotte Hwy', 'review_count': 17, 'stars': 4.0, 'name': 'Bubbly Nails', 'city': 'Fort Mill', 'categories': ['Nail Salons', 'Beauty & Spas']},
  "Mmh4w2g2bSAkdSAFd_MH_g": {'state': 'SC', 'address': '845 Stockbridge Dr', 'review_count': 77, 'stars': 3.0, 'name': 'Red Bowl', 'city': 'Fort Mill', 'categories': ['Restaurants', 'Asian Fusion']},
  "vMO2vNyWLuxumso7t3rbYw": {'state': 'ON', 'address': '300 Borough Drive', 'review_count': 5, 'stars': 4.0, 'name': "Pablo's Grill It Up", 'city': 'Scarborough', 'categories': ['Food Court', 'Restaurants', 'Barbeque']},
  "h2XsV6mR6c7QURhlsi0RqA": {'state': 'AZ', 'address': '211 E 10th Dr, Ste 2', 'review_count': 26, 'stars': 4.5, 'name': "John's Refrigeration Heating and Cooling", 'city': 'Mesa', 'categories': ['Home Services', 'Air Duct Cleaning', 'Local Services', 'Heating & Air Conditioning/HVAC']},
  "c6Q3HP4cmWZbD9GX8kr4IA": {'state': 'NC', 'address': '4837 N Tryon St', 'review_count': 8, 'stars': 3.5, 'name': 'Pep Boys', 'city': 'Charlotte', 'categories': ['Auto Parts & Supplies', 'Auto Repair', 'Tires', 'Automotive']},
  "1EuqKW-JC-Fm3RSWRqKdrg": {'state': 'NV', 'address': '2075 E Warm Springs Rd', 'review_count': 5, 'stars': 5.0, 'name': 'Life Springs Christian Church', 'city': 'Las Vegas', 'categories': ['Religious Organizations', 'Churches']},
  "VZ37HCZVruFm-w_Mkl1aEQ": {'state': 'AZ', 'address': '13637 N Tatum Blvd, Ste 8', 'review_count': 16, 'stars': 5.0, 'name': 'Conservatory of Dance', 'city': 'Phoenix', 'categories': ['Education', 'Dance Schools', 'Arts & Entertainment', 'Fitness & Instruction', 'Specialty Schools', 'Active Life', 'Dance Studios', 'Performing Arts']},
  "htKaC4cHY4wlB4Wqb8CDnQ": {'state': 'PA', 'address': '4730 Liberty Ave', 'review_count': 4, 'stars': 4.0, 'name': 'Allure', 'city': 'Pittsburgh', 'categories': ['Accessories', "Women's Clothing", 'Fashion', 'Shopping']},
  "7fiIMBxbOYdAv3XMcmWivw": {'state': 'OH', 'address': '850 Euclid Ave', 'review_count': 3, 'stars': 3.0, 'name': "Renee's Relaxation and Body Mechanics", 'city': 'Cleveland', 'categories': ['Massage', 'Beauty & Spas']},
  "4SBY4CHiMD8YOCEU9_fdnw": {'state': 'ON', 'address': '123 Queen Street W', 'review_count': 3, 'stars': 4.0, 'name': 'Fidora Salon and Spa', 'city': 'Toronto', 'categories': ['Day Spas', 'Hair Salons', 'Beauty & Spas']},
  "6aFAEeJ3nS-iWGt7Tn7S0Q": {'state': 'NC', 'address': '19925 Jetton Rd, Ste 100', 'review_count': 5, 'stars': 5.0, 'name': 'KS Audio Video', 'city': 'Cornelius', 'categories': ['Home Services', 'Television Service Providers', 'Home Automation', 'Home Theatre Installation', 'Professional Services']},
}
