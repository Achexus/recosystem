# 🎬 Smart Movie Recommendation Engine

This project is an **Item-Based Collaborative Filtering** recommendation engine that uses the **MovieLens 100k** dataset to help users discover new movies based on their preferences. 

The project is designed with a modular architecture in accordance with modern software engineering practices and features a visual web interface built with **Streamlit** for seamless user interaction.

---

## 🚀 Features

* **Automated Data Pipeline:** Downloads, extracts, and cleans the MovieLens dataset with a single command.
* **Smart Algorithm:** Calculates mathematical similarities between movies using the Pearson Correlation Coefficient.
* **Advanced Search Box:** Provides a clean interface that allows users to instantly search through thousands of movies by typing.
* **Modular Architecture:** Data extraction, preprocessing, modeling, and interface layers work completely independent of each other.

---

## 📁 Project Structure

```text
recosystem/
├── data/
│   ├── raw/          # Raw data downloaded from the source
│   └── processed/    # Cleaned CSV files ready for analysis
├── src/
│   ├── __init__.py   # Python package identifier
│   ├── data/         # Data downloading and preprocessing scripts
│   └── models/       # Mathematical model of the recommendation engine (Pearson)
├── app.py            # Streamlit Web Interface
├── requirements.txt  # Project dependencies (libraries)
└── .gitignore        # Git untracked files (datasets and virtual environments)

"In this project, I took my first steps into data science. Since I am new to this field, I got a lot of help from AI to guide me."