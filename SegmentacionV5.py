import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import os

# Load the customer data from the CSV file
customer_data = pd.read_csv('customer_data.csv')

# Create Dash app
app = dash.Dash(__name__)
server = app.server

# New graphs
gender_purchase_frequency = customer_data.groupby('Gender')['Purchase_Frequency'].mean().reset_index()
gender_purchase_frequency_fig = px.bar(gender_purchase_frequency, x='Gender', y='Purchase_Frequency', title='Average Purchase Frequency by Gender', color='Gender')

purchase_amount_by_category_fig = px.box(customer_data, x='Product_Category', y='Purchase_Amount', title='Purchase Amount by Product Category', color='Product_Category')

age_vs_purchase_amount_fig = px.scatter(customer_data, x='Age', y='Purchase_Amount', color='Location', title='Age vs. Purchase Amount by Location')

# Purchase Frequency Distribution updated code
purchase_frequency_counts = customer_data['Purchase_Frequency'].value_counts().reset_index()
purchase_frequency_counts.columns = ['Purchase_Frequency', 'Count']
purchase_frequency_fig = px.bar(purchase_frequency_counts, x='Purchase_Frequency', y='Count', title='Purchase Frequency Distribution', color='Purchase_Frequency', color_continuous_scale=px.colors.sequential.Blues)

# Define the layout of the dashboard
app.layout = html.Div([
    html.Div([
        html.Img(src='assets/logo.png', height=50, width=50),
        html.H1("Customer Data Dashboard", style={'display': 'inline', 'marginLeft': '10px'}),
    ]),
    html.Div([
        html.Div([
            dcc.Graph(
                id='age_hist',
                figure=px.histogram(customer_data, x='Age', nbins=20, title='Age Distribution', color='Gender')
            ),
            dcc.Textarea(id='age_hist_comments', placeholder='Comentarios', style={'width': '100%', 'height': '50px'}),
            dcc.Graph(
                id='purchase_frequency_hist',
                figure=purchase_frequency_fig
            ),
            dcc.Textarea(id='purchase_frequency_hist_comments', placeholder='Comentarios', style={'width': '100%', 'height': '50px'}),
        ], className="six columns"),
        html.Div([
            dcc.Graph(
                id='gender_count',
                figure=px.bar(customer_data['Gender'].value_counts().reset_index(), x='index', y='Gender', title='Gender Distribution', color='index', labels={'index': 'Gender', 'Gender': 'Count'})
            ),
            dcc.Textarea(id='gender_count_comments', placeholder='Comentarios', style={'width': '100%', 'height': '50px'}),
            dcc.Graph(
                id='location_count',
                figure=px.bar(customer_data['Location'].value_counts().reset_index(), x='index', y='Location', title='Location Distribution', color='index', labels={'index': 'Location', 'Location': 'Count'})
            ),
            dcc.Textarea(id='location_count_comments', placeholder='Comentarios', style={'width': '100%', 'height': '50px'}),
        ], className="six columns"),
    ], className="row"),
    html.Div([
        html.Div([
            dcc.Graph(
                id='product_category_count',
                figure=px.bar(customer_data['Product_Category'].value_counts().reset_index(), x='index', y='Product_Category', title='Product Category Distribution', color='index', labels={'index': 'Product Category', 'Product_Category': 'Count'})
            ),
            dcc.Textarea(id='product_category_count_comments', placeholder='Comentarios', style={'width': '100%', 'height': '50px'}),
            dcc.Graph(
                id='gender_purchase_frequency',
                figure=gender_purchase_frequency_fig
            ),
            dcc.Textarea(id='gender_purchase_frequency_comments', placeholder='Comentarios', style={'width': '100%', 'height': '50px'}),
        ], className="six columns"),
        html.Div([
            dcc.Graph(
                id='purchase_amount_by_category',
                figure=purchase_amount_by_category_fig
            ),
            dcc.Textarea(id='purchase_amount_by_category_comments', placeholder='Comentarios', style={'width': '100%', 'height': '50px'}),
            dcc.Graph(
                id='age_vs_purchase_amount',
                figure=age_vs_purchase_amount_fig
            ),
            dcc.Textarea(id='age_vs_purchase_amount_comments', placeholder='Comentarios', style={'width': '100%', 'height': '50px'}),
        ], className="six columns"),
    ], className="row"),
])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run_server(debug=True, host='0.0.0.0', port=8050)




