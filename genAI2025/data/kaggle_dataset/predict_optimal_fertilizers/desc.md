# Name
predict optimal fertilizers

# Goal
Your objective is to select the best fertilizer for different weather, soil conditions and crops.

# Evaluation

Submissions are evaluated according to the Mean Average Precision @ 3 (MAP@3):

MAP@5=\frac{1}{U}\sum_{u=1}^{U}\sum_{k=1}^{min(n,5)}P(k)\times rel(k)

where 
U is the number of observations, P(k)is the precision at cutoff k, n is the number predictions per observation, and rel(k) is an indicator function equaling 1 if the item at rank k is a relevant (correct) label, zero otherwise.

Once a correct label has been scored for an observation, that label is no longer considered relevant for that observation, and additional predictions of that label are skipped in the calculation. For example, if the correct label is A for an observation, the following predictions all score an average precision of 1.0.

[A, B, C, D, E]
[A, A, A, A, A]
[A, B, A, C, A]


# Submission File
For each id in the test set, you may predict up to 3 Fertilizer Name values, with the predictions space delimited. The file should contain a header and have the following format:

```
id,Fertilizer Name 
750000,14-35-14 10-26-26 Urea
750000,14-35-14 10-26-26 Urea 
etc
```

# metadata
 - id: int
 - Temparature: int
 - Humidity: int
 - Moisture: int
 - Soil Type: string
 - Crop Type: string
 - Nitrogen: int
 - Potassium: int
 - Phosphorous: int
 - Fertilizer Name: string, target variable