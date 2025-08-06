# Weather Data Analysis Toolkit

A comprehensive Python toolkit for analyzing weather data with built-in visualization and machine learning capabilities.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Data Format](#data-format)
- [Contributing](#contributing)
- [License](#license)

## Features

🌦️ **Comprehensive Weather Analysis**
- Data loading and exploration
- Statistical analysis and insights generation
- Interactive visualizations

📊 **Data Visualization**
- Correlation plots and pairplots
- Monthly trend analysis
- Temperature and rainfall patterns

🤖 **Machine Learning**
- Rainfall prediction using linear regression
- Model performance evaluation
- Custom prediction capabilities

📋 **Rich Reporting**
- Detailed data exploration reports
- Performance metrics and insights
- Professional-grade documentation

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Dependencies

```
pandas>=1.0         # Data manipulation and analysis
matplotlib>=3.2     # Plotting and visualization
seaborn>=0.10      # Statistical data visualization
scikit-learn>=0.22 # Machine learning algorithms
```

## Quick Start

```python
from weather_data_analysis import WeatherAnalyzer

# Initialize the analyzer
analyzer = WeatherAnalyzer()

# Load your weather data
analyzer.load_data('weather.csv')

# Explore the data
exploration = analyzer.explore_data()

# Analyze monthly trends
monthly_trends = analyzer.analyze_monthly_trends()

# Train ML model and get predictions
metrics = analyzer.predict_rainfall()

# Make custom predictions
rainfall = analyzer.predict_custom(min_temp=15.0, max_temp=25.0)

# Get comprehensive insights
insights = analyzer.get_insights()
```

## API Reference

### WeatherAnalyzer Class

The main class for weather data analysis operations.

#### Constructor

```python
WeatherAnalyzer(feature_columns=None, target_column='Rainfall')
```

**Parameters:**
- `feature_columns` (list, optional): Features for ML prediction. Defaults to `['MinTemp', 'MaxTemp']`
- `target_column` (str): Target variable for prediction. Defaults to `'Rainfall'`

#### Methods

##### `load_data(filepath)`

Load weather data from a CSV file.

**Parameters:**
- `filepath` (str): Path to the CSV file containing weather data

**Returns:**
- `pd.DataFrame`: Loaded weather dataset

**Raises:**
- `FileNotFoundError`: If the specified file doesn't exist
- `pd.errors.EmptyDataError`: If the file is empty

**Example:**
```python
analyzer = WeatherAnalyzer()
df = analyzer.load_data('weather.csv')
print(f"Loaded {len(df)} records")
```

##### `explore_data()`

Perform comprehensive data exploration and return summary statistics.

**Returns:**
- `dict`: Dictionary containing exploration results:
  - `shape`: Dataset dimensions
  - `columns`: List of column names
  - `missing_values`: Count of missing values per column
  - `data_types`: Data types of each column
  - `summary_stats`: Descriptive statistics

**Raises:**
- `ValueError`: If no data has been loaded

**Example:**
```python
exploration = analyzer.explore_data()
print(f"Dataset shape: {exploration['shape']}")
print(f"Missing values: {exploration['missing_values'].sum()}")
```

##### `visualize_correlations(columns=None, figsize=(10, 6))`

Create pairplot visualization for specified columns.

**Parameters:**
- `columns` (list, optional): Columns to include in pairplot. Defaults to `['MinTemp', 'MaxTemp', 'Rainfall']`
- `figsize` (tuple): Figure size as (width, height). Defaults to `(10, 6)`

**Raises:**
- `ValueError`: If no data has been loaded or columns don't exist

**Example:**
```python
analyzer.visualize_correlations(['MinTemp', 'MaxTemp', 'Humidity9am'])
```

##### `analyze_monthly_trends(date_column='Date')`

Analyze monthly temperature trends.

**Parameters:**
- `date_column` (str): Name of the date column. Defaults to `'Date'`

**Returns:**
- `pd.Series`: Monthly average maximum temperatures

**Raises:**
- `ValueError`: If no data loaded or date column doesn't exist
- `KeyError`: If MaxTemp column doesn't exist

**Example:**
```python
monthly_temps = analyzer.analyze_monthly_trends()
print(f"Hottest month: {monthly_temps.idxmax()}")
print(f"Coldest month: {monthly_temps.idxmin()}")
```

##### `plot_monthly_trends(figsize=(12, 6))`

Plot monthly temperature trends.

**Parameters:**
- `figsize` (tuple): Figure size as (width, height). Defaults to `(12, 6)`

**Raises:**
- `ValueError`: If monthly analysis hasn't been performed yet

**Example:**
```python
analyzer.analyze_monthly_trends()
analyzer.plot_monthly_trends()
```

##### `prepare_ml_data(test_size=0.2, random_state=42)`

Prepare data for machine learning by splitting into train/test sets.

**Parameters:**
- `test_size` (float): Proportion of data for testing. Defaults to `0.2`
- `random_state` (int): Random seed for reproducibility. Defaults to `42`

**Returns:**
- `tuple`: (X_train, X_test, y_train, y_test) arrays

**Raises:**
- `ValueError`: If no data loaded or required columns missing

**Example:**
```python
X_train, X_test, y_train, y_test = analyzer.prepare_ml_data()
print(f"Training set size: {len(X_train)}")
```

##### `predict_rainfall(test_size=0.2, random_state=42)`

Train a linear regression model to predict rainfall and evaluate performance.

**Parameters:**
- `test_size` (float): Proportion of data for testing. Defaults to `0.2`
- `random_state` (int): Random seed for reproducibility. Defaults to `42`

**Returns:**
- `dict`: Dictionary containing model performance metrics:
  - `mse`: Mean Squared Error
  - `rmse`: Root Mean Squared Error
  - `r2`: R-squared score
  - `mae`: Mean Absolute Error

**Raises:**
- `ValueError`: If no data loaded or model training fails

**Example:**
```python
metrics = analyzer.predict_rainfall()
print(f"Model R²: {metrics['r2']:.3f}")
print(f"RMSE: {metrics['rmse']:.3f}")
```

##### `predict_custom(min_temp, max_temp)`

Make a rainfall prediction for custom temperature values.

**Parameters:**
- `min_temp` (float): Minimum temperature
- `max_temp` (float): Maximum temperature

**Returns:**
- `float`: Predicted rainfall amount

**Raises:**
- `ValueError`: If model hasn't been trained yet

**Example:**
```python
analyzer.predict_rainfall()  # Train model first
rainfall = analyzer.predict_custom(min_temp=15.0, max_temp=25.0)
print(f"Predicted rainfall: {rainfall:.2f}mm")
```

##### `get_insights()`

Generate comprehensive insights from the weather data analysis.

**Returns:**
- `dict`: Dictionary containing various insights about the weather data

**Raises:**
- `ValueError`: If no data has been loaded or analyzed

**Example:**
```python
analyzer.analyze_monthly_trends()
insights = analyzer.get_insights()
print(f"Hottest month: {insights['hottest_month']}")
```

## Examples

### Complete Analysis Workflow

```python
from weather_data_analysis import WeatherAnalyzer

def complete_analysis():
    """Demonstrate a complete weather analysis workflow."""
    
    # Initialize analyzer
    analyzer = WeatherAnalyzer()
    
    # Load and explore data
    analyzer.load_data('weather.csv')
    exploration = analyzer.explore_data()
    
    # Visualize data relationships
    analyzer.visualize_correlations()
    
    # Analyze temporal patterns
    monthly_trends = analyzer.analyze_monthly_trends()
    analyzer.plot_monthly_trends()
    
    # Machine learning analysis
    ml_metrics = analyzer.predict_rainfall()
    
    # Custom predictions
    predictions = [
        analyzer.predict_custom(10, 20),
        analyzer.predict_custom(15, 25),
        analyzer.predict_custom(20, 30)
    ]
    
    # Get insights
    insights = analyzer.get_insights()
    
    return {
        'exploration': exploration,
        'ml_metrics': ml_metrics,
        'predictions': predictions,
        'insights': insights
    }

if __name__ == "__main__":
    results = complete_analysis()
```

### Custom Feature Analysis

```python
# Analyze with different features
analyzer = WeatherAnalyzer(
    feature_columns=['MinTemp', 'MaxTemp', 'Humidity9am', 'Pressure9am'],
    target_column='Rainfall'
)

analyzer.load_data('weather.csv')
metrics = analyzer.predict_rainfall()
```

### Focused Visualization

```python
# Create specific visualizations
analyzer = WeatherAnalyzer()
analyzer.load_data('weather.csv')

# Temperature and humidity correlations
analyzer.visualize_correlations([
    'MinTemp', 'MaxTemp', 'Humidity9am', 'Humidity3pm'
], figsize=(12, 8))
```

### Batch Predictions

```python
# Make multiple predictions
analyzer = WeatherAnalyzer()
analyzer.load_data('weather.csv')
analyzer.predict_rainfall()

# Temperature ranges for prediction
temp_ranges = [
    (5, 15), (10, 20), (15, 25), (20, 30), (25, 35)
]

predictions = []
for min_temp, max_temp in temp_ranges:
    rainfall = analyzer.predict_custom(min_temp, max_temp)
    predictions.append({
        'min_temp': min_temp,
        'max_temp': max_temp,
        'predicted_rainfall': rainfall
    })

print("Rainfall predictions for different temperature ranges:")
for pred in predictions:
    print(f"  {pred['min_temp']}-{pred['max_temp']}°C: {pred['predicted_rainfall']:.2f}mm")
```

## Data Format

The weather data should be in CSV format with the following expected columns:

### Required Columns

- `Date`: Date of the weather observation
- `MinTemp`: Minimum temperature for the day
- `MaxTemp`: Maximum temperature for the day
- `Rainfall`: Amount of rainfall (target variable)

### Optional Columns

- `Evaporation`: Evaporation amount
- `Sunshine`: Hours of sunshine
- `WindGustDir`: Wind gust direction
- `WindGustSpeed`: Wind gust speed
- `WindDir9am`, `WindDir3pm`: Wind direction at 9am and 3pm
- `WindSpeed9am`, `WindSpeed3pm`: Wind speed at 9am and 3pm
- `Humidity9am`, `Humidity3pm`: Humidity at 9am and 3pm
- `Pressure9am`, `Pressure3pm`: Atmospheric pressure at 9am and 3pm
- `Cloud9am`, `Cloud3pm`: Cloud cover at 9am and 3pm
- `Temp9am`, `Temp3pm`: Temperature at 9am and 3pm
- `RainToday`: Whether it rained today (Yes/No)
- `RISK_MM`: Risk of rainfall
- `RainTomorrow`: Whether it will rain tomorrow (Yes/No)

### Sample Data Structure

```csv
MinTemp,MaxTemp,Rainfall,Evaporation,Sunshine,WindGustDir,WindGustSpeed,Date
8,24.3,0,3.4,6.3,NW,30,2021-01-01
14,26.9,3.6,4.4,9.7,ENE,39,2021-01-02
13.7,23.4,3.6,5.8,3.3,NW,85,2021-01-03
```

## Error Handling

The toolkit includes comprehensive error handling:

- **File Operations**: Handles missing files and empty datasets
- **Data Validation**: Checks for required columns and data types
- **Model Training**: Validates features and targets before training
- **Visualization**: Ensures data exists before plotting

## Performance Considerations

- **Memory Usage**: Large datasets are handled efficiently with pandas
- **Processing Speed**: Vectorized operations for optimal performance
- **Visualization**: Matplotlib and seaborn for high-quality plots
- **ML Training**: Scikit-learn for reliable machine learning

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues, please:

1. Check the API documentation above
2. Review the examples section
3. Open an issue on the repository
4. Contact the development team

---

**Version**: 1.0.0  
**Author**: Weather Analysis Team  
**Last Updated**: 2024