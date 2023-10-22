import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics

class RecEngine:
    
    regressor = None

    def __init__(self):
        self.buildModel()
        
    def buildModel(self):
        basedir = os.path.abspath(os.path.dirname(__file__))

        # Specify the file path
        file_path = basedir + "/../static/data/MLData.csv"

        dataset = pd.read_csv(file_path, header=0)
        array = dataset.values

        x = array[:, 0:2]
        y = array[:, 2]

        X_Train, X_Test, Y_Train, Y_Test = train_test_split(x, y, test_size=0.2, random_state=0)

        # Using ElasticNet regression model
        # alpha is the penalty parameter and l1_ratio defines the balance between L1 and L2 regularizations
        self.regressor = LinearRegression()
        self.regressor.fit(X_Train, Y_Train)

        Y_Prediction = self.regressor.predict(X_Test)

        df = pd.DataFrame({'Actual' : Y_Test, 'Predicted': Y_Prediction})

        print(df)

        mae = metrics.mean_absolute_error(Y_Test, Y_Prediction)
        r2 = metrics.r2_score(Y_Test, Y_Prediction)

        print("The model performance for testing set")
        print("-------------------------------------")
        print('MAE is {}'.format(mae))
        print('R2 score is {}'.format(r2))

    def predict(self, gpa, sat):
        prediction = self.regressor.predict([[gpa, sat]])
        return prediction[0]


model = RecEngine()
prediction = model.predict(3.9, 1580)
print(f"The predicted value is {prediction}")


"""Y_Prediction = regressor.predict(X_Test)

df = pd.DataFrame({'Actual' : Y_Test, 'Predicted': Y_Prediction})

print(df)

mae = metrics.mean_absolute_error(Y_Test, Y_Prediction)
r2 = metrics.r2_score(Y_Test, Y_Prediction)

print("The model performance for testing set")
print("-------------------------------------")
print('MAE is {}'.format(mae))
print('R2 score is {}'.format(r2))
"""