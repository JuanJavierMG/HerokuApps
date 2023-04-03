import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Load the customer data from the CSV file
customer_data = pd.read_csv('customer_data.csv')

# Create Dash app
app = dash.Dash(__name__)

# New graphs
gender_purchase_frequency = customer_data.groupby('Gender')['Purchase_Frequency'].mean().reset_index()
gender_purchase_frequency_fig = px.bar(gender_purchase_frequency, x='Gender', y='Purchase_Frequency', title='Average Purchase Frequency by Gender')

purchase_amount_by_category_fig = px.box(customer_data, x='Product_Category', y='Purchase_Amount', title='Purchase Amount by Product Category')

age_vs_purchase_amount_fig = px.scatter(customer_data, x='Age', y='Purchase_Amount', color='Location', title='Age vs. Purchase Amount by Location')

# Define the layout of the dashboard
app.layout = html.Div([
    html.Div([
        html.Img(src='assets/company_logo.png', height=50, width=50),
        html.H1("Customer Data Dashboard", style={'display': 'inline', 'marginLeft': '10px'}),
    ]),
    html.Div([
        html.Div([
            dcc.Graph(
                id='age_hist',
                figure=px.histogram(customer_data, x='Age', nbins=20, title='Age Distribution')
            ),
            dcc.Graph(
                id='purchase_frequency_hist',
                figure=px.histogram(customer_data, x='Purchase_Frequency', nbins=10, title='Purchase Frequency Distribution')
            ),
        ], className="six columns"),
        html.Div([
            dcc.Graph(
                id='gender_count',
                figure=px.bar(customer_data['Gender'].value_counts().reset_index(), x='index', y='Gender', title='Gender Distribution')
            ),
            dcc.Graph(
                id='location_count',
                figure=px.bar(customer_data['Location'].value_counts().reset_index(), x='index', y='Location', title='Location Distribution')
            ),
        ], className="six columns"),
    ], className="row"),
    html.Div([
        html.Div([
            dcc.Graph(
                id='product_category_count',
                figure=px.bar(customer_data['Product_Category'].value_counts().reset_index(), x='index', y='Product_Category', title='Product Category Distribution')
            ),
            dcc.Graph(
                id='gender_purchase_frequency',
                figure=gender_purchase_frequency_fig
            ),
        ], className="six columns"),
        html.Div([
            dcc.Graph(
                id='purchase_amount_by_category',
                figure=purchase_amount_by_category_fig
            ),
            dcc.Graph(
                id='age_vs_purchase_amount',
                figure=age_vs_purchase_amount_fig
            ),
        ], className="six columns"),
    ], className="row"),
])

if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8050)
