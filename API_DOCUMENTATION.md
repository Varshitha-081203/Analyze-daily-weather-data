# Weather Data Analysis Toolkit - API Documentation

## Table of Contents

- [WeatherAnalyzer Class](#weatheranalyzer-class)
  - [Constructor](#constructor)
  - [Data Loading Methods](#data-loading-methods)
  - [Data Exploration Methods](#data-exploration-methods)
  - [Visualization Methods](#visualization-methods)
  - [Analysis Methods](#analysis-methods)
  - [Machine Learning Methods](#machine-learning-methods)
  - [Utility Methods](#utility-methods)
- [Function Reference](#function-reference)
- [Error Handling](#error-handling)
- [Type Annotations](#type-annotations)
- [Examples](#examples)

---

## WeatherAnalyzer Class

### Constructor

#### `WeatherAnalyzer(feature_columns=None, target_column='Rainfall')`

Initialize a new WeatherAnalyzer instance.

**Signature:**
```python
def __init__(self, feature_columns: Optional[list] = None, target_column: str = 'Rainfall') -> None
```

**Parameters:**
- `feature_columns` (Optional[list]): List of column names to use as features for machine learning. If None, defaults to `['MinTemp', 'MaxTemp']`.
- `target_column` (str): Name of the target column for prediction. Defaults to `'Rainfall'`.

**Attributes Created:**
- `df` (pd.DataFrame): Will store the loaded weather dataset
- `model` (LinearRegression): Will store the trained ML model
- `feature_columns` (list): Features used for ML prediction
- `target_column` (str): Target variable for prediction
- `_monthly_stats` (pd.Series): Internal storage for monthly statistics

**Example:**
```python
# Default initialization
analyzer = WeatherAnalyzer()

# Custom features
analyzer = WeatherAnalyzer(
    feature_columns=['MinTemp', 'MaxTemp', 'Humidity9am'],
    target_column='Rainfall'
)
```

---

## Data Loading Methods

### `load_data(filepath)`

Load weather data from a CSV file into the analyzer.

**Signature:**
```python
def load_data(self, filepath: str) -> pd.DataFrame
```

**Parameters:**
- `filepath` (str): Path to the CSV file containing weather data. Can be relative or absolute path.

**Returns:**
- `pd.DataFrame`: The loaded weather dataset

**Raises:**
- `FileNotFoundError`: If the specified file doesn't exist
- `pd.errors.EmptyDataError`: If the file is empty or cannot be parsed

**Side Effects:**
- Sets `self.df` to the loaded DataFrame
- Prints loading status and record count

**Example:**
```python
analyzer = WeatherAnalyzer()
df = analyzer.load_data('weather.csv')
print(f"Loaded {len(df)} records with {len(df.columns)} columns")
```

---

## Data Exploration Methods

### `explore_data()`

Perform comprehensive data exploration and return detailed statistics.

**Signature:**
```python
def explore_data(self) -> Dict[str, Any]
```

**Parameters:**
None

**Returns:**
- `dict`: Dictionary containing exploration results:
  - `shape` (tuple): Dataset dimensions (rows, columns)
  - `columns` (list): List of all column names
  - `missing_values` (pd.Series): Count of missing values per column
  - `data_types` (pd.Series): Data types of each column
  - `summary_stats` (pd.DataFrame): Descriptive statistics for numeric columns

**Raises:**
- `ValueError`: If no data has been loaded (`self.df is None`)

**Side Effects:**
- Prints comprehensive exploration report including:
  - Dataset shape and column names
  - First 5 rows preview
  - Data types and info
  - Summary statistics

**Example:**
```python
analyzer.load_data('weather.csv')
exploration = analyzer.explore_data()

print(f"Shape: {exploration['shape']}")
print(f"Missing values total: {exploration['missing_values'].sum()}")
print(f"Numeric columns: {len(exploration['summary_stats'].columns)}")
```

---

## Visualization Methods

### `visualize_correlations(columns=None, figsize=(10, 6))`

Create pairplot visualization showing correlations between specified columns.

**Signature:**
```python
def visualize_correlations(self, columns: Optional[list] = None, figsize: Tuple[int, int] = (10, 6)) -> None
```

**Parameters:**
- `columns` (Optional[list]): List of column names to include in the pairplot. If None, defaults to `['MinTemp', 'MaxTemp', 'Rainfall']`.
- `figsize` (Tuple[int, int]): Figure size as (width, height) in inches. Defaults to `(10, 6)`.

**Returns:**
None

**Raises:**
- `ValueError`: If no data has been loaded or if specified columns don't exist in the dataset

**Side Effects:**
- Creates and displays a seaborn pairplot
- Prints information about which columns are being plotted

**Example:**
```python
analyzer.load_data('weather.csv')

# Default correlation plot
analyzer.visualize_correlations()

# Custom columns and size
analyzer.visualize_correlations(
    columns=['MinTemp', 'MaxTemp', 'Humidity9am', 'Pressure9am'],
    figsize=(12, 8)
)
```

### `plot_monthly_trends(figsize=(12, 6))`

Create a line plot showing monthly temperature trends.

**Signature:**
```python
def plot_monthly_trends(self, figsize: Tuple[int, int] = (12, 6)) -> None
```

**Parameters:**
- `figsize` (Tuple[int, int]): Figure size as (width, height) in inches. Defaults to `(12, 6)`.

**Returns:**
None

**Raises:**
- `ValueError`: If monthly analysis hasn't been performed yet (call `analyze_monthly_trends()` first)

**Side Effects:**
- Creates and displays a matplotlib line plot with:
  - Monthly average temperatures on y-axis
  - Months (1-12) on x-axis
  - Data point annotations
  - Grid and styling

**Example:**
```python
analyzer.load_data('weather.csv')
analyzer.analyze_monthly_trends()
analyzer.plot_monthly_trends(figsize=(14, 7))
```

---

## Analysis Methods

### `analyze_monthly_trends(date_column='Date')`

Analyze monthly temperature patterns and calculate averages.

**Signature:**
```python
def analyze_monthly_trends(self, date_column: str = 'Date') -> pd.Series
```

**Parameters:**
- `date_column` (str): Name of the date column in the dataset. Defaults to `'Date'`.

**Returns:**
- `pd.Series`: Monthly average maximum temperatures indexed by month number (1-12)

**Raises:**
- `ValueError`: If no data loaded or if the specified date column doesn't exist
- `KeyError`: If `'MaxTemp'` column doesn't exist in the dataset

**Side Effects:**
- Stores monthly statistics in `self._monthly_stats`
- Prints detailed monthly temperature breakdown
- Converts date column to datetime format (on a copy)

**Example:**
```python
analyzer.load_data('weather.csv')
monthly_temps = analyzer.analyze_monthly_trends()

hottest_month = monthly_temps.idxmax()
coldest_month = monthly_temps.idxmin()
print(f"Hottest: Month {hottest_month}, Coldest: Month {coldest_month}")
```

### `get_insights()`

Generate comprehensive insights and statistics from the loaded weather data.

**Signature:**
```python
def get_insights(self) -> Dict[str, Any]
```

**Parameters:**
None

**Returns:**
- `dict`: Dictionary containing various insights:
  - `total_records` (int): Total number of records
  - `date_range` (dict): Start and end dates if available
  - `max_temperature` (dict): Highest, lowest, and average max temperatures
  - `min_temperature` (dict): Highest, lowest, and average min temperatures  
  - `rainfall` (dict): Total, average, max single day, and rainy days count
  - `hottest_month` (int): Month with highest average temperature (if trends analyzed)
  - `coldest_month` (int): Month with lowest average temperature (if trends analyzed)

**Raises:**
- `ValueError`: If no data has been loaded

**Side Effects:**
- Prints comprehensive insights summary

**Example:**
```python
analyzer.load_data('weather.csv')
analyzer.analyze_monthly_trends()  # Optional for monthly insights
insights = analyzer.get_insights()

print(f"Total rainy days: {insights['rainfall']['rainy_days']}")
print(f"Average rainfall: {insights['rainfall']['average']:.2f}mm")
```

---

## Machine Learning Methods

### `prepare_ml_data(test_size=0.2, random_state=42)`

Prepare and split data for machine learning training and testing.

**Signature:**
```python
def prepare_ml_data(self, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]
```

**Parameters:**
- `test_size` (float): Proportion of data to use for testing. Must be between 0 and 1. Defaults to `0.2` (20%).
- `random_state` (int): Random seed for reproducible data splitting. Defaults to `42`.

**Returns:**
- `tuple`: Four numpy arrays in order:
  - `X_train`: Training features
  - `X_test`: Testing features  
  - `y_train`: Training target values
  - `y_test`: Testing target values

**Raises:**
- `ValueError`: If no data loaded, or if required feature/target columns are missing

**Side Effects:**
- Prints information about data preparation including feature names and sample counts
- Handles missing values by dropping rows with NaN in feature columns

**Example:**
```python
analyzer = WeatherAnalyzer(feature_columns=['MinTemp', 'MaxTemp', 'Humidity9am'])
analyzer.load_data('weather.csv')
X_train, X_test, y_train, y_test = analyzer.prepare_ml_data(test_size=0.3)

print(f"Training set: {len(X_train)} samples")
print(f"Test set: {len(X_test)} samples")
```

### `predict_rainfall(test_size=0.2, random_state=42)`

Train a linear regression model and evaluate its performance on rainfall prediction.

**Signature:**
```python
def predict_rainfall(self, test_size: float = 0.2, random_state: int = 42) -> Dict[str, float]
```

**Parameters:**
- `test_size` (float): Proportion of data for testing. Defaults to `0.2`.
- `random_state` (int): Random seed for reproducibility. Defaults to `42`.

**Returns:**
- `dict`: Model performance metrics:
  - `mse` (float): Mean Squared Error
  - `rmse` (float): Root Mean Squared Error
  - `r2` (float): R-squared coefficient of determination
  - `mae` (float): Mean Absolute Error

**Raises:**
- `ValueError`: If no data loaded or if model training fails

**Side Effects:**
- Trains and stores linear regression model in `self.model`
- Prints detailed performance metrics and model coefficients
- Calls `prepare_ml_data()` internally

**Example:**
```python
analyzer = WeatherAnalyzer()
analyzer.load_data('weather.csv')
metrics = analyzer.predict_rainfall()

print(f"Model accuracy (R²): {metrics['r2']:.3f}")
if metrics['r2'] > 0.7:
    print("Good model performance!")
```

### `predict_custom(min_temp, max_temp)`

Make rainfall prediction for custom temperature values using the trained model.

**Signature:**
```python
def predict_custom(self, min_temp: float, max_temp: float) -> float
```

**Parameters:**
- `min_temp` (float): Minimum temperature in degrees Celsius
- `max_temp` (float): Maximum temperature in degrees Celsius

**Returns:**
- `float`: Predicted rainfall amount in millimeters

**Raises:**
- `ValueError`: If model hasn't been trained yet (call `predict_rainfall()` first)

**Side Effects:**
- Prints the prediction result with input parameters

**Note:**
This method assumes the default feature set of `['MinTemp', 'MaxTemp']`. For custom features, ensure the input matches your configured feature columns.

**Example:**
```python
analyzer = WeatherAnalyzer()
analyzer.load_data('weather.csv')
analyzer.predict_rainfall()  # Train the model first

# Single prediction
rainfall = analyzer.predict_custom(min_temp=15.0, max_temp=25.0)
print(f"Expected rainfall: {rainfall:.2f}mm")

# Multiple predictions
scenarios = [(10, 20), (15, 25), (20, 30)]
for min_t, max_t in scenarios:
    predicted = analyzer.predict_custom(min_t, max_t)
    print(f"{min_t}-{max_t}°C: {predicted:.2f}mm")
```

---

## Function Reference

### `main()`

Demonstration function showing complete weather analysis workflow.

**Signature:**
```python
def main() -> None
```

**Parameters:**
None

**Returns:**
None

**Description:**
Executes a complete analysis workflow including:
1. Data loading from 'weather.csv'
2. Data exploration
3. Correlation visualization
4. Monthly trend analysis
5. Machine learning model training
6. Custom predictions
7. Insights generation

**Example:**
```python
# Run the complete demo
if __name__ == "__main__":
    main()
```

---

## Error Handling

The WeatherAnalyzer class implements comprehensive error handling:

### File Operations
- **FileNotFoundError**: Raised when CSV file doesn't exist
- **pd.errors.EmptyDataError**: Raised when CSV file is empty or corrupted

### Data Validation
- **ValueError**: Raised when:
  - Required data hasn't been loaded
  - Specified columns don't exist in dataset
  - Model operations attempted without training
  - Invalid parameter values provided
- **KeyError**: Raised when required columns are missing from dataset

### Machine Learning
- **ValueError**: Raised when:
  - Feature columns missing from dataset
  - Target column missing from dataset
  - Insufficient data for training
  - Model prediction attempted before training

### Example Error Handling:
```python
try:
    analyzer = WeatherAnalyzer()
    analyzer.load_data('weather.csv')
    metrics = analyzer.predict_rainfall()
except FileNotFoundError:
    print("Weather data file not found!")
except ValueError as e:
    print(f"Data validation error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## Type Annotations

The API uses comprehensive type annotations for better code clarity and IDE support:

```python
from typing import Optional, Tuple, Dict, Any
import pandas as pd
import numpy as np

# Constructor
def __init__(self, feature_columns: Optional[list] = None, target_column: str = 'Rainfall') -> None

# Data operations
def load_data(self, filepath: str) -> pd.DataFrame
def explore_data(self) -> Dict[str, Any]

# Visualization
def visualize_correlations(self, columns: Optional[list] = None, figsize: Tuple[int, int] = (10, 6)) -> None
def plot_monthly_trends(self, figsize: Tuple[int, int] = (12, 6)) -> None

# Analysis
def analyze_monthly_trends(self, date_column: str = 'Date') -> pd.Series
def get_insights(self) -> Dict[str, Any]

# Machine Learning
def prepare_ml_data(self, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]
def predict_rainfall(self, test_size: float = 0.2, random_state: int = 42) -> Dict[str, float]
def predict_custom(self, min_temp: float, max_temp: float) -> float
```

---

## Examples

### Basic Usage Pattern
```python
# 1. Initialize
analyzer = WeatherAnalyzer()

# 2. Load data
analyzer.load_data('weather.csv')

# 3. Explore
exploration = analyzer.explore_data()

# 4. Visualize
analyzer.visualize_correlations()

# 5. Analyze trends
monthly_trends = analyzer.analyze_monthly_trends()
analyzer.plot_monthly_trends()

# 6. Machine learning
metrics = analyzer.predict_rainfall()

# 7. Custom predictions
rainfall = analyzer.predict_custom(15.0, 25.0)

# 8. Get insights
insights = analyzer.get_insights()
```

### Advanced Configuration
```python
# Custom feature engineering
analyzer = WeatherAnalyzer(
    feature_columns=['MinTemp', 'MaxTemp', 'Humidity9am', 'Pressure9am', 'WindSpeed9am'],
    target_column='Rainfall'
)

# Custom data preparation
X_train, X_test, y_train, y_test = analyzer.prepare_ml_data(
    test_size=0.25, 
    random_state=123
)

# Custom visualization
analyzer.visualize_correlations(
    columns=['MinTemp', 'MaxTemp', 'Humidity9am', 'Humidity3pm', 'Pressure9am'], 
    figsize=(15, 10)
)
```

### Batch Processing
```python
# Load and train once
analyzer = WeatherAnalyzer()
analyzer.load_data('weather.csv')
analyzer.predict_rainfall()

# Multiple predictions
temperature_scenarios = [
    (5, 15), (10, 20), (15, 25), (20, 30), (25, 35)
]

predictions = []
for min_t, max_t in temperature_scenarios:
    rainfall = analyzer.predict_custom(min_t, max_t)
    predictions.append({
        'min_temp': min_t,
        'max_temp': max_t, 
        'rainfall': rainfall
    })
```

---

**API Version**: 1.0.0  
**Last Updated**: 2024  
**Python Version**: 3.7+