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

# Custom CSS styles
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Pink Morsel Sales Dashboard</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            
            .header {
                background: linear-gradient(135deg, #ff6b6b 0%, #ff8e8e 100%);
                padding: 30px;
                text-align: center;
                border-radius: 0 0 20px 20px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                margin-bottom: 40px;
            }
            
            .header h1 {
                margin: 0;
                color: white;
                font-size: 48px;
                font-weight: bold;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            }
            
            .header p {
                margin: 10px 0 0 0;
                color: rgba(255,255,255,0.9);
                font-size: 18px;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            
            .card {
                background: white;
                border-radius: 20px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                margin-bottom: 30px;
            }
            
            .region-selector {
                text-align: center;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 15px;
                margin-bottom: 30px;
            }
            
            .region-selector label {
                font-size: 18px;
                font-weight: 600;
                color: #333;
                margin-right: 20px;
            }
            
            .radio-group {
                display: inline-flex;
                gap: 15px;
                flex-wrap: wrap;
                justify-content: center;
            }
            
            .radio-option {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 8px 16px;
                background: white;
                border-radius: 25px;
                cursor: pointer;
                transition: all 0.3s ease;
                border: 2px solid #e0e0e0;
            }
            
            .radio-option:hover {
                border-color: #ff6b6b;
                transform: translateY(-2px);
            }
            
            .radio-option input[type="radio"] {
                cursor: pointer;
                accent-color: #ff6b6b;
            }
            
            .radio-option label {
                cursor: pointer;
                margin: 0;
                font-weight: 500;
            }
            
            .stats {
                display: flex;
                justify-content: space-around;
                margin-top: 20px;
                flex-wrap: wrap;
                gap: 20px;
            }
            
            .stat-card {
                flex: 1;
                min-width: 150px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                transition: transform 0.3s ease;
            }
            
            .stat-card:hover {
                transform: translateY(-5px);
            }
            
            .stat-card h3 {
                margin: 0 0 10px 0;
                font-size: 14px;
                opacity: 0.9;
            }
            
            .stat-card p {
                margin: 0;
                font-size: 28px;
                font-weight: bold;
            }
            
            .note {
                text-align: center;
                padding: 15px;
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                border-radius: 10px;
                color: #856404;
                margin-top: 20px;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .card {
                animation: fadeIn 0.6s ease-out;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Define the layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("🌸 Pink Morsel Sales Dashboard 🌸"),
        html.P("Interactive Sales Analysis | Filter by Region")
    ], className="header", id="header"),
    
    # Main container
    html.Div([
        # Region selector card
        html.Div([
            html.H3("📊 Filter by Region", style={'textAlign': 'center', 'marginBottom': '20px', 'color': '#333'}),
            html.Div([
                dcc.RadioItems(
                    id='region-selector',
                    options=[
                        {'label': '🌍 All Regions', 'value': 'all'},
                        {'label': '⬆️ North', 'value': 'north'},
                        {'label': '⬇️ South', 'value': 'south'},
                        {'label': '➡️ East', 'value': 'east'},
                        {'label': '⬅️ West', 'value': 'west'}
                    ],
                    value='all',
                    inline=True,
                    className="radio-group",
                    labelClassName="radio-option",
                    inputClassName="radio-input"
                )
            ], style={'textAlign': 'center'})
        ], className="region-selector"),
        
        # Chart card
        html.Div([
            dcc.Graph(id='sales-chart', config={'displayModeBar': True})
        ], className="card"),
        
        # Stats cards (will be updated by callback)
        html.Div(id='stats-cards', className="stats"),
        
        # Note
        html.Div([
            html.P("💡 Tip: Click on regions above to filter sales data. Hover over the chart to see detailed values.", 
                   style={'margin': 0}),
            html.P("📈 The vertical line marks the price increase date (January 15, 2021)", 
                   style={'margin': '10px 0 0 0', 'fontSize': '12px'})
        ], className="note")
        
    ], className="container")
])

# Callback to update chart
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
    
    # Group by date for all regions
    if selected_region == 'all':
        daily_sales = filtered_df.groupby('date')['sales'].sum().reset_index()
    else:
        daily_sales = filtered_df[['date', 'sales']].copy()
    
    # Create the line chart with enhanced styling
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
    
    # Add vertical line for price increase (if data includes 2021)
    if daily_sales['date'].max() >= pd.to_datetime('2021-01-15'):
        fig.add_vline(
            x='2021-01-15', 
            line_dash="dash", 
            line_color="red",
            line_width=2,
            annotation_text="💰 Price Increase",
            annotation_position="top",
            annotation_font_size=12
        )
    
    # Update layout with modern styling
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Total Sales ($)",
        hovermode='x unified',
        template='plotly_white',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Segoe UI", size=12),
        title_font=dict(size=24, color='#333', family="Segoe UI"),
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(0,0,0,0.1)',
            showline=True,
            linewidth=2,
            linecolor='#e0e0e0'
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(0,0,0,0.1)',
            showline=True,
            linewidth=2,
            linecolor='#e0e0e0'
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Segoe UI"
        )
    )
    
    # Add range slider for better navigation
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    
    return fig

# Callback to update stats cards
@app.callback(
    Output('stats-cards', 'children'),
    Input('region-selector', 'value')
)
def update_stats(selected_region):
    # Filter data
    if selected_region == 'all':
        filtered_df = df
    else:
        filtered_df = df[df['region'] == selected_region]
    
    # Calculate statistics
    total_sales = filtered_df['sales'].sum()
    avg_daily_sales = filtered_df['sales'].mean()
    max_sales = filtered_df['sales'].max()
    max_date = filtered_df.loc[filtered_df['sales'].idxmax(), 'date'].strftime('%Y-%m-%d')
    
    # Create stats cards
    return [
        html.Div([
            html.H3("💰 Total Sales"),
            html.P(f"${total_sales:,.0f}")
        ], className="stat-card"),
        html.Div([
            html.H3("📊 Avg Daily Sales"),
            html.P(f"${avg_daily_sales:,.0f}")
        ], className="stat-card"),
        html.Div([
            html.H3("🏆 Best Day"),
            html.P(f"${max_sales:,.0f}"),
            html.Small(max_date, style={'fontSize': '12px'})
        ], className="stat-card")
    ]

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
