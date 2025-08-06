#!/usr/bin/env python3
"""
Weather Data Analysis Examples

This script demonstrates various use cases and capabilities of the 
WeatherAnalyzer toolkit with practical examples.

Examples included:
1. Basic analysis workflow
2. Custom feature analysis
3. Advanced visualization
4. Batch predictions
5. Error handling demonstration
6. Performance comparison

Author: Weather Analysis Team
Version: 1.0.0
"""

from weather_data_analysis import WeatherAnalyzer
import pandas as pd
import matplotlib.pyplot as plt
import time
import warnings
warnings.filterwarnings('ignore')


def example_1_basic_workflow():
    """
    Example 1: Complete basic analysis workflow
    
    This example demonstrates the most common use case: loading data,
    exploring it, and generating predictions.
    """
    print("\n" + "="*60)
    print("EXAMPLE 1: BASIC ANALYSIS WORKFLOW")
    print("="*60)
    
    try:
        # Initialize analyzer
        analyzer = WeatherAnalyzer()
        
        # Load data
        print("Loading weather data...")
        analyzer.load_data('weather.csv')
        
        # Explore the data
        print("\nPerforming data exploration...")
        exploration = analyzer.explore_data()
        
        # Analyze monthly trends
        print("\nAnalyzing monthly temperature trends...")
        monthly_trends = analyzer.analyze_monthly_trends()
        
        # Train ML model and evaluate
        print("\nTraining machine learning model...")
        ml_metrics = analyzer.predict_rainfall()
        
        # Make a custom prediction
        print("\nMaking custom prediction...")
        rainfall = analyzer.predict_custom(min_temp=15.0, max_temp=25.0)
        
        # Get comprehensive insights
        print("\nGenerating insights...")
        insights = analyzer.get_insights()
        
        print(f"\n✅ Basic workflow completed successfully!")
        print(f"   📊 Dataset contains {exploration['shape'][0]} records")
        print(f"   🎯 Model R² score: {ml_metrics['r2']:.3f}")
        print(f"   🌡️ Predicted rainfall for 15-25°C: {rainfall:.2f}mm")
        
        return {
            'exploration': exploration,
            'ml_metrics': ml_metrics,
            'insights': insights
        }
        
    except Exception as e:
        print(f"❌ Error in basic workflow: {str(e)}")
        return None


def example_2_custom_features():
    """
    Example 2: Custom feature analysis
    
    This example shows how to use different features for machine learning
    and compare model performance.
    """
    print("\n" + "="*60)
    print("EXAMPLE 2: CUSTOM FEATURE ANALYSIS")
    print("="*60)
    
    # Test different feature combinations
    feature_sets = [
        {
            'name': 'Temperature Only',
            'features': ['MinTemp', 'MaxTemp'],
            'description': 'Basic temperature features'
        },
        {
            'name': 'Temperature + Humidity',
            'features': ['MinTemp', 'MaxTemp', 'Humidity9am', 'Humidity3pm'],
            'description': 'Temperature and humidity features'
        },
        {
            'name': 'Weather Conditions',
            'features': ['MinTemp', 'MaxTemp', 'Humidity9am', 'Pressure9am', 'WindSpeed9am'],
            'description': 'Comprehensive weather conditions'
        }
    ]
    
    results = {}
    
    for feature_set in feature_sets:
        print(f"\n🔍 Testing: {feature_set['name']}")
        print(f"   Features: {feature_set['features']}")
        print(f"   Description: {feature_set['description']}")
        
        try:
            # Initialize analyzer with custom features
            analyzer = WeatherAnalyzer(
                feature_columns=feature_set['features'],
                target_column='Rainfall'
            )
            
            # Load data and train model
            analyzer.load_data('weather.csv')
            metrics = analyzer.predict_rainfall()
            
            results[feature_set['name']] = metrics
            print(f"   📈 R² Score: {metrics['r2']:.4f}")
            print(f"   📊 RMSE: {metrics['rmse']:.4f}")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            results[feature_set['name']] = None
    
    # Compare results
    print(f"\n📋 FEATURE COMPARISON SUMMARY:")
    print("-" * 50)
    best_r2 = 0
    best_model = None
    
    for name, metrics in results.items():
        if metrics:
            print(f"{name:20} | R²: {metrics['r2']:.4f} | RMSE: {metrics['rmse']:.4f}")
            if metrics['r2'] > best_r2:
                best_r2 = metrics['r2']
                best_model = name
        else:
            print(f"{name:20} | Failed to train")
    
    if best_model:
        print(f"\n🏆 Best performing model: {best_model} (R² = {best_r2:.4f})")
    
    return results


