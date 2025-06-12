# Name
predict rainfall

# Goal
Your goal is to predict rainfall for each day of the year

# Evaluation
Submissions are evaluated on area under the ROC curve between the predicted probability and the observed target.

# Submission File
For each id in the test set, you must predict a probability for the target rainfall. The file should contain a header and have the following format:

```
id,rainfall
2190,0.5
2191,0.1
2192,0.9
etc.
```

# Metadata
 - id: int
 - day: int
 - pressure: float
 - maxtemp: float
 - temparature: float
 - mintemp: float
 - dewpoint: float
 - humidity: int
 - cloud: int
 - sunshine: float
 - winddirection:float
 - windspeed: int
 - rainfall: int, target variable