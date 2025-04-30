import sys
import joblib
import numpy as np
import pandas as pd

# Load the trained model and encoders
model = joblib.load('C:/Users/Admin/Crime prediction/ml model/crime_modelGB.pkl')
blockcode_encoder = joblib.load('C:/Users/Admin/Crime prediction/ml model/blockcode.pkl')
locationcode_encoder = joblib.load('C:/Users/Admin/Crime prediction/ml model/locationcode.pkl')

# Inputs
latitude = float(sys.argv[1])
longitude = float(sys.argv[2])
hour = int(sys.argv[3])
dayOfWeek = int(sys.argv[4])
month = int(sys.argv[5])
blockCode = str(sys.argv[6])
locationCode = str(sys.argv[7])

# Convert blockCode to list before encoding
encoded_block = blockcode_encoder.transform([blockCode])[0]  # Encode blockCode
encoded_location = locationcode_encoder.transform([locationCode])[0]  # Encode locationCode

# Create input feature array

input_features = pd.DataFrame([[
    latitude, longitude, hour, dayOfWeek, month, encoded_block, encoded_location
]], columns=['LATITUDE', 'LONGITUDE', 'HOUR', 'DAYOFWEEK', 'MONTH', 'BLOCK CODE', 'LOCATION CODE'])

# Prediction
prediction = model.predict(input_features)[0]



# Output the prediction
print(f"Prediction: {prediction}")


