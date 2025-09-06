# Housing Market Prediction (C# + Embedded Python)

An educational demo showing how a .NET 9 worker hosts embedded Python (via CSnakes) to perform basic exploratory data analysis and train baseline regression models (SVR, Random Forest, Linear Regression) on a housing prices dataset. Plots are generated headlessly and saved as images; model performance is printed as Mean Absolute Percentage Error (MAPE).

> Python feature engineering + model flow is adapted (and simplified) from the public tutorial:  
> House Price Prediction Using Machine Learning in Python (GeeksforGeeks)  
> https://www.geeksforgeeks.org/machine-learning/house-price-prediction-using-machine-learning-in-python/  
> This repository re-hosts the concept inside a .NET environment; code has been refactored for embedding, plotting to files, and concise baseline modeling.

---

## ✨ Features
- .NET 9 + embedded Python 3.12 (auto-created virtual environment)
- Reads Excel dataset (`HousePricePrediction.xlsx`) from disk (loaded as bytes in C#)
- Quick exploratory data analysis:
  - Correlation heatmap
  - Unique categorical counts
  - Per-category distributions
- One-hot encoding of categorical variables
- Three baseline regression models
- MAPE evaluation printed to console
- All plots saved to PNG (non-interactive backend)

---

## 🖼 Headless Matplotlib (`matplotlib.use("Agg")`)
Because Python runs on a background (non-UI) thread inside the .NET host, interactive backends (TkAgg/Qt) would warn:

```
UserWarning: Starting a Matplotlib GUI outside of the main thread will likely fail.
```

To prevent GUI issues and still generate plots, the script uses the non-interactive `Agg` backend. Resulting images:
- `correlation_heatmap.png`
- `categorical_unique_values.png`
- `categorical_features_distribution.png`

Open them manually after execution.

---

## 🚀 Quick Start
1. **Prerequisites**: Ensure you have the .NET 9 SDK and Visual Studio 2022 (latest) installed.
2. **Clone the repo** and navigate to the project directory.
3. **Place the data file**: Add `HousePricePrediction.xlsx` to the project root (where `Program.cs` is).
4. **First run**: Execute the project to auto-create a Python virtual environment and install dependencies.

**Run Options**:
- **Visual Studio**: Build Solution then Start Debugging (F5) or Start Without Debugging (Ctrl+F5).
- **CLI**: Execute `dotnet run --project Housing_Market_Prediction`.

Check the console and project directory for output artifacts and metrics.

---

## 📂 Project Layout
.
├─ Program.cs                # Host + Python environment setup + file dispatch  
├─ data_processor.py         # EDA, preprocessing, modeling  
├─ requirements.txt          # Python dependencies  
├─ HousePricePrediction.xlsx # Input dataset (supply locally)  
├─ *.png                     # Generated artifacts (after run)  
└─ README.md

---

## 🔄 Processing Pipeline
Load Excel → Inspect dtypes → Generate plots → Clean/Impute → One-Hot Encode categoricals → Train/Test Split → Train SVR / RandomForest / LinearRegression → Print MAPE metrics

---

## 📊 Models & Metric
| Model | Notes |
|-------|-------|
| SVR | Non-linear kernel baseline |
| Random Forest | Fast ensemble, low tuning here |
| Linear Regression | Interpretable baseline |

Metric: `mean_absolute_percentage_error` (lower is better). For robustness consider also MAE / RMSE.

---

## 🚀 Setup
Prerequisites:
- .NET 9 SDK
- Visual Studio 2022 (current updates)

No global Python installation required—the redistributable and virtual environment are provisioned automatically on first run.

---

## ▶ Running
Visual Studio:
1. Place `HousePricePrediction.xlsx` alongside `Program.cs`.
2. Build (__Build Solution__).
3. Run (__Start Debugging__ or __Start Without Debugging__).

CLI:
1. Ensure you have the .NET 9 SDK installed.
2. Clone the repo and navigate to the project directory.
3. Place `HousePricePrediction.xlsx` in the project root.
4. Run `dotnet run --project Housing_Market_Prediction`.

Outputs (plots, metrics) will be in the project directory post-execution.

---

## 🔧 Troubleshooting
| Issue | Fix |
|-------|-----|
| Plots not showing | Intentional—open the generated PNG files |
| Missing dataset | Ensure `HousePricePrediction.xlsx` is in project root |
| Bad dependency state | Delete `.venv` folder and re-run |
| Want interactive plots | Would require main-thread execution & removing `matplotlib.use("Agg")` |
| Encoding explosion | Limit categories or use target/frequency encoding (not implemented here) |

---

## 💡 Extension Ideas
- Hyperparameter tuning (`GridSearchCV` / `RandomizedSearchCV`)
- Additional metrics (MAE, RMSE, R²)
- Model persistence (`joblib.dump`) + loading from C#
- Logging via Python `logging` -> forward to .NET
- Feature scaling + pipeline abstractions
- Train/validation leakage checks
- CLI argument for dataset path

---

## ⚠ Disclaimer
This is a learning/demo setup—no production hardening, performance optimization, or rigorous validation included. Python modeling approach conceptually follows (but does not verbatim copy) the referenced GeeksforGeeks tutorial; adaptations were made for embedding and environment constraints.

---

Enjoy exploring the bridge between .NET and Python.

