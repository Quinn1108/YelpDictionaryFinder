# -*- coding: utf-8 -*-
"""
Authors: Sohie Lee, Peter Mawhorter, and Lyn Turbak
Consulted:
Date: 2022-04-12
Purpose: Yelp task tests: tests functions for working with the Yelp data
  set.
"""

import json
import yelp
import optimism
import test_data as td

optimism.skipChecksAfterFail('all')
# If you want optimism to keep running checks when one fails like it used
# to do, uncomment this line:
# optimism.skipChecksAfterFail('case')

def checkJSONFile(results, expectedStructure, filename=None):
    """
    Runs a custom check which loads the specified file in JSON format and
    checks that the result is the same as the given expected structure
    variable. If no filename is specified, checks the first argument to
    the function being tested which was a string ending in '.json'.
    """
    # Get filename automatically if we can
    if filename is None:
        case = results["case"]
        for arg in list(case.args) + list(case.kwargs.values()):
            if isinstance(arg, str) and arg.endswith(".json"):
                filename = arg
                break
    if filename is None:
        raise ValueError(
            f"No filename provided as an extra argument in checkCustom"
            f" and no string argument ending in '.json' found for case:"
            f" {case}"
        )

    # Open file & load as JSON
    with open(filename, 'r') as fileReader:
        result = json.load(fileReader)

    # Compare against expected structure
    dif = optimism.findFirstDifference(result, expectedStructure)
    if dif is None:
        return True
    else:
        return dif

#--------------#
# TESTING CODE #
#--------------#

testLD = optimism.testFunctionMaybe(yelp, "loadData")
testLD.case("soloYelp.json").checkReturnValue(td.soloYelpLoaded)
testLD.case("microYelp.json").checkReturnValue(td.microYelpLoaded)
testLD.case("miniYelp.json").checkReturnValue(td.miniYelpLoaded)

testGBC = optimism.testFunctionMaybe(yelp, "getBusinessCount")
testGBC.case(td.soloYelpLoaded, "Retz's Laconi's II").checkReturnValue(1)
testGBC.case(td.microYelpLoaded, "McDonald's").checkReturnValue(1)
testGBC.case(td.miniYelpLoaded, "Pizza Hut").checkReturnValue(2)
testGBC.case(td.miniYelpLoaded, "pizza hut").checkReturnValue(2)
testGBC.case(td.miniYelpLoaded, "McDonald's").checkReturnValue(3)

testUC = optimism.testFunctionMaybe(yelp, "uniqueCities")
testUC.case(td.soloYelpLoaded).checkReturnValue(["Cuyahoga Falls"])
testUC.case(td.microYelpLoaded).checkReturnValue(
    [
        'Charlotte', 'Cleveland', 'Cornelius', 'Cuyahoga Falls',
        'Fort Mill', 'Las Vegas', 'Mesa', 'Mississauga', 'Phoenix',
        'Pittsburgh', 'Scarborough', 'Toronto'
    ]
)
testUC.case(td.miniYelpLoaded).checkReturnValue(
    [
        'Ahwatukee', 'Anthem', 'Bay Village', 'Bethel Park', 'Boulder City',
        'Cave Creek', 'Champaign', 'Chandler', 'Charlotte', 'Chesterland',
        'Cleveland', 'Cleveland Heights', 'Concord', 'Coraopolis',
        'Cornelius', 'Cuyahoga Falls', 'Davidson', 'Dorval', 'Dunfermline',
        'Edinburgh', 'Elyria', 'Etna', 'Fitchburg', 'Fort Mill',
        'Fountain Hills', 'Frazer', 'Gastonia', 'Gilbert', 'Glendale',
        'Goodyear', 'Henderson', 'Homestead', 'Houston', 'Kent',
        'Lakewood', 'Las Vegas', 'Laval', 'Laveen', 'MESA', 'Madison',
        'Markham', 'Matthews', 'McMurray', 'Mentor',
        'Mentor-on-the-Lake', 'Mesa', 'Mint Hill', 'Mirabel',
        'Mississauga', 'Montreal', 'Montréal', 'Munroe Falls',
        'Newmarket', 'North Las Vegas', 'North Olmsted', 'North York',
        'Oakdale', 'Peoria', 'Phoenix', 'Pineville', 'Pittsburgh',
        'Richmond Hill', 'Rocky River', 'Scarborough', 'Scottsdale',
        'Solon', 'Stuttgart', 'Sun Prairie', 'Surprise', 'Tega Cay',
        'Tempe', 'Toronto', 'Urbana', 'Vaughan', 'Verdun', 'Westlake',
        'Wexford', 'Willoughby', 'Willoughby Hills'
    ]
)

