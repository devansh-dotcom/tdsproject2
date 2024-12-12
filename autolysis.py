import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests

# Set up AI Proxy Token
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")

# Load the dataset
def load_data(file):
    return pd.read_csv(file, encoding='ISO-8859-1')

# Generate summary statistics
def analyze_data(df):
    summary = df.describe()
    missing_values = df.isnull().sum()
    return summary, missing_values

# Create visualizations
def create_visualizations(df):
    # Boxplot of 'Life Ladder' across countries
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Country name', y='Life Ladder', data=df)
    plt.xticks(rotation=90)
    plt.title('Distribution of Life Ladder across Countries')
    plt.tight_layout()
    plt.savefig('life_ladder_distribution.png')

    # Exclude non-numeric columns for correlation calculation
    numeric_df = df.select_dtypes(include=['float64', 'int64'])  # Only numeric columns

    # Correlation heatmap
    corr_matrix = numeric_df.corr()  # Calculate correlation only for numeric columns
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation Matrix of Numerical Features')
    plt.tight_layout()
    plt.savefig('correlation_matrix.png')

    # Missing data bar chart
    missing_data = df.isnull().sum()
    plt.figure(figsize=(10, 6))
    missing_data.plot(kind='bar', color='lightblue')
    plt.title('Missing Data in Each Column')
    plt.ylabel('Number of Missing Values')
    plt.tight_layout()
    plt.savefig('missing_data.png')

# Request further AI insights
def request_ai_analysis(df):
    url = "https://aiproxy.sanand.workers.dev"
    headers = {"Authorization": f"Bearer {AIPROXY_TOKEN}"}
    data = {"file": df.to_json()}
    response = requests.post(url, headers=headers, data=data)
    return response.json()

# Main function to run the script
def main(file):
    # Load the data
    df = load_data(file)

    # Perform analysis
    summary, missing_values = analyze_data(df)
    print("Summary Statistics:\n", summary)
    print("\nMissing Values:\n", missing_values)

    # Create visualizations
    create_visualizations(df)

    # Request AI insights
    ai_analysis = request_ai_analysis(df)
    print("\nAI Analysis Response:\n", ai_analysis)

if __name__ == "__main__":
    file = "happiness.csv"  # Update this with your actual dataset path
    main(file)