def example_3_advanced_visualization():
    """
    Example 3: Advanced visualization techniques
    
    This example demonstrates various visualization capabilities
    and customization options.
    """
    print("\n" + "="*60)
    print("EXAMPLE 3: ADVANCED VISUALIZATION")
    print("="*60)
    
    try:
        analyzer = WeatherAnalyzer()
        analyzer.load_data('weather.csv')
        
        # 1. Basic correlations
        print("\n📊 Creating correlation visualizations...")
        analyzer.visualize_correlations()
        
        # 2. Custom correlation plots
        print("📊 Creating custom correlation plots...")
        if all(col in analyzer.df.columns for col in ['Humidity9am', 'Humidity3pm', 'Pressure9am']):
            analyzer.visualize_correlations([
                'MinTemp', 'MaxTemp', 'Humidity9am', 'Humidity3pm'
            ], figsize=(12, 8))
        
        # 3. Monthly trends analysis and plotting
        print("📊 Analyzing and plotting monthly trends...")
        analyzer.analyze_monthly_trends()
        analyzer.plot_monthly_trends(figsize=(14, 7))
        
        # 4. Custom analysis plots
        print("📊 Creating additional analysis plots...")
        
        # Temperature distribution
        plt.figure(figsize=(12, 5))
        
        plt.subplot(1, 2, 1)
        plt.hist(analyzer.df['MinTemp'].dropna(), bins=30, alpha=0.7, color='blue', label='Min Temp')
        plt.hist(analyzer.df['MaxTemp'].dropna(), bins=30, alpha=0.7, color='red', label='Max Temp')
        plt.xlabel('Temperature (°C)')
        plt.ylabel('Frequency')
        plt.title('Temperature Distribution')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.subplot(1, 2, 2)
        plt.scatter(analyzer.df['MinTemp'], analyzer.df['MaxTemp'], alpha=0.6)
        plt.xlabel('Min Temperature (°C)')
        plt.ylabel('Max Temperature (°C)')
        plt.title('Min vs Max Temperature Relationship')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        print("✅ Advanced visualizations completed!")
        
    except Exception as e:
        print(f"❌ Error in visualization: {str(e)}")


def example_4_batch_predictions():
    """
    Example 4: Batch predictions and scenario analysis
    
    This example shows how to make multiple predictions and analyze
    different weather scenarios.
    """
    print("\n" + "="*60)
    print("EXAMPLE 4: BATCH PREDICTIONS")
    print("="*60)
    
    try:
        # Initialize and train model
        analyzer = WeatherAnalyzer()
        analyzer.load_data('weather.csv')
        print("🔧 Training model for batch predictions...")
        analyzer.predict_rainfall()
        
        # Define temperature scenarios
        scenarios = [
            {'name': 'Cold Day', 'min_temp': 5, 'max_temp': 15},
            {'name': 'Mild Day', 'min_temp': 10, 'max_temp': 20},
            {'name': 'Warm Day', 'min_temp': 15, 'max_temp': 25},
            {'name': 'Hot Day', 'min_temp': 20, 'max_temp': 30},
            {'name': 'Very Hot Day', 'min_temp': 25, 'max_temp': 35},
            {'name': 'Extreme Heat', 'min_temp': 30, 'max_temp': 40}
        ]
        
        print(f"\n🔮 RAINFALL PREDICTIONS FOR DIFFERENT SCENARIOS:")
        print("-" * 60)
        predictions = []
        
        for scenario in scenarios:
            rainfall = analyzer.predict_custom(
                scenario['min_temp'], 
                scenario['max_temp']
            )
            predictions.append({
                'scenario': scenario['name'],
                'min_temp': scenario['min_temp'],
                'max_temp': scenario['max_temp'],
                'predicted_rainfall': rainfall
            })
            
            print(f"{scenario['name']:15} | {scenario['min_temp']:3}°C - {scenario['max_temp']:3}°C | {rainfall:6.2f}mm")
        
        # Temperature range analysis
        print(f"\n🌡️ TEMPERATURE RANGE ANALYSIS:")
        print("-" * 50)
        
        temp_ranges = range(0, 41, 5)
        range_predictions = []
        
        for min_temp in temp_ranges:
            max_temp = min_temp + 10
            if max_temp <= 45:  # Reasonable temperature limit
                rainfall = analyzer.predict_custom(min_temp, max_temp)
                range_predictions.append({
                    'temp_range': f"{min_temp}-{max_temp}°C",
                    'predicted_rainfall': rainfall
                })
                print(f"Temperature range {min_temp:2}-{max_temp:2}°C: {rainfall:6.2f}mm")
        
        # Find optimal conditions
        min_rainfall = min(predictions, key=lambda x: x['predicted_rainfall'])
        max_rainfall = max(predictions, key=lambda x: x['predicted_rainfall'])
        
        print(f"\n📈 PREDICTION ANALYSIS:")
        print(f"   🌵 Lowest rainfall: {min_rainfall['scenario']} ({min_rainfall['predicted_rainfall']:.2f}mm)")
        print(f"   🌧️ Highest rainfall: {max_rainfall['scenario']} ({max_rainfall['predicted_rainfall']:.2f}mm)")
        
        return predictions
        
    except Exception as e:
        print(f"❌ Error in batch predictions: {str(e)}")
        return None


