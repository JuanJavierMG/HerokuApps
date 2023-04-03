import pandas as pd
import numpy as np

# Set a random seed for reproducibility
np.random.seed(42)

# Define the number of customers
num_customers = 10000

# Generate random customer data
ages = np.random.randint(18, 75, size=num_customers)
genders = np.random.choice(['M', 'F'], size=num_customers)
purchase_frequencies = np.random.randint(1, 12, size=num_customers)
purchase_amounts = np.random.randint(10, 500, size=num_customers)
product_categories = np.random.choice(['Electronics', 'Fashion', 'Home & Kitchen', 'Sports & Outdoors'], size=num_customers)
locations = np.random.choice(['North', 'South', 'East', 'West'], size=num_customers)

# Create a pandas DataFrame
customer_data = pd.DataFrame({
    'Age': ages,
    'Gender': genders,
    'Purchase_Frequency': purchase_frequencies,
    'Purchase_Amount': purchase_amounts,
    'Product_Category': product_categories,
    'Location': locations
})

# Save the DataFrame to a CSV file
customer_data.to_csv('C:/Users/JJMARTINEZ/Segmentación/customer_data.csv', index=False)

# Display the first few rows of the DataFrame
print(customer_data.head())
