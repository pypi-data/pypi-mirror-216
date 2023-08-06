This is a simple Python package that aims to make using linear regression easier for programmers. For now, it only provides a simple linear regresion calculation that is based on one independent variable.

You can create a linear regression model as following:
```
from regrez import Model
m = Model("path/to/csv", "label for column that'll be used for x axis", "label for column that'll be used for y axis")
```
After that, you can train your model using m.Train() and test using m.Test(list_that_will_be_used_for_testing). Alternatively, there is a function called m.TrainAndTest() if you only want to see how good would the model work. It separates 20% of the data for testing, trains the model with the rest of it, tests the model with separated data and shows how accurate your model is. Finally, you can use m.Visualize() after training if you want to see a plot showing both data points and the line to see how relative your variables are.