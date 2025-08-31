# COVID-19 Trend Analysis Project

## Overview
This project analyzes COVID-19 trends using historical data to visualize the progression of confirmed cases, deaths, and recoveries across different countries and globally. The analysis provides insights into the pandemic's impact through data cleaning, aggregation, and comprehensive visualization.

## Features
- **Data Preprocessing**: Cleans and standardizes COVID-19 dataset
- **Country-wise Analysis**: Individual trend analysis for each affected country
- **Global Trend Visualization**: Worldwide COVID-19 progression analysis
- **Multi-metric Tracking**: Simultaneous analysis of confirmed cases, deaths, and recoveries
- **Missing Data Handling**: Robust imputation strategies for incomplete data
- **Interactive Visualizations**: Scatter plots showing temporal trends

## Dataset
- **File**: `covid_19_data.csv`
- **Source**: COVID-19 historical data
- **Metrics**: Confirmed cases, Deaths, Recovered cases
- **Scope**: Global data with country and date-wise breakdown

## Technologies Used
- **Python 3.x**
- **Libraries**:
  - `pandas` - Data manipulation and analysis
  - `numpy` - Numerical computing
  - `matplotlib` - Data visualization and plotting
  - `sklearn.impute.SimpleImputer` - Missing data imputation

## Installation

### Prerequisites
Ensure you have Python 3.x installed on your system.

### Required Libraries
Install the required libraries using pip:

```bash
pip install pandas numpy matplotlib scikit-learn
```

## Usage

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/Covid19_Trend_Analysis.git
   cd Covid19_Trend_Analysis
   ```

2. **Prepare your data**:
   - Place `covid_19_data.csv` in the project directory
   - Ensure the CSV contains columns: Date, Country/Region, Province/State, Confirmed, Deaths, Recovered

3. **Run the analysis**:
   ```bash
   python covid_analysis.py
   ```

## Project Structure
```
Covid19_Trend_Analysis/
│
├── covid_19_data.csv       # COVID-19 dataset
├── covid_analysis.py       # Main analysis script
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
└── visualizations/        # Generated plots and charts
```

## Analysis Workflow

### 1. Data Loading & Preprocessing
- Loads COVID-19 dataset from CSV file
- Removes unnecessary columns (`SNo`, `Last Update`)
- Standardizes column names for better readability
- Converts date strings to datetime objects for time series analysis

### 2. Data Cleaning & Imputation
- Handles missing values using SimpleImputer with constant strategy
- Ensures data consistency across all records
- Maintains data integrity while filling gaps

### 3. Data Aggregation
- **Country-level aggregation**: Groups data by country and date
- **Global aggregation**: Combines all countries for worldwide trends
- **Filtering**: Focuses on countries with significant case numbers (>100 confirmed cases, >10 deaths)

### 4. Visualization Generation
- **Individual Country Plots**: Separate scatter plots for each country showing:
  - Confirmed cases (blue)
  - Recovered cases (green)
  - Deaths (red)
- **Global Trend Plot**: Combined worldwide data visualization
- **Time Series Format**: X-axis represents days since first case, Y-axis shows case numbers

## Key Insights

### Country-wise Analysis
- Individual country trends reveal different pandemic trajectories
- Some countries show rapid growth followed by control measures impact
- Recovery patterns vary significantly between regions

### Global Trends
- Worldwide data shows the overall pandemic progression
- Helps identify global peaks and recovery periods
- Demonstrates the collective impact across all affected regions

## Visualization Features
- **Color-coded Metrics**: 
  - Blue: Confirmed cases
  - Green: Recovered cases  
  - Red: Deaths
- **Interactive Legends**: Easy identification of different metrics
- **Temporal Analysis**: Days-based progression tracking
- **Multiple Country Comparison**: Side-by-side country analysis

## Data Quality Measures
- **Missing Value Treatment**: Uses constant imputation strategy
- **Data Validation**: Filters out countries with minimal impact for focused analysis
- **Date Standardization**: Ensures consistent temporal analysis
- **Outlier Handling**: Robust aggregation methods

## Performance Considerations
- **Memory Optimization**: Efficient groupby operations for large datasets
- **Visualization Scaling**: Handles multiple country plots systematically
- **Data Processing**: Streamlined pipeline for quick analysis

## Future Enhancements
- **Advanced Modeling**: Implement predictive models for trend forecasting
- **Interactive Dashboards**: Create web-based interactive visualizations
- **Statistical Analysis**: Add correlation analysis between metrics
- **Geographical Mapping**: Include map-based visualizations
- **Vaccination Data**: Integrate vaccination rates for comprehensive analysis
- **Economic Impact**: Correlate health data with economic indicators
- **Real-time Updates**: Implement automated data fetching and updates

## Sample Results
The analysis generates visualizations showing:
1. Individual country trend plots (one per country)
2. Global COVID-19 progression chart
3. Comparative analysis of confirmed vs recovered vs deaths

## Data Sources & Methodology
- Uses historical COVID-19 data with daily updates
- Focuses on three key metrics for comprehensive health impact assessment
- Employs time series analysis techniques for trend identification

## Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-analysis`)
3. Commit your changes (`git commit -am 'Add new analysis feature'`)
4. Push to the branch (`git push origin feature/new-analysis`)
5. Create a Pull Request


## Contact 
Project Link: [https://github.com/GunjanKhatrii/Covid19TrendAnalysis](https://github.com/GunjanKhatrii/Covid19TrendAnalysis)

## Acknowledgments
- World Health Organization (WHO) for COVID-19 data standards
- Johns Hopkins University for maintaining comprehensive COVID-19 datasets
- The global health community for data collection efforts
- Open-source Python community for analytical tools

## Disclaimer
This analysis is for educational and research purposes. For official COVID-19 information and health guidance, please consult official health authorities and medical professionals.

---
*This project demonstrates data science techniques applied to public health data analysis and epidemiological trend identification.*
