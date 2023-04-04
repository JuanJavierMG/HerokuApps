import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import MiniBatchKMeans
from sklearn.metrics import silhouette_score

# Load the customer data from the CSV file
customer_data = pd.read_csv('customer_data.csv')

# Create a copy of the DataFrame for visualizations before encoding
customer_data_visualization = customer_data.copy()

# Display the first few rows of the DataFrame
print(customer_data.head())

# Check for missing data
print("\nMissing data summary:\n", customer_data.isnull().sum())

#Describe Data
print(customer_data.describe())

# Fill missing values with appropriate methods (mean, median, mode, etc.)
#customer_data['column_name'].fillna(customer_data['column_name'].mean(), inplace=True)

# Encode categorical features, such as gender
customer_data = pd.get_dummies(customer_data, columns=['Gender', 'Product_Category', 'Location'], drop_first=True)

# Standardize the numeric features, if necessary
scaler = StandardScaler()
customer_data[['Age', 'Purchase_Frequency', 'Purchase_Amount']] = scaler.fit_transform(customer_data[['Age', 'Purchase_Frequency', 'Purchase_Amount']])

# Visualize the distribution of numerical variables
numerical_vars = ['Age', 'Purchase_Frequency', 'Purchase_Amount']

for var in numerical_vars:
    plt.figure()
    sns.histplot(data=customer_data_visualization, x=var, kde=True)
    plt.title(f"Distribution of {var}")

# Visualize the distribution of categorical variables
categorical_vars = ['Gender', 'Product_Category', 'Location']

for var in categorical_vars:
    plt.figure()
    sns.countplot(data=customer_data_visualization, x=var)
    plt.title(f"Distribution of {var}")

# Pairplot for visualizing relationships between numerical variables
sns.pairplot(customer_data_visualization, hue='Gender', markers=["o", "s"], diag_kind='hist')
plt.show()

#Adicional
sns.catplot(data=customer_data_visualization, x='Product_Category', hue='Location', kind='count')
plt.title("Relationship between Product Category and Location")
plt.show()

# Compute the correlation matrix
correlation_matrix = customer_data_visualization.corr(numeric_only=True)
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.show()

# Define the target variable (e.g., 'Purchase_Frequency')
y = customer_data['Purchase_Frequency']
X = customer_data.drop('Purchase_Frequency', axis=1)

# Fit the random forest model
rf = RandomForestRegressor()
rf.fit(X, y)

# Get R-squared for the random forest model
r_squared = rf.score(X, y)
print("R-squared value for the Random Forest model:", r_squared)

# Get feature importances
importances = rf.feature_importances_
feature_importances = pd.DataFrame({'feature': X.columns, 'importance': importances}).sort_values(by='importance', ascending=False)

# Select the top k features
k = 5
selected_features = feature_importances['feature'].head(k).tolist()

print("\nSelected features for clustering or further analysis:\n", selected_features)

# Identify potential outliers using the IQR method
Q1 = customer_data.quantile(0.25)
Q3 = customer_data.quantile(0.75)
IQR = Q3 - Q1

outliers = ((customer_data < (Q1 - 1.5 * IQR)) | (customer_data > (Q3 + 1.5 * IQR))).any(axis=1)
print("Number of potential outliers:", outliers.sum())

# Remove outliers or keep them based on the context of the project
customer_data_no_outliers = customer_data[~outliers]

# Model selection and implementation
X = customer_data_no_outliers[selected_features]

# Determine the optimal number of clusters using the elbow method and silhouette analysis
wcss = []
silhouette_scores = []
max_clusters = 10

for i in range(2, max_clusters + 1):
    kmeans = MiniBatchKMeans(n_clusters=i, random_state=42, n_init=10)
    kmeans.fit(X)

    # Calculate within-cluster sum of squares (WCSS)
    wcss.append(kmeans.inertia_)

    # Calculate silhouette score
    silhouette_scores.append(silhouette_score(X, kmeans.labels_))

# Plot the elbow method graph
plt.figure()
plt.plot(range(2, max_clusters + 1), wcss, marker='o')
plt.xlabel("Number of clusters")
plt.ylabel("WCSS")
plt.title("Elbow Method")
plt.show()

# Plot the silhouette analysis graph
plt.figure()
plt.plot(range(2, max_clusters + 1), silhouette_scores, marker='o')
plt.xlabel("Number of clusters")
plt.ylabel("Silhouette Score")
plt.title("Silhouette Analysis")
plt.show()

# Choose the optimal number of clusters based on the project objectives and data characteristics
optimal_clusters = 5  # Replace this value with the optimal number of clusters from the elbow method or silhouette analysis

# Apply the clustering algorithm
kmeans = MiniBatchKMeans(n_clusters=optimal_clusters, random_state=42, n_init=10)
kmeans.fit(X)

# Add the cluster labels to the original data
customer_data_no_outliers['Cluster'] = kmeans.labels_

# Visualize the clusters
plt.figure()
sns.scatterplot(data=customer_data_no_outliers, x='Purchase_Amount', y='Age', hue='Cluster', palette='viridis', style='Gender_M')
plt.xlabel("Purchase Amount")
plt.ylabel("Age")
plt.title("Clusters")
plt.show()

