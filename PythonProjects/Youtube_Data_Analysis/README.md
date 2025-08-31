# YouTube Data Analysis Project
![](youtubelogo.webp)

## Overview
This project performs comprehensive sentiment analysis on YouTube comments from US users. The analysis includes sentiment polarity scoring, word cloud visualization, and emoji usage patterns to understand viewer engagement and emotional responses.

## Features
- **Sentiment Analysis**: Uses TextBlob to calculate polarity scores for each comment
- **Word Cloud Generation**: Creates visual representations of most frequent words in positive and negative comments
- **Emoji Analysis**: Identifies and visualizes the most commonly used emojis in comments
- **Data Cleaning**: Handles missing values and malformed data entries

## Dataset
- **File**: `UScomments.csv`
- **Source**: YouTube comments from US users
- **Size**: The analysis processes the complete dataset with optional sampling for performance optimization

## Technologies Used
- **Python 3.x**
- **Libraries**:
  - `pandas` - Data manipulation and analysis
  - `numpy` - Numerical computing
  - `matplotlib` & `seaborn` - Data visualization
  - `textblob` - Natural language processing and sentiment analysis
  - `wordcloud` - Word cloud generation
  - `emoji` - Emoji detection and analysis
  - `plotly` - Interactive visualizations
  - `collections` - Data counting and frequency analysis

## Installation

### Prerequisites
Make sure you have Python 3.x installed on your system.

### Required Libraries
Install the required libraries using pip:

```bash
pip install pandas numpy seaborn matplotlib textblob wordcloud emoji plotly
```

## Usage

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/Youtube_Data_Analysis.git
   cd Youtube_Data_Analysis
   ```

2. **Prepare your data**:
   - Ensure `UScomments.csv` is in the project directory
   - The CSV should contain a `comment_text` column with YouTube comments

3. **Run the analysis**:
   ```bash
   python youtube_analysis.py
   ```

## Project Structure
```
Youtube_Data_Analysis/
│
├── UScomments.csv          # Dataset file
├── youtube_analysis.py     # Main analysis script
├── README.md              # Project documentation
└── requirements.txt       # Python dependencies
```

## Analysis Workflow

### 1. Data Loading & Cleaning
- Loads YouTube comments dataset
- Handles malformed lines with `on_bad_lines='skip'`
- Removes null values to ensure data quality

### 2. Sentiment Analysis
- Calculates sentiment polarity for each comment using TextBlob
- Polarity ranges from -1 (negative) to 1 (positive)
- Separates comments into positive and negative categories
- Handles exceptions gracefully by assigning neutral polarity (0)

### 3. Word Cloud Analysis
- Generates separate word clouds for positive and negative comments
- Filters out common stop words
- Provides visual insights into frequently used terms

### 4. Emoji Analysis
- Extracts all emojis from comments
- Counts frequency of each emoji
- Creates interactive bar charts showing top 10 most used emojis

## Key Insights

### Positive Comments
The word cloud analysis reveals that positive comments frequently contain words like:
- "best", "awesome", "perfect", "amazing"
- "look", "happy"
- Other positive descriptors

### Negative Comments
Negative sentiment analysis helps identify areas of concern or dissatisfaction among viewers.

### Emoji Usage
The emoji analysis provides insights into emotional expressions and popular symbols used by the YouTube community.

## Results and Visualizations
The project generates several visualizations:
1. Word clouds for positive and negative sentiments
2. Interactive bar chart of most common emojis
3. Distribution of sentiment polarity scores


## Future Enhancements
- **Advanced NLP**: Implement more sophisticated sentiment analysis models
- **Topic Modeling**: Identify key themes in comments using LDA or similar techniques
- **Time Series Analysis**: Analyze sentiment trends over time
- **Comparative Analysis**: Compare sentiment across different video categories
- **Machine Learning**: Build predictive models for comment sentiment

## Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-analysis`)
3. Commit your changes (`git commit -am 'Add new analysis feature'`)
4. Push to the branch (`git push origin feature/new-analysis`)
5. Create a Pull Request


## Contact
**Your Name** - your.email@example.com
Project Link: [https://github.com/GunjanKhatrii/Youtube_Data_Analysis](https://github.com/GunjanKhatrii/Youtube_Data_Analysis)

## Acknowledgments
- TextBlob library for sentiment analysis capabilities
- WordCloud library for text visualization
- YouTube for providing the data platform
- The open-source community for the tools and libraries used

---
*This project is part of a data science learning journey focused on natural language processing and social media analytics.*