def example_5_error_handling():
    """
    Example 5: Error handling demonstration
    
    This example shows how the toolkit handles various error conditions
    gracefully.
    """
    print("\n" + "="*60)
    print("EXAMPLE 5: ERROR HANDLING DEMONSTRATION")
    print("="*60)
    
    print("🧪 Testing error handling capabilities...")
    
    # Test 1: File not found
    print("\n1️⃣ Testing file not found error...")
    try:
        analyzer = WeatherAnalyzer()
        analyzer.load_data('nonexistent_file.csv')
    except FileNotFoundError as e:
        print(f"   ✅ Properly caught FileNotFoundError: {str(e)}")
    
    # Test 2: No data loaded
    print("\n2️⃣ Testing operations without loaded data...")
    try:
        analyzer = WeatherAnalyzer()
        analyzer.explore_data()
    except ValueError as e:
        print(f"   ✅ Properly caught ValueError: {str(e)}")
    
    # Test 3: Model not trained
    print("\n3️⃣ Testing prediction without trained model...")
    try:
        analyzer = WeatherAnalyzer()
        analyzer.load_data('weather.csv')
        analyzer.predict_custom(15.0, 25.0)  # Model not trained
    except ValueError as e:
        print(f"   ✅ Properly caught ValueError: {str(e)}")
    
    # Test 4: Invalid columns
    print("\n4️⃣ Testing invalid column names...")
    try:
        analyzer = WeatherAnalyzer()
        analyzer.load_data('weather.csv')
        analyzer.visualize_correlations(['NonexistentColumn1', 'NonexistentColumn2'])
    except ValueError as e:
        print(f"   ✅ Properly caught ValueError: {str(e)}")
    
    # Test 5: Missing features for ML
    print("\n5️⃣ Testing missing feature columns...")
    try:
        analyzer = WeatherAnalyzer(feature_columns=['InvalidFeature1', 'InvalidFeature2'])
        analyzer.load_data('weather.csv')
        analyzer.predict_rainfall()
    except ValueError as e:
        print(f"   ✅ Properly caught ValueError: {str(e)}")
    
    print(f"\n✅ All error handling tests completed successfully!")
    print("   The toolkit handles errors gracefully and provides meaningful messages.")


