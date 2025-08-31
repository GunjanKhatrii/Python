# Movie Recommendation System using LightFM

## Overview
This project implements a collaborative filtering-based movie recommendation system using the LightFM library and the MovieLens dataset. The system analyzes user preferences to predict and recommend movies that users are likely to enjoy based on similar user behavior patterns.

## Features
- **Collaborative Filtering**: Uses LightFM's WARP (Weighted Approximate-Rank Pairwise) loss function
- **Real Dataset**: Leverages the popular MovieLens dataset for training and testing
- **User-based Recommendations**: Generates personalized movie recommendations for individual users
- **Known vs Recommended**: Compares user's known preferences with model predictions
- **Scalable Architecture**: Handles large-scale user-item interaction matrices efficiently

## Dataset
- **Source**: MovieLens dataset (fetched automatically via LightFM)
- **Rating Threshold**: Minimum rating of 4.0 (focuses on positive interactions)
- **Users**: 943 unique users
- **Movies**: 1,682 unique movies
- **Training Data**: 49,906 user-movie interactions
- **Test Data**: 5,469 user-movie interactions

## Technologies Used
- **Python 3.x**
- **Libraries**:
  - `numpy` - Numerical computing and array operations
  - `lightfm` - Recommendation system framework
  - `lightfm.datasets` - Built-in dataset access

## Installation

### Prerequisites
Ensure you have Python 3.x installed on your system.

### Required Libraries
Install the required libraries using pip:

```bash
pip install numpy lightfm
```

## Usage

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/Movie_Recommendation_System.git
   cd Movie_Recommendation_System
   ```

2. **Run the recommendation system**:
   ```bash
   python movie_recommender.py
   ```

3. **Jupyter Notebook** (alternative):
   ```bash
   jupyter notebook movie_recommendation.ipynb
   ```

## Project Structure
```
Movie_Recommendation_System/
│
├── movie_recommender.py           # Main recommendation script
├── movie_recommendation.ipynb     # Jupyter notebook version
├── README.md                     # Project documentation
├── requirements.txt              # Python dependencies
└── outputs/                      # Sample recommendation outputs
```

## System Architecture

### 1. Data Preparation
- Fetches MovieLens dataset with minimum rating threshold
- Formats item labels for proper string representation
- Splits data into training and testing sets

### 2. Model Configuration
- **Algorithm**: LightFM with WARP loss function
- **Loss Function**: WARP (Weighted Approximate-Rank Pairwise) - optimized for top-N recommendations
- **Training Parameters**: 30 epochs with 2 threads for parallel processing

### 3. Recommendation Engine
- **Input**: User ID
- **Process**: Calculates prediction scores for all movies
- **Output**: Top-N ranked movie recommendations
- **Comparison**: Shows known preferences vs new recommendations

### 4. Evaluation Framework
- Compares known positive interactions with model predictions
- Provides transparency in recommendation reasoning
- Enables manual validation of recommendation quality

## Model Performance

### Training Details
- **Epochs**: 30 training iterations
- **Threads**: 2 parallel threads for efficient processing
- **Matrix Dimensions**: 943 users × 1,682 movies
- **Sparsity**: Handles sparse user-item interaction matrix effectively

### Sample Output
```
User 3
     Known positives:
        Star Wars (1977)
        Contact (1997)
        Stargate (1994)
     Recommended:
        Amadeus (1984)
        Casablanca (1942)
        L.A. Confidential (1997)
```

## Key Features Explained

### WARP Loss Function
- Optimized for ranking tasks
- Focuses on top recommendations rather than rating prediction
- Particularly effective for implicit feedback scenarios

### Collaborative Filtering Approach
- Learns from user behavior patterns
- Identifies similar users with comparable preferences
- Recommends items liked by similar users

### Sparse Matrix Handling
- Efficiently processes user-item interaction data
- Handles missing interactions (users who haven't rated certain movies)
- Scales well with increasing data size

## Use Cases
- **Personal Movie Recommendations**: Individual users seeking new movies
- **Streaming Platform Integration**: Backend for video streaming services
- **Market Research**: Understanding user preference patterns
- **Content Discovery**: Helping users explore diverse movie genres
- **A/B Testing**: Comparing recommendation algorithm performance

## Limitations & Considerations
- **Cold Start Problem**: New users with no rating history need alternative approaches
- **Popularity Bias**: May favor popular movies over niche content
- **Data Sparsity**: Limited by available user-item interactions
- **Temporal Aspects**: Doesn't account for changing user preferences over time

## Future Enhancements
- **Hybrid Models**: Combine collaborative and content-based filtering
- **Deep Learning Integration**: Implement neural collaborative filtering
- **Real-time Updates**: Enable incremental learning for new ratings
- **Content Features**: Incorporate movie metadata (genre, director, cast)
- **Evaluation Metrics**: Add precision@K, recall@K, and NDCG measurements
- **User Interface**: Build web application for interactive recommendations
- **A/B Testing Framework**: Compare different recommendation algorithms

## Performance Metrics
Future versions will include:
- **Precision@K**: Accuracy of top-K recommendations
- **Recall@K**: Coverage of relevant items in top-K recommendations
- **NDCG**: Normalized Discounted Cumulative Gain
- **AUC**: Area Under the ROC Curve

## Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/recommendation-improvement`)
3. Commit your changes (`git commit -am 'Add recommendation enhancement'`)
4. Push to the branch (`git push origin feature/recommendation-improvement`)
5. Create a Pull Request


## Contact
Project Link: [https://github.com/GunjanKhatrii/Recommendation_system](https://github.com/GunjanKhatrii/Recommendation_system)

## Acknowledgments
- **MovieLens**: University of Minnesota for providing the dataset
- **LightFM**: Microsoft Research for the recommendation framework
- **GroupLens Research**: For advancing recommendation system research
- **The collaborative filtering community**: For foundational algorithms and techniques

## References
- Koren, Y., Bell, R., & Volinsky, C. (2009). Matrix factorization techniques for recommender systems
- Hu, Y., Koren, Y., & Volinsky, C. (2008). Collaborative filtering for implicit feedback datasets
- LightFM Documentation: https://lyst.github.io/lightfm/docs/home.html

---
*This project demonstrates machine learning applications in recommendation systems and collaborative filtering techniques.*
