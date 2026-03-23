import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load the processed data
df = pd.read_csv('formatted_data.csv')

# Convert date to datetime and sort
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    # Header
    html.H1("Pink Morsel Sales Analysis", 
            style={
                'textAlign': 'center', 
                'color': '#FF69B4',
                'fontSize': '36px',
                'marginBottom': '30px',
                'marginTop': '20px'
            }),
    
    # Region selector
    html.Div([
        html.Label("Select Region:", 
                   style={'fontSize': '18px', 'fontWeight': 'bold'}),
        dcc.RadioItems(
            id='region-selector',
            options=[
                {'label': 'All Regions', 'value': 'all'},
                {'label': 'North', 'value': 'north'},
                {'label': 'South', 'value': 'south'},
                {'label': 'East', 'value': 'east'},
                {'label': 'West', 'value': 'west'}
            ],
            value='all',
            style={'marginTop': '10px', 'marginBottom': '20px'}
        )
    ], style={'textAlign': 'center', 'marginBottom': '30px'}),
    
    # Line chart
    dcc.Graph(id='sales-chart'),
    
    # Add a note about the price increase
    html.Div([
        html.P("Note: Pink Morsel price increased from $3.00 to $4.50 on January 15, 2021",
               style={'textAlign': 'center', 'color': 'gray', 'fontStyle': 'italic'})
    ])
])

# Define callback to update chart based on region selection
@app.callback(
    Output('sales-chart', 'figure'),
    Input('region-selector', 'value')
)
def update_chart(selected_region):
    # Filter data based on region selection
    if selected_region == 'all':
        filtered_df = df
        title = "Pink Morsel Sales - All Regions"
    else:
        filtered_df = df[df['region'] == selected_region]
        title = f"Pink Morsel Sales - {selected_region.title()} Region"
    
    # Group by date to sum sales if multiple regions selected
    if selected_region == 'all':
        daily_sales = filtered_df.groupby('date')['sales'].sum().reset_index()
    else:
        daily_sales = filtered_df[['date', 'sales']].copy()
    
    # Create the line chart
    fig = px.line(
        daily_sales, 
        x='date', 
        y='sales',
        title=title,
        labels={
            'date': 'Date',
            'sales': 'Total Sales ($)'
        }
    )
    
    # Add a vertical line for the price increase date
    fig.add_vline(
        x='2021-01-15', 
        line_dash="dash", 
        line_color="red",
        annotation_text="Price Increase",
        annotation_position="top"
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Total Sales ($)",
        hovermode='x unified',
        template='plotly_white'
    )
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)