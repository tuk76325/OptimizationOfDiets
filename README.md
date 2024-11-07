# OptimizationOfDiets
This program was written based on data from the famous large scale diet optimization problem that the US military used to minimize costs.
  
  The diet problem is one of the first large-scale optimization problems to be studied in practice. Back in the 1930’s and 40’s, 
the Army wanted to meet the nutritional requirements of its soldiers while minimizing the cost. The data is given in the file diet.xls.

  1. Formulated an optimization model (a linear program) to find the cheapest diet that satisfies the
maximum and minimum daily nutrition constraints, and solved it using PuLP.

  2. Added the following constraints and solve the new model:
    a. If a food is selected, then a minimum of 1/10 serving must be chosen.
    b. Many people dislike celery and frozen broccoli. So at most one, but not both, can be selected.
    c. To get day-to-day variety in protein, at least 3 kinds of meat/poultry/fish/eggs must be selected. 
