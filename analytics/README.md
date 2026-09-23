# Analytics Module

This analytics module explores the Titanic dataset to perform exploratory data analysis (EDA), statistical interpretation, and data visualization. The project is designed to understand how passenger characteristics relate to survival outcomes and to demonstrate practical Python skills in data cleaning and analytics.

## Dataset used

The project uses the Titanic dataset, which contains passenger-level information including demographics, ticket information, and survival status. The dataset is loaded from Seaborn and then stored locally in the analytics folder for further processing.

The files generated in the analytics source folder include:

- `analytics/src/titanic.csv` — raw dataset saved as a CSV file
- `analytics/src/titanic_cleaned.csv` — cleaned version after missing values and redundant columns are handled

The dataset includes features such as:

- `age`
- `fare`
- `sex`
- `pclass`
- `survived`
- `embarked`
- `embark_town`
- `alone`
- `sibsp`
- `parch`

## Project objective

The main objective of this module is to analyze and interpret passenger data to answer critical questions such as:

- What is the age and fare distribution of passengers?
- Are there abnormal values or outliers in the dataset?
- Which age groups were most common on the ship?
- Did women have a higher chance of survival than men?
- Did passenger class influence survival outcomes?
- How do gender and class together affect survival probability?
- Which variables show the strongest relationships with each other?

## Key analysis steps

The script performs the following tasks:

1. Loads the Titanic dataset from Seaborn.
2. Displays the first rows, dataset shape, and summary statistics.
3. Checks missing values and data quality.
4. Saves the raw dataset as a CSV file.
5. Removes duplicate rows.
6. Cleans missing values in key columns such as `age`, `embarked`, and `embark_town`.
7. Drops unnecessary or redundant columns that add little analytical value.
8. Saves the cleaned dataset to `titanic_cleaned.csv`.
9. Visualizes the age and fare distributions using histograms.
10. Uses boxplots to identify age and fare outliers.
11. Applies the IQR method to detect outlier ranges.
12. Computes summary statistics such as mean, median, and mode.
13. Compares survival rates across gender and passenger class.
14. Evaluates combined survival patterns for sex and class.
15. Builds a correlation matrix for selected numerical variables.
16. Prints key findings and insights from the analysis.

## Data cleaning and preprocessing

Before the analysis begins, the dataset is processed to improve quality and consistency. This includes:

- removing duplicate entries
- dropping rows with missing `embarked` and `embark_town` values
- filling missing values in `age` with the mean age
- removing unnecessary columns like `deck`, `who`, `adult_male`, `class`, `alive`, and `embarked`
- saving the processed data to a cleaned CSV file for reuse

## Run the script

From the project root, run:

```bash
python analytics/src/analytics.py
```

## Generated outputs

The script produces several types of results, including:

- dataset summary and descriptive statistics
- printed missing-value information
- histograms for age and fare
- boxplots for outlier detection
- count of age and fare outliers
- comparisons of survival rate by gender
- comparisons of survival rate by passenger class
- combined analysis of gender and class survival
- correlation information between selected variables

## Expected insights

This project is expected to reveal key patterns such as:

- women had a higher survival rate than men
- first-class passengers had better survival outcomes than lower classes
- age and fare distributions are not perfectly symmetrical
- fare data contains extreme values that may be treated as outliers
- variables such as passenger class and fare are related to each other

## Notes

This module is an educational analytics exercise focused on practical data analysis using Python. It demonstrates how to clean, summarize, visualize, and interpret a dataset in a way that supports real business or research questions.
