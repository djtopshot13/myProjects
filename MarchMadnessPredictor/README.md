- [**March Madness Predictor**](#march-madness-predictor)
  - [**Project Purpose**](#project-purpose)
  - [**Navigating the Repo**](#navigating-the-repo)
    - [**Data**](#data)
      - [**CurrentData**](#currentdata)
      - [**HistoricalData**](#historicaldata)
    - [**DataCleaning**](#datacleaning)
    - [**Modeling**](#modeling)
    - [**Testing**](#testing)
# **March Madness Predictor**
## **Project Purpose**
- This project is an attempt at predicting the March Madness NCAA tournament perfectly
- At the very least this is supposed to be more accurate than a person's surface-level analysis and projection
## **Navigating the Repo**
### **Data** 
- Houses all the data files that will be used for training the model
- Is essential to the success of this project
#### **CurrentData**
- Contains data files with stats from teams in the tournament from the current season 
- Used to predict likelihood of winners based on season stats and favorites of the match
#### **HistoricalData**
- Contains data files with stats from matchups in previous tournaments
- Used to predict likelihood of winners based on matchup trends (i.e. 6 seed vs 11 seed matchups usually lean toward the 11 seed)
### **DataCleaning**
- Uses python files to clean data
- Ensure data is ready to be used for training
### **Modeling**
- Contains files for prediction purposes
- Runs different model types, including XGBoost for one
### **Testing**
- Runs the model's projections over previous tournaments
- Compares the projection accuracy and saves the results to compare which models perform the best