testFB = optimism.testFunctionMaybe(yelp, "findBusinesses")
testFB.case(
    td.soloYelpLoaded,
    'Pizza', 'Cuyahoga Falls', 3, 20,
    'results/testFB-solo-Pizza-Cuyahoga_Falls.json'
).checkCustom(
    checkJSONFile, 
    [
      {
        "address": "547 Sackett Ave",
        "categories": ["Italian", "Restaurants", "Pizza"],
        "city": "Cuyahoga Falls",
        "name": "Retz\'s Laconi\'s II",
        "review_count": 29,
        "stars": 3.5,
        "state": "OH"
      }
    ]
)
testFB.case(
    td.soloYelpLoaded,
    'Pizza', 'Cuyahoga Falls', 4, 20,
    'results/testFB-solo-empty.json'
).checkCustom(checkJSONFile, [])
testFB.case(
    td.microYelpLoaded,
    'Pizza', 'Cuyahoga Falls', 3, 20,
    'results/testFB-micro-Pizza-Cuyahoga_Falls.json'
).checkCustom(
    checkJSONFile,
    [
      {
        "address": "547 Sackett Ave",
        "categories": ["Italian", "Restaurants", "Pizza"],
        "city": "Cuyahoga Falls",
        "name": "Retz\'s Laconi\'s II",
        "review_count": 29,
        "stars": 3.5,
        "state": "OH"
      }
    ]
)
testFB.case(
    td.miniYelpLoaded,
    'Food', 'Charlotte', 4, 10,
    'results/testFB-mini-Food-Charlotte.json'
).checkCustom(
    checkJSONFile,
    [
      {
        "address": "1710 Kenilworth Ave, Ste 220",
        "categories": [
          "Breakfast & Brunch",
          "Food",
          "Coffee & Tea",
          "Donuts",
          "Restaurants"
        ],
        "city": "Charlotte",
        "name": "Duck Donuts",
        "review_count": 373,
        "stars": 4.5,
        "state": "NC"
      },
      {
        "address": "2838 The Plz",
        "categories": [
          "Pizza",
          "Food",
          "Internet Cafes",
          "Restaurants",
          "Caribbean"
        ],
        "city": "Charlotte",
        "name": "Finga Lickin\' Caribbean Eatery",
        "review_count": 21,
        "stars": 4.5,
        "state": "NC"
      }
    ]
)
testFB.case(
    td.miniYelpLoaded,
    'Beauty & Spas', 'Toronto', 4, 1,
    'results/testFB-mini-Beauty-Toronto.json'
).checkCustom(
    checkJSONFile,
    [
      {
        "address": "123 Queen Street W",
        "categories": [
          "Day Spas",
          "Hair Salons",
          "Beauty & Spas"
        ],
        "city": "Toronto",
        "name": "Fidora Salon and Spa",
        "review_count": 3,
        "stars": 4.0,
        "state": "ON"
      }
    ]
)

testFB.case(
    td.miniYelpLoaded,
    'Restaurants', 'Las Vegas', 2, 1,
    'results/testFB-mini-Restaurants-Toronto-2-1.json'
).checkCustom(
    checkJSONFile,
    [
      {
        "address": "3020 E Desert Inn Rd",
        "categories": [
          "Restaurants",
          "Fast Food",
          "Burgers"
        ],
        "city": "Las Vegas",
        "name": "McDonald's",
        "review_count": 20,
        "stars": 2.0,
        "state": "NV"
      },
      {
        "address": "6889 S Eastern Ave, Ste 101",
        "categories": [
          "Fast Food",
          "Restaurants",
          "Sandwiches"
        ],
        "city": "Las Vegas",
        "name": "Subway",
        "review_count": 6,
        "stars": 2.5,
        "state": "NV"
      },
      {
        "address": "6587 Las Vegas Blvd S, Ste 171",
        "categories": [
          "Arcades",
          "Arts & Entertainment",
          "Gastropubs",
          "Restaurants",
          "American (New)"
        ],
        "city": "Las Vegas",
        "name": "GameWorks",
        "review_count": 349,
        "stars": 3.0,
        "state": "NV"
      },
      {
        "address": "5111 Boulder Hwy",
        "categories": [
          "Sandwiches",
          "Restaurants",
          "Fast Food"
        ],
        "city": "Las Vegas",
        "name": "Subway",
        "review_count": 3,
        "stars": 3.0,
        "state": "NV"
      },
      {
        "address": "333 S Valley View Blvd",
        "categories": [
          "Restaurants",
          "Cafes",
          "American (New)",
          "Bars",
          "Nightlife",
          "Wine Bars"
        ],
        "city": "Las Vegas",
        "name": "Divine Cafe at the Springs Preserve",
        "review_count": 140,
        "stars": 4.0,
        "state": "NV"
      },
      {
        "address": "6730 S Las Vegas Blvd",
        "categories": [
          "Nightlife",
          "Bars",
          "Barbeque",
          "Sports Bars",
          "American (New)",
          "Restaurants"
        ],
        "city": "Las Vegas",
        "name": "Flight Deck Bar & Grill",
        "review_count": 13,
        "stars": 4.0,
        "state": "NV"
      },
      {
        "address": "5006 S Maryland Pkwy, Ste 17",
        "categories": [
          "Karaoke",
          "Bars",
          "Mexican",
          "Restaurants",
          "Nightlife",
          "Dance Clubs"
        ],
        "city": "Las Vegas",
        "name": "Cancun Bar & Grill",
        "review_count": 5,
        "stars": 4.5,
        "state": "NV"
      },
      {
        "address": "8560 Las Vegas Blvd S",
        "categories": [
          "Restaurants",
          "American (Traditional)"
        ],
        "city": "Las Vegas",
        "name": "Geebee's Bar & Grill",
        "review_count": 33,
        "stars": 4.5,
        "state": "NV"
      },
      {
        "address": "9905 S Eastern Ave, Ste 140",
        "categories": [
          "Seafood",
          "Italian",
          "Pizza",
          "Restaurants"
        ],
        "city": "Las Vegas",
        "name": "Trattoria Italia",
        "review_count": 210,
        "stars": 4.5,
        "state": "NV"
      }
    ]
)


