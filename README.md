# Heart Disease Predictor

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://heart-disease-predictor-by-tyhan.streamlit.app/)

An ML-powered Heart Disease Prediction Web App built with Python, Scikit-learn, and Streamlit.

## 🎯 Overview

This project leverages machine learning to predict the likelihood of heart disease based on patient health metrics and medical history. The application provides an interactive web interface for both data exploration and real-time predictions.

## ✨ Features

- **Interactive Web Interface**: Built with Streamlit for easy-to-use prediction interface
- **Machine Learning Model**: Trained with Scikit-learn using real-world health data
- **Real-time Predictions**: Get instant heart disease risk assessments
- **Data Visualization**: Explore patterns and relationships in health data
- **Jupyter Notebooks**: Complete analysis and model development documentation

## 🚀 Live Demo

Visit the live application here: [Heart Disease Predictor Web App](https://heart-disease-predictor-by-tyhan.streamlit.app/)

## 🛠️ Technology Stack

- **Backend**: Python 3.x
- **ML Framework**: Scikit-learn
- **Web Framework**: Streamlit
- **Data Analysis**: Jupyter Notebooks
- **Data Processing**: Pandas, NumPy

## 📊 Project Structure

```
heart-disease-predictor/
├── README.md                 # This file
├── notebooks/                # Jupyter notebooks for analysis & model development
├── data/                      # Dataset files
├── models/                    # Trained ML models
├── app.py                     # Streamlit application
└── requirements.txt           # Python dependencies
```

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/tyhan-data/heart-disease-predictor.git
   cd heart-disease-predictor
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Usage

### Run the Web App Locally

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Explore the Analysis

Open and run the Jupyter notebooks in the `notebooks/` directory to see the full data exploration, preprocessing, and model development pipeline.

## 📈 Model Information

- **Algorithm**: Classification model trained on cardiac health data
- **Features**: Patient health metrics including age, blood pressure, cholesterol, and more
- **Output**: Probability prediction of heart disease presence

## 🗂️ Language Composition

- **Jupyter Notebook**: 97.6%
- **Python**: 2.4%

## 📝 License

This project is open source and available for educational and research purposes.

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request with your improvements.

## 📧 Contact

For questions or feedback about this project, please open an issue in the repository.

---

**Made with ❤️ by [tyhan-data](https://github.com/tyhan-data)**
