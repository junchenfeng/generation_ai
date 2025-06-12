# Name
predict calorie expenditure

#Goal:
Your goal is to predict how many calories were burned during a workout.

# Evaluation
The evaluation metric for this competition is Root Mean Squared Logarithmic Error.

# Submission File
For each id row in the test set, you must predict the continuous target, Calories. The file should contain a header and have the following format:
```
id,Calories
750000,93.2
750001,27.42
750002,103.8
etc.
```

# Metadata
 - id: int
 - Sex: string
 - Age: int
 - Height:  int
 - Weight: int
 - Duration: init
 - Heart_Rate: int
 - Body_Temp: float
 - Calories: int, target variable


