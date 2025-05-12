import joblib
model = joblib.load('random_forest_co2_model.pkl')
print(model.predict([[180, 175, 170]]))  # Use actual lagged valuespython