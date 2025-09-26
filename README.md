🎲 Powerball Analysis & Prediction (Educational)

This project analyzes historical Powerball draw data and produces insights such as hot/cold numbers, frequency charts, and weighted random predictions for upcoming draws.
⚠️ Note: Powerball results are random — this project is for educational and exploratory purposes only, not guaranteed predictions.

✨ Features

📊 Data Cleaning

Parses raw CSV from official results

Extracts main numbers, Powerball, and draw date

Removes incomplete rows and sorts by time

🔍 Frequency Analysis

Counts how often each number appears

Identifies hot (frequent) and cold (rare) numbers

Provides Powerball frequency distribution

📈 Visualizations

Bar charts for main numbers and Powerballs

🎯 Weighted Predictions

Generates “predicted” tickets based on historical frequency

Supports recent-window analysis (e.g., last 200 draws)

Multiple ticket generator

💾 Outputs

Saves cleaned dataset (powerball_clean.csv)

Saves frequency tables for reuse (freq_main_full.csv, freq_powerball_full.csv)

🚀 Getting Started
1. Clone the repo
git clone https://github.com/yourusername/powerball-analysis.git
cd powerball-analysis

2. Install requirements

This project uses Python 3.x.
Install dependencies:

pip install pandas matplotlib numpy

3. Run in Jupyter / Colab

If using Google Colab, just upload your dataset and run the notebook.

📂 File Structure
powerball-analysis/
│
├── powerball_analysis.ipynb   # Notebook version (recommended for Colab)
├── powerball_analysis.py      # Script version
├── README.md                  # This file
├── powerball_clean.csv        # Saved cleaned dataset
├── freq_main_full.csv         # Frequency of main numbers
└── freq_powerball_full.csv    # Frequency of Powerball numbers

📊 Example Outputs

Frequency of Main Numbers


Frequency of Powerball Numbers


Sample Prediction

Full-history weighted pick:
Main: [7, 14, 22, 36, 52] | Powerball: 24

🧑‍💻 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you’d like to change.

⚠️ Disclaimer

This project is not a lottery predictor. It’s meant for data science practice and visualization.
Use it to learn — not as a betting strategy.
