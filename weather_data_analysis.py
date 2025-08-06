"""
Weather Data Analysis Module

This module provides comprehensive tools for analyzing weather data including
data exploration, visualization, and machine learning predictions.

Author: Weather Analysis Team
Version: 1.0.0
License: MIT
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from typing import Optional, Tuple, Dict, Any
import numpy as np
import warnings
warnings.filterwarnings('ignore')


class WeatherAnalyzer:
    """
    A comprehensive weather data analysis toolkit.
    
    This class provides methods for loading, exploring, visualizing, and 
    analyzing weather data, including machine learning capabilities for
    rainfall prediction.
    
    Attributes:
        df (pd.DataFrame): The loaded weather dataset
        model (LinearRegression): Trained model for rainfall prediction
        feature_columns (list): List of features used for prediction
        target_column (str): Target variable for prediction
    
    Example:
        >>> analyzer = WeatherAnalyzer()
        >>> analyzer.load_data('weather.csv')
        >>> analyzer.explore_data()
        >>> analyzer.analyze_monthly_trends()
        >>> mse = analyzer.predict_rainfall()
        >>> print(f"Model MSE: {mse}")
    """
    
    def __init__(self, feature_columns: Optional[list] = None, target_column: str = 'Rainfall'):
        """
        Initialize the WeatherAnalyzer.
        
        Args:
            feature_columns (list, optional): Features for ML prediction. 
                                            Defaults to ['MinTemp', 'MaxTemp'].
            target_column (str): Target variable for prediction. Defaults to 'Rainfall'.
        """
        self.df = None
        self.model = None
        self.feature_columns = feature_columns or ['MinTemp', 'MaxTemp']
        self.target_column = target_column
        self._monthly_stats = None
    
    def load_data(self, filepath: str) -> pd.DataFrame:
        """
        Load weather data from a CSV file.
        
        Args:
            filepath (str): Path to the CSV file containing weather data
            
        Returns:
            pd.DataFrame: Loaded weather dataset
            
        Raises:
            FileNotFoundError: If the specified file doesn't exist
            pd.errors.EmptyDataError: If the file is empty
            
        Example:
            >>> analyzer = WeatherAnalyzer()
            >>> df = analyzer.load_data('weather.csv')
            >>> print(f"Loaded {len(df)} records")
        """
        try:
            self.df = pd.read_csv(filepath)
            print(f"Successfully loaded {len(self.df)} records from {filepath}")
            return self.df
        except FileNotFoundError:
            raise FileNotFoundError(f"Weather data file not found: {filepath}")
        except pd.errors.EmptyDataError:
            raise pd.errors.EmptyDataError(f"Empty data file: {filepath}")
    
    def explore_data(self) -> Dict[str, Any]:
        """
        Perform comprehensive data exploration and return summary statistics.
        
        Returns:
            dict: Dictionary containing exploration results including:
                - shape: Dataset dimensions
                - columns: List of column names
                - missing_values: Count of missing values per column
                - data_types: Data types of each column
                - summary_stats: Descriptive statistics
                
        Raises:
            ValueError: If no data has been loaded
            
        Example:
            >>> analyzer = WeatherAnalyzer()
            >>> analyzer.load_data('weather.csv')
            >>> exploration = analyzer.explore_data()
            >>> print(f"Dataset shape: {exploration['shape']}")
            >>> print(f"Missing values: {exploration['missing_values'].sum()}")
        """
        if self.df is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        print("=== DATA EXPLORATION ===")
        print(f"Dataset shape: {self.df.shape}")
        print(f"Columns: {list(self.df.columns)}")
        print("\nFirst 5 rows:")
        print(self.df.head())
        print("\nDataset info:")
        print(self.df.info())
        print("\nSummary statistics:")
        print(self.df.describe())
        
        exploration_results = {
            'shape': self.df.shape,
            'columns': list(self.df.columns),
            'missing_values': self.df.isnull().sum(),
            'data_types': self.df.dtypes,
            'summary_stats': self.df.describe()
        }
        
        return exploration_results
    
    def visualize_correlations(self, columns: Optional[list] = None, figsize: Tuple[int, int] = (10, 6)) -> None:
        """
        Create pairplot visualization for specified columns.
        
        Args:
            columns (list, optional): Columns to include in pairplot. 
                                    Defaults to ['MinTemp', 'MaxTemp', 'Rainfall'].
            figsize (tuple): Figure size as (width, height). Defaults to (10, 6).
            
        Raises:
            ValueError: If no data has been loaded or columns don't exist
            
        Example:
            >>> analyzer = WeatherAnalyzer()
            >>> analyzer.load_data('weather.csv')
            >>> analyzer.visualize_correlations(['MinTemp', 'MaxTemp', 'Humidity9am'])
        """
        if self.df is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        if columns is None:
            columns = ['MinTemp', 'MaxTemp', 'Rainfall']
        
        # Verify columns exist
        missing_cols = [col for col in columns if col not in self.df.columns]
        if missing_cols:
            raise ValueError(f"Columns not found in dataset: {missing_cols}")
        
        print(f"Creating pairplot for columns: {columns}")
        plt.figure(figsize=figsize)
        sns.pairplot(self.df[columns])
        plt.suptitle('Weather Data Correlations', y=1.02)
        plt.tight_layout()
        plt.show()
    
    def analyze_monthly_trends(self, date_column: str = 'Date') -> pd.Series:
        """
        Analyze monthly temperature trends.
        
        Args:
            date_column (str): Name of the date column. Defaults to 'Date'.
                             If column doesn't exist, creates synthetic monthly groupings.
            
        Returns:
            pd.Series: Monthly average maximum temperatures
            
        Raises:
            ValueError: If no data loaded
            KeyError: If MaxTemp column doesn't exist
            
        Example:
            >>> analyzer = WeatherAnalyzer()
            >>> analyzer.load_data('weather.csv')
            >>> monthly_temps = analyzer.analyze_monthly_trends()
            >>> print(f"Hottest month: {monthly_temps.idxmax()}")
            >>> print(f"Coldest month: {monthly_temps.idxmin()}")
        """
        if self.df is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        if 'MaxTemp' not in self.df.columns:
            raise KeyError("MaxTemp column not found in dataset.")
        
        # Convert date column and extract month
        df_copy = self.df.copy()
        
        if date_column in self.df.columns:
            # Use actual date column
            df_copy[date_column] = pd.to_datetime(df_copy[date_column])
            df_copy['Month'] = df_copy[date_column].dt.month
            print(f"Using actual date column '{date_column}' for monthly analysis.")
        else:
            # Create synthetic monthly groupings based on data order
            # Assume data is chronologically ordered and create 12 monthly groups
            n_records = len(df_copy)
            records_per_month = max(1, n_records // 12)
            df_copy['Month'] = (df_copy.index // records_per_month) % 12 + 1
            print(f"Date column '{date_column}' not found. Using synthetic monthly groupings based on data order.")
            print(f"Assuming {records_per_month} records per month for {n_records} total records.")
        
        # Calculate monthly averages
        monthly_avg_max_temp = df_copy.groupby('Month')['MaxTemp'].mean()
        self._monthly_stats = monthly_avg_max_temp
        
        print("=== MONTHLY TEMPERATURE TRENDS ===")
        print("Monthly Average Maximum Temperatures:")
        for month, temp in monthly_avg_max_temp.items():
            print(f"Month {month}: {temp:.2f}°C")
        
        return monthly_avg_max_temp
    
    def plot_monthly_trends(self, figsize: Tuple[int, int] = (12, 6)) -> None:
        """
        Plot monthly temperature trends.
        
        Args:
            figsize (tuple): Figure size as (width, height). Defaults to (12, 6).
            
        Raises:
            ValueError: If monthly analysis hasn't been performed yet
            
        Example:
            >>> analyzer = WeatherAnalyzer()
            >>> analyzer.load_data('weather.csv')
            >>> analyzer.analyze_monthly_trends()
            >>> analyzer.plot_monthly_trends()
        """
        if self._monthly_stats is None:
            raise ValueError("No monthly analysis performed. Call analyze_monthly_trends() first.")
        
        plt.figure(figsize=figsize)
        plt.plot(self._monthly_stats.index, self._monthly_stats.values, 
                marker='o', linewidth=2, markersize=8)
        plt.xlabel('Month', fontsize=12)
        plt.ylabel('Average Max Temperature (°C)', fontsize=12)
        plt.title('Monthly Average Maximum Temperature Trends', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.xticks(range(1, 13))
        
        # Add value labels on points
        for i, v in enumerate(self._monthly_stats.values, 1):
            plt.annotate(f'{v:.1f}°C', (i, v), textcoords="offset points", 
                        xytext=(0,10), ha='center')
        
        plt.tight_layout()
        plt.show()
    
    def prepare_ml_data(self, test_size: float = 0.2, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Prepare data for machine learning by splitting into train/test sets.
        
        Args:
            test_size (float): Proportion of data for testing. Defaults to 0.2.
            random_state (int): Random seed for reproducibility. Defaults to 42.
            
        Returns:
            tuple: (X_train, X_test, y_train, y_test) arrays
            
        Raises:
            ValueError: If no data loaded or required columns missing
            
        Example:
            >>> analyzer = WeatherAnalyzer()
            >>> analyzer.load_data('weather.csv')
            >>> X_train, X_test, y_train, y_test = analyzer.prepare_ml_data()
            >>> print(f"Training set size: {len(X_train)}")
        """
        if self.df is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        # Check if required columns exist
        missing_features = [col for col in self.feature_columns if col not in self.df.columns]
        if missing_features:
            raise ValueError(f"Feature columns not found: {missing_features}")
        
        if self.target_column not in self.df.columns:
            raise ValueError(f"Target column '{self.target_column}' not found.")
        
        # Prepare features and target
        X = self.df[self.feature_columns].dropna()
        y = self.df[self.target_column].loc[X.index]
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        print(f"Data prepared for ML:")
        print(f"  Features: {self.feature_columns}")
        print(f"  Target: {self.target_column}")
        print(f"  Training samples: {len(X_train)}")
        print(f"  Testing samples: {len(X_test)}")
        
        return X_train, X_test, y_train, y_test
    
    def predict_rainfall(self, test_size: float = 0.2, random_state: int = 42) -> Dict[str, float]:
        """
        Train a linear regression model to predict rainfall and evaluate performance.
        
        Args:
            test_size (float): Proportion of data for testing. Defaults to 0.2.
            random_state (int): Random seed for reproducibility. Defaults to 42.
            
        Returns:
            dict: Dictionary containing model performance metrics:
                - mse: Mean Squared Error
                - rmse: Root Mean Squared Error  
                - r2: R-squared score
                - mae: Mean Absolute Error
                
        Raises:
            ValueError: If no data loaded or model training fails
            
        Example:
            >>> analyzer = WeatherAnalyzer()
            >>> analyzer.load_data('weather.csv')
            >>> metrics = analyzer.predict_rainfall()
            >>> print(f"Model R²: {metrics['r2']:.3f}")
            >>> print(f"RMSE: {metrics['rmse']:.3f}")
        """
        # Prepare the data
        X_train, X_test, y_train, y_test = self.prepare_ml_data(test_size, random_state)
        
        # Train the model
        self.model = LinearRegression()
        self.model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = self.model.predict(X_test)
        
        # Calculate metrics
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        mae = np.mean(np.abs(y_test - y_pred))
        
        metrics = {
            'mse': mse,
            'rmse': rmse,
            'r2': r2,
            'mae': mae
        }
        
        print("=== MACHINE LEARNING RESULTS ===")
        print(f"Mean Squared Error: {mse:.4f}")
        print(f"Root Mean Squared Error: {rmse:.4f}")
        print(f"R² Score: {r2:.4f}")
        print(f"Mean Absolute Error: {mae:.4f}")
        
        # Model coefficients
        print(f"\nModel coefficients:")
        for feature, coef in zip(self.feature_columns, self.model.coef_):
            print(f"  {feature}: {coef:.4f}")
        print(f"  Intercept: {self.model.intercept_:.4f}")
        
        return metrics
    
    def predict_custom(self, min_temp: float, max_temp: float) -> float:
        """
        Make a rainfall prediction for custom temperature values.
        
        Args:
            min_temp (float): Minimum temperature
            max_temp (float): Maximum temperature
            
        Returns:
            float: Predicted rainfall amount
            
        Raises:
            ValueError: If model hasn't been trained yet
            
        Example:
            >>> analyzer = WeatherAnalyzer()
            >>> analyzer.load_data('weather.csv')
            >>> analyzer.predict_rainfall()
            >>> rainfall = analyzer.predict_custom(min_temp=15.0, max_temp=25.0)
            >>> print(f"Predicted rainfall: {rainfall:.2f}mm")
        """
        if self.model is None:
            raise ValueError("Model not trained. Call predict_rainfall() first.")
        
        prediction = self.model.predict([[min_temp, max_temp]])[0]
        print(f"Prediction for MinTemp={min_temp}°C, MaxTemp={max_temp}°C: {prediction:.2f}mm rainfall")
        return prediction
    
    def get_insights(self) -> Dict[str, Any]:
        """
        Generate comprehensive insights from the weather data analysis.
        
        Returns:
            dict: Dictionary containing various insights about the weather data
            
        Raises:
            ValueError: If no data has been loaded or analyzed
            
        Example:
            >>> analyzer = WeatherAnalyzer()
            >>> analyzer.load_data('weather.csv')
            >>> analyzer.analyze_monthly_trends()
            >>> insights = analyzer.get_insights()
            >>> print(f"Hottest month: {insights['hottest_month']}")
        """
        if self.df is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        insights = {}
        
        # Basic statistics
        insights['total_records'] = len(self.df)
        insights['date_range'] = {
            'start': self.df['Date'].min() if 'Date' in self.df.columns else 'Unknown',
            'end': self.df['Date'].max() if 'Date' in self.df.columns else 'Unknown'
        }
        
        # Temperature insights
        if 'MaxTemp' in self.df.columns:
            insights['max_temperature'] = {
                'highest': self.df['MaxTemp'].max(),
                'lowest': self.df['MaxTemp'].min(),
                'average': self.df['MaxTemp'].mean()
            }
        
        if 'MinTemp' in self.df.columns:
            insights['min_temperature'] = {
                'highest': self.df['MinTemp'].max(),
                'lowest': self.df['MinTemp'].min(), 
                'average': self.df['MinTemp'].mean()
            }
        
        # Rainfall insights
        if 'Rainfall' in self.df.columns:
            insights['rainfall'] = {
                'total': self.df['Rainfall'].sum(),
                'average': self.df['Rainfall'].mean(),
                'max_single_day': self.df['Rainfall'].max(),
                'rainy_days': (self.df['Rainfall'] > 0).sum()
            }
        
        # Monthly insights (if analysis was performed)
        if self._monthly_stats is not None:
            insights['hottest_month'] = self._monthly_stats.idxmax()
            insights['coldest_month'] = self._monthly_stats.idxmin()
        
        print("=== WEATHER DATA INSIGHTS ===")
        for key, value in insights.items():
            print(f"{key}: {value}")
        
        return insights


def main():
    """
    Example usage of the WeatherAnalyzer class.
    
    This function demonstrates a complete weather data analysis workflow
    including data loading, exploration, visualization, and machine learning.
    """
    try:
        # Initialize analyzer
        analyzer = WeatherAnalyzer()
        
        # Load data
        analyzer.load_data('weather.csv')
        
        # Explore the data
        exploration = analyzer.explore_data()
        
        # Visualize correlations
        analyzer.visualize_correlations()
        
        # Analyze monthly trends
        monthly_trends = analyzer.analyze_monthly_trends()
        analyzer.plot_monthly_trends()
        
        # Machine learning prediction
        ml_metrics = analyzer.predict_rainfall()
        
        # Make a custom prediction
        prediction = analyzer.predict_custom(min_temp=15.0, max_temp=25.0)
        
        # Get comprehensive insights
        insights = analyzer.get_insights()
        
        print("\n=== ANALYSIS COMPLETE ===")
        print("All weather data analysis steps completed successfully!")
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        raise


if __name__ == "__main__":
    main()
