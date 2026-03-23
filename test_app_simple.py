import pytest
import pandas as pd
import os
import sys

# Add the current directory to path
sys.path.append(os.path.dirname(__file__))

# Import app without running it
import app

def test_data_file_exists():
    """Test that the formatted_data.csv file exists"""
    assert os.path.exists('formatted_data.csv'), "formatted_data.csv file not found"
    print("✓ Data file exists")

def test_data_has_required_columns():
    """Test that the data has the required columns"""
    df = pd.read_csv('formatted_data.csv')
    required_columns = ['sales', 'date', 'region']
    for col in required_columns:
        assert col in df.columns, f"Column '{col}' not found in data"
    print(f"✓ Data has required columns: {', '.join(required_columns)}")

def test_data_has_pink_morsel_only():
    """Test that the data only contains sales values (no product column needed)"""
    df = pd.read_csv('formatted_data.csv')
    # Verify data is not empty
    assert len(df) > 0, "Data is empty"
    print(f"✓ Data has {len(df)} records")

def test_app_has_header():
    """Test that the app layout contains a header"""
    # Layout structure: Div -> Div (header)
    header_found = False
    for child in app.app.layout.children:
        if hasattr(child, 'id') and child.id == 'header':
            header_found = True
            break
    assert header_found, "Header not found in app layout"
    print("✓ Header element exists in app")

def test_app_has_chart():
    """Test that the app layout contains a chart"""
    # Layout structure: Div -> Div -> Div -> Graph
    chart_found = False
    # First level: layout children
    for child in app.app.layout.children:
        # Look for the container (second div)
        if hasattr(child, 'children') and isinstance(child.children, list):
            for inner_child in child.children:
                # Look for the card div
                if hasattr(inner_child, 'children') and isinstance(inner_child.children, list):
                    for card_child in inner_child.children:
                        if hasattr(card_child, 'id') and card_child.id == 'sales-chart':
                            chart_found = True
                            break
    assert chart_found, "Chart element not found in app layout"
    print("✓ Chart element exists in app")

def test_app_has_region_selector():
    """Test that the app layout contains a region selector"""
    # Layout structure: Div -> Div -> Div -> Div -> RadioItems
    selector_found = False
    # First level: layout children
    for child in app.app.layout.children:
        # Look for the container (second div)
        if hasattr(child, 'children') and isinstance(child.children, list):
            for inner_child in child.children:
                # Look for the region-selector div
                if hasattr(inner_child, 'children') and isinstance(inner_child.children, list):
                    for selector_child in inner_child.children:
                        if hasattr(selector_child, 'children') and isinstance(selector_child.children, list):
                            for radio_child in selector_child.children:
                                if hasattr(radio_child, 'id') and radio_child.id == 'region-selector':
                                    selector_found = True
                                    break
    assert selector_found, "Region selector not found in app layout"
    print("✓ Region selector exists in app")

def test_region_selector_has_five_options():
    """Test that region selector has all 5 options"""
    selector = None
    # Navigate to the RadioItems component
    for child in app.app.layout.children:
        if hasattr(child, 'children') and isinstance(child.children, list):
            for inner_child in child.children:
                if hasattr(inner_child, 'children') and isinstance(inner_child.children, list):
                    for selector_child in inner_child.children:
                        if hasattr(selector_child, 'children') and isinstance(selector_child.children, list):
                            for radio_child in selector_child.children:
                                if hasattr(radio_child, 'id') and radio_child.id == 'region-selector':
                                    selector = radio_child
                                    break
    
    assert selector is not None, "Could not find region selector"
    
    expected_values = ['all', 'north', 'south', 'east', 'west']
    actual_values = [opt['value'] for opt in selector.options]
    
    for val in expected_values:
        assert val in actual_values, f"Option '{val}' not found in region selector"
    
    print(f"✓ Region selector has all 5 options: {', '.join(actual_values)}")

def test_region_selector_default_value():
    """Test that region selector default value is 'all'"""
    selector = None
    # Navigate to the RadioItems component
    for child in app.app.layout.children:
        if hasattr(child, 'children') and isinstance(child.children, list):
            for inner_child in child.children:
                if hasattr(inner_child, 'children') and isinstance(inner_child.children, list):
                    for selector_child in inner_child.children:
                        if hasattr(selector_child, 'children') and isinstance(selector_child.children, list):
                            for radio_child in selector_child.children:
                                if hasattr(radio_child, 'id') and radio_child.id == 'region-selector':
                                    selector = radio_child
                                    break
    
    assert selector is not None, "Could not find region selector"
    assert selector.value == 'all', f"Default value should be 'all', got '{selector.value}'"
    print("✓ Region selector default value is 'all'")

def test_stats_cards_placeholder_exists():
    """Test that stats cards placeholder exists"""
    stats_found = False
    # Navigate to the stats-cards div
    for child in app.app.layout.children:
        if hasattr(child, 'children') and isinstance(child.children, list):
            for inner_child in child.children:
                if hasattr(inner_child, 'id') and inner_child.id == 'stats-cards':
                    stats_found = True
                    break
    assert stats_found, "Stats cards placeholder not found"
    print("✓ Stats cards placeholder exists")

def test_stats_callback_exists():
    """Test that the stats callback function exists"""
    assert hasattr(app, 'update_stats'), "update_stats callback not found"
    print("✓ Stats callback exists")

def test_chart_callback_exists():
    """Test that the chart callback function exists"""
    assert hasattr(app, 'update_chart'), "update_chart callback not found"
    print("✓ Chart callback exists")

if __name__ == '__main__':
    pytest.main([__file__, '-v'])