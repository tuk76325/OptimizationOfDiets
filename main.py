import pulp
from pulp import *
from collections import defaultdict
import pandas as pd
from six import binary_type

df = pd.read_excel("diet.xls", header = 0) # read all data

minReqs1 = df.loc[65].dropna().to_dict()
maxReqs1 = df.loc[66].dropna().to_dict()

minReqs = defaultdict(float)
maxReqs = defaultdict(float)

for key in minReqs1:
    if key=="Serving Size":
        continue
    else:
        minReqs[key] = minReqs1[key]
        maxReqs[key] = maxReqs1[key]


df = df.dropna()
lstData = df.values.tolist()

lstOfDicts = []
for i in range(len(df)):
    lstOfDicts.append(df.loc[i].to_dict())

lstOfFoodNames = []
for food in lstOfDicts:
    lstOfFoodNames.append(food["Foods"])

costPerFood = defaultdict(float)
for food in lstOfDicts:
    costPerFood[food['Foods']] = food['Price/ Serving']

nutrientsPerFood = []
for i in range(len(list(df.columns))-2):
        nutrientsPerFood.append(dict([(j[0], float(j[i+2])) for j in lstData])) #makes dict of each nutrient value to key of food

costPerFood = list(costPerFood.values())

prob = LpProblem("dietOptimization", LpMinimize) #minimize bc lowest cost

#DECISION VARIABLE
foodVars = LpVariable.dicts('foods', lstOfFoodNames, 0, cat="Continuous")
chosenFoodVars = LpVariable.dicts("chosen",lstOfFoodNames,lowBound=0, upBound=1, cat="Binary")


#OBJECTIVE FUNCTION
prob += lpSum([costPerFood[i] * foodVars[lstOfFoodNames[i]] for i in range(len(foodVars))]), "Total Cost"

#CONSTRAINTS
indexOfNutrients = 1 # 1=not including serving size
for newKey in minReqs:
    prob += lpSum([nutrientsPerFood[indexOfNutrients][lstOfFoodNames[i]] * foodVars[lstOfFoodNames[i]] for i in range(len(foodVars))]) >= minReqs[newKey]
    prob += lpSum([nutrientsPerFood[indexOfNutrients][lstOfFoodNames[i]] * foodVars[lstOfFoodNames[i]] for i in range(len(foodVars))]) <= maxReqs[newKey]
    indexOfNutrients+=1

#account for serving size and part b
for f in lstOfFoodNames:
    prob += foodVars[f] <= 1000000 * chosenFoodVars[f] #determines if chosen by seeing if chosen is 1 or 0
    prob += foodVars[f] >= .1 * chosenFoodVars[f] #seeing if servings size >= 0.1

#frozen broccoli or celery but not both
prob += chosenFoodVars['Frozen Broccoli'] + chosenFoodVars['Celery, Raw'] <= 1

#Protein, each of these must equal three so since binary only three can be selected at a time
prob += chosenFoodVars['Roasted Chicken'] + chosenFoodVars['Poached Eggs'] + chosenFoodVars['Scrambled Eggs'] + chosenFoodVars['Frankfurter, Beef'] + \
  chosenFoodVars['Kielbasa,Prk'] + chosenFoodVars['Hamburger W/Toppings'] + chosenFoodVars['Hotdog, Plain'] + chosenFoodVars['Pork'] + \
  chosenFoodVars['Bologna,Turkey'] + chosenFoodVars['Ham,Sliced,Extralean'] + chosenFoodVars['White Tuna in Water']  >= 3

#SOLVE
prob.solve()
print("Status: ", LpStatus[prob.status])
for v in prob.variables():
    if v.varValue > 0:
        if str(v).find("chosen"):
            print(f"Optimal Quantity of {v.name}: ", v.varValue)
print('Minimum Cost: ', pulp.value(prob.objective))