testFB.case(
    td.miniYelpLoaded,
    'Restaurants', 'Las Vegas', 4, 30, 
    'results/testFB-Restaurants-LasVegas-4-30.json'
).checkCustom(
    checkJSONFile,
    [
      {
        "address": "333 S Valley View Blvd",
        "categories": [
          "Restaurants",
          "Cafes",
          "American (New)",
          "Bars",
          "Nightlife",
          "Wine Bars"
        ],
        "city": "Las Vegas",
        "name": "Divine Cafe at the Springs Preserve",
        "review_count": 140,
        "stars": 4.0,
        "state": "NV"
      },
      {
        "address": "8560 Las Vegas Blvd S",
        "categories": [
          "Restaurants",
          "American (Traditional)"
        ],
        "city": "Las Vegas",
        "name": "Geebee's Bar & Grill",
        "review_count": 33,
        "stars": 4.5,
        "state": "NV"
      },
      {
        "address": "9905 S Eastern Ave, Ste 140",
        "categories": [
          "Seafood",
          "Italian",
          "Pizza",
          "Restaurants"
        ],
        "city": "Las Vegas",
        "name": "Trattoria Italia",
        "review_count": 210,
        "stars": 4.5,
        "state": "NV"
      }
    ]
)

testFC = optimism.testFunctionMaybe(yelp, "findCategories")
testFC.case(td.soloYelpLoaded, 1).checkReturnValue(
    {
        "Italian": 1,
        "Restaurants": 1,
        "Pizza": 1
    }
)
testFC.case(td.microYelpLoaded, 4).checkReturnValue({"Restaurants": 5})
testFC.case(td.microYelpLoaded, 2).checkReturnValue(
    {
        'Fitness & Instruction': 2,
        'Active Life': 2,
        'Restaurants': 5,
        'Beauty & Spas': 3,
        'Home Services': 2
    }
)
testFC.case(td.miniYelpLoaded, 50).checkReturnValue(
    {
        "Restaurants": 106,
        "Shopping": 50
    }
)

testBPP = optimism.testFunctionMaybe(yelp, "bestPizzaPlace")
testBPP.case(td.soloYelpLoaded).checkReturnValue(
    [
        {
            'state': 'OH',
            'address': '547 Sackett Ave',
            'review_count': 29,
            'stars': 3.5,
            'name': "Retz's Laconi's II",
            'city': 'Cuyahoga Falls',
            'categories': ['Italian', 'Restaurants', 'Pizza']
        }
    ]
)
testBPP.case(td.pizzaYelpLoaded).checkReturnValue(
    [
        {
            "state": "AZ",
            "address": "15557 West Bell Road",
            "review_count": 30,
            "stars": 4.0,
            "name": "Papa Murphy's",
            "city": "Surprise",
            "categories": ["Restaurants", "Pizza"]
        }
    ]
)
testBPP.case(td.microYelpLoaded).checkReturnValue(
    [
        {
            'state': 'OH',
            'address': '547 Sackett Ave',
            'review_count': 29,
            'stars': 3.5,
            'name': "Retz's Laconi's II",
            'city': 'Cuyahoga Falls',
            'categories': ['Italian', 'Restaurants', 'Pizza']
        }
    ]
)
testBPP.case(td.miniYelpLoaded).checkReturnValue(
    [
        {
            'state': 'AZ',
            'address': '',
            'review_count': 4,
            'stars': 5.0,
            'name': "Caviness Studio",
            'city': 'Phoenix',
            'categories': [
                "Marketing", "Men's Clothing", "Restaurants",
                "Graphic Design", "Women's Clothing", "Screen Printing",
                "Advertising", "Pizza", "Shopping", "Web Design", "Fashion",
                "Local Services", "Screen Printing/T-Shirt Printing",
                "Professional Services"
            ]
        }
    ]
)