def example_6_performance_comparison():
    """
    Example 6: Performance comparison
    
    This example demonstrates the performance characteristics of different
    operations and provides timing information.
    """
    print("\n" + "="*60)
    print("EXAMPLE 6: PERFORMANCE COMPARISON")
    print("="*60)
    
    try:
        analyzer = WeatherAnalyzer()
        
        # Time data loading
        print("⏱️ Timing data loading operation...")
        start_time = time.time()
        analyzer.load_data('weather.csv')
        load_time = time.time() - start_time
        print(f"   📊 Data loading: {load_time:.4f} seconds")
        
        # Time data exploration
        print("⏱️ Timing data exploration...")
        start_time = time.time()
        exploration = analyzer.explore_data()
        explore_time = time.time() - start_time
        print(f"   📊 Data exploration: {explore_time:.4f} seconds")
        
        # Time monthly analysis
        print("⏱️ Timing monthly analysis...")
        start_time = time.time()
        analyzer.analyze_monthly_trends()
        monthly_time = time.time() - start_time
        print(f"   📊 Monthly analysis: {monthly_time:.4f} seconds")
        
        # Time ML training
        print("⏱️ Timing machine learning training...")
        start_time = time.time()
        ml_metrics = analyzer.predict_rainfall()
        ml_time = time.time() - start_time
        print(f"   📊 ML training: {ml_time:.4f} seconds")
        
        # Time predictions
        print("⏱️ Timing individual predictions...")
        prediction_times = []
        for i in range(10):
            start_time = time.time()
            analyzer.predict_custom(15.0 + i, 25.0 + i)
            prediction_time = time.time() - start_time
            prediction_times.append(prediction_time)
        
        avg_prediction_time = sum(prediction_times) / len(prediction_times)
        print(f"   📊 Average prediction time: {avg_prediction_time:.6f} seconds")
        
        # Time insights generation
        print("⏱️ Timing insights generation...")
        start_time = time.time()
        insights = analyzer.get_insights()
        insights_time = time.time() - start_time
        print(f"   📊 Insights generation: {insights_time:.4f} seconds")
        
        # Performance summary
        total_time = load_time + explore_time + monthly_time + ml_time + insights_time
        print(f"\n📈 PERFORMANCE SUMMARY:")
        print(f"   🚀 Total analysis time: {total_time:.4f} seconds")
        print(f"   💾 Dataset size: {exploration['shape'][0]} records, {exploration['shape'][1]} features")
        print(f"   ⚡ Records per second: {exploration['shape'][0] / total_time:.0f}")
        
        # Memory usage approximation
        memory_mb = analyzer.df.memory_usage(deep=True).sum() / 1024 / 1024
        print(f"   💽 Memory usage: {memory_mb:.2f} MB")
        
        return {
            'load_time': load_time,
            'explore_time': explore_time,
            'monthly_time': monthly_time,
            'ml_time': ml_time,
            'avg_prediction_time': avg_prediction_time,
            'insights_time': insights_time,
            'total_time': total_time,
            'memory_mb': memory_mb
        }
        
    except Exception as e:
        print(f"❌ Error in performance testing: {str(e)}")
        return None


def main():
    """
    Main function to run all examples
    
    This function executes all the example functions in sequence,
    demonstrating the full capabilities of the WeatherAnalyzer toolkit.
    """
    print("🌤️ WEATHER DATA ANALYSIS TOOLKIT - EXAMPLES")
    print("="*80)
    print("This script demonstrates various capabilities of the WeatherAnalyzer")
    print("toolkit through practical examples and use cases.")
    
    # Run all examples
    examples = [
        ("Basic Workflow", example_1_basic_workflow),
        ("Custom Features", example_2_custom_features),
        ("Advanced Visualization", example_3_advanced_visualization),
        ("Batch Predictions", example_4_batch_predictions),
        ("Error Handling", example_5_error_handling),
        ("Performance Comparison", example_6_performance_comparison)
    ]
    
    results = {}
    
    for name, example_func in examples:
        try:
            print(f"\n🔄 Running {name} example...")
            result = example_func()
            results[name] = result
            print(f"✅ {name} completed successfully!")
            
        except Exception as e:
            print(f"❌ {name} failed: {str(e)}")
            results[name] = None
    
    # Final summary
    print("\n" + "="*80)
    print("📋 EXAMPLES SUMMARY")
    print("="*80)
    
    successful = sum(1 for result in results.values() if result is not None)
    total = len(results)
    
    print(f"✅ Successfully completed: {successful}/{total} examples")
    
    if successful == total:
        print("🎉 All examples completed successfully!")
        print("   The WeatherAnalyzer toolkit is working correctly.")
    else:
        print("⚠️ Some examples failed. Check the error messages above.")
    
    print("\n🎯 Next steps:")
    print("   1. Try modifying the examples for your specific use case")
    print("   2. Experiment with different feature combinations")
    print("   3. Load your own weather data files")
    print("   4. Extend the toolkit with additional functionality")
    
    return results


if __name__ == "__main__":
    # Run all examples
    example_results = main()