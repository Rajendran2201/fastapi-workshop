from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.ensemble import RandomForestClassifier
import joblib
import pandas as pd

# load the data 
iris_data = load_iris()
X = pd.DataFrame(iris_data.data, columns=iris_data.feature_names)
y = iris_data.target

# split the data 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# train a simple model 
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

y_pred = model.predict(X_test)

# evaluate the model 
accuracy = accuracy_score(y_test, y_pred)
print(f"Test accuracy: {accuracy}")

# save the model 
joblib.dump(model, "model.pkl")
joblib.dump(iris_data.feature_names, "feature_names.pkl")
joblib.dump(iris_data.target_names.tolist(), "class_names.pkl")

# print statements to ensure the process is complete
print("\nModel and feature names are saved!")
