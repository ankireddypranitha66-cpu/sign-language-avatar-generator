# 💳 Credit Card Fraud Detection

An end-to-end machine learning project that detects fraudulent credit card transactions in a **highly imbalanced** dataset (~0.17% fraud rate), from raw data through to a deployed, interactive **Streamlit** app.

The project covers the full ML lifecycle: exploratory data analysis, feature engineering, handling severe class imbalance with SMOTE, training and comparing multiple models, hyperparameter tuning with leakage-safe cross-validation, decision threshold optimization, and a real-time / batch scoring web app.

---

## 🎯 Problem Statement

Credit card fraud detection is a classic **imbalanced classification** problem: fraudulent transactions are extremely rare, but missing one is far costlier than a false alarm. A model that just predicts "genuine" for everything would be 99.83% accurate — and completely useless. This project is built around metrics and techniques that actually matter for this kind of problem: **PR-AUC**, **SMOTE**, and **threshold tuning**, rather than accuracy alone.

---

## 📊 Dataset

- **Source:** [Kaggle — Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
- **Size:** 284,807 transactions, 31 columns
- **Features:** `Time`, `Amount`, and 28 anonymized PCA components (`V1`–`V28`)
- **Target:** `Class` (1 = Fraud, 0 = Genuine)
- **Class balance:** ~0.17% fraud (492 fraudulent transactions out of 284,807)

> The raw `creditcard.csv` is not included in this repo due to size/licensing — download it from Kaggle and place it in `data/creditcard.csv` before running the notebooks.

---

## 🧠 Approach

| Stage | Notebook | What happens |
|---|---|---|
| 1. EDA | `01_EDA.ipynb` | Load & clean data, explore class imbalance, `Amount`/`Time` behavior, PCA feature distributions, correlations, outliers |
| 2. Preprocessing | `02_preprocessing.ipynb` | Feature engineering (`Hour`, `Amount_log`), leakage-safe train/test split, `RobustScaler`, SMOTE resampling |
| 3. Modelling | `03_modelling.ipynb` | Train & compare Logistic Regression, Random Forest, XGBoost baselines |
| 4. Evaluation | `04_evaluation.ipynb` | PR/ROC curves, hyperparameter tuning (SMOTE-inside-CV), decision threshold tuning, champion model selection |
| 5. App | `app.py` | Streamlit app for single-transaction and batch fraud scoring |

### Key design decisions

- **PR-AUC over ROC-AUC / accuracy** — with 0.17% fraud, ROC-AUC can look great even for a weak model, since true negatives dominate. Precision-Recall is the metric that actually reflects performance on the minority class.
- **SMOTE inside cross-validation, not before it** — resampling is refit inside every CV fold during hyperparameter search, so no synthetic information leaks into validation scores.
- **Threshold tuning, not just 0.5** — the default 0.5 decision threshold is rarely optimal for fraud detection. The final model uses a **Best-F2 threshold**, which favors recall over precision, since missing fraud is typically costlier than a false alarm.
- **Train/test split before any scaling or resampling** — the test set stays completely untouched and reflects the real-world imbalanced distribution, giving an honest read on production performance.

---

## 📈 Results
odel,Accuracy,Precision,Recall,F1,ROC_AUC,PR_AUC,Train_Time_sec
Random Forest,0.9995241955380115,0.925,0.7789473684210526,0.8457142857142858,0.9662988250311929,0.8196081679962277,154.21
XGBoost,0.9992951045007578,0.7835051546391752,0.8,0.7916666666666666,0.9701622770629774,0.8146311632861523,15.14
Logistic Regression,0.9741127127903288,0.05389610389610389,0.8736842105263158,0.10152905198776759,0.9629081662515365,0.6839717515374308,2.85


Three baseline models were trained on the SMOTE-balanced training set and evaluated on an untouched, real-world-imbalanced test set:
Baseline models were evaluated on the untouched, real-world-imbalanced test set. **Random Forest** had the strongest PR-AUC and was selected for tuning:

| Model | Precision | Recall | F1 | PR-AUC |
|---|---|---|---|---|
| Random Forest (baseline, threshold 0.5) | 0.925 | 0.779 | 0.846 | 0.820 |
| Random Forest (tuned, threshold 0.5) | 0.925 | 0.779 | 0.846 | 0.820 |
| **Random Forest (tuned, Best-F2 threshold 0.252)** | **0.821** | **0.821** | **0.821** | 0.820 |

*See `data/processed/model_comparison_baseline.csv` for the full Logistic Regression / Random Forest / XGBoost baseline comparison, and `data/processed/final_model_summary.csv` for the tuning progression above.*

*(Exact numbers are generated when you run the notebooks against the real dataset — see `data/processed/model_comparison_baseline.csv` and `data/processed/final_model_summary.csv` for your run's results.)*

The strongest baseline (by PR-AUC) was taken forward for **hyperparameter tuning** via `RandomizedSearchCV` over a `SMOTE + classifier` pipeline, then **threshold-tuned** to find the best trade-off between precision and recall for a fraud-detection use case.

### Visuals produced by the pipeline (`images/`)

- Class distribution & imbalance breakdown
- `Amount` / `Time` distributions by class
- Correlation heatmap & feature-target correlations
- PCA feature (`V1`–`V28`) distributions by class
- Outlier analysis on top discriminative features
- SMOTE before/after class balance
- Confusion matrices for every model
- Feature importances (Random Forest, XGBoost)
- PR & ROC curves (baseline comparison)
- Threshold tuning curve
- Confusion matrices at different decision thresholds

---

## 🖥️ The App

`app.py` is a Streamlit app with three pages:

- **Single Transaction** — manually enter transaction details (or load a demo example) and get an instant fraud probability, verdict, and gauge chart
- **Batch Upload** — upload a CSV of transactions, get every row scored, view flagged transactions, download results, and (if a `Class` column is present) see live precision/recall/F1 evaluation
- **Model Info** — champion model details, performance summary, and feature importances

The decision threshold is adjustable live via a sidebar slider, defaulting to the tuned Best-F2 threshold found in `04_evaluation.ipynb`.

---

## 🗂️ Project Structure

```
fraud-detection/
├── data/
│   ├── creditcard.csv              # (download from Kaggle, not included)
│   ├── creditcard_cleaned.csv      # produced by 01_EDA.ipynb
│   └── processed/                  # produced by 02_preprocessing.ipynb & 04_evaluation.ipynb
│       ├── scaler.pkl
│       ├── X_train_scaled.csv / y_train.csv
│       ├── X_train_resampled.csv / y_train_resampled.csv
│       ├── X_test_scaled.csv / y_test.csv
│       ├── model_comparison_baseline.csv
│       └── final_model_summary.csv
├── models/                         # produced by 03_modelling.ipynb & 04_evaluation.ipynb
│   ├── logistic_regression.pkl
│   ├── random_forest.pkl
│   ├── xgboost.pkl
│   ├── best_model.pkl              # tuned champion model
│   └── best_threshold.json         # chosen threshold + feature order
├── images/                         # all plots, produced by the notebooks
├── 01_EDA.ipynb
├── 02_preprocessing.ipynb
├── 03_modelling.ipynb
├── 04_evaluation.ipynb
├── app.py
└── README.md
```

---

## ⚙️ Setup & Usage

### 1. Clone / download this project

```bash
git clone <your-repo-url>
cd fraud-detection
```

### 2. Install dependencies

```bash
pip install pandas numpy matplotlib seaborn scikit-learn xgboost imbalanced-learn streamlit plotly joblib jupyter
```

### 3. Get the dataset

Download `creditcard.csv` from [Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) and place it in:

```
data/creditcard.csv
```

### 4. Run the notebooks — in order

```bash
jupyter notebook
```

Run each notebook fully, top to bottom, in this order:

1. `01_EDA.ipynb`
2. `02_preprocessing.ipynb`
3. `03_modelling.ipynb`
4. `04_evaluation.ipynb`

> ⏱️ Note: `04_evaluation.ipynb` runs a cross-validated hyperparameter search and can take a while depending on your machine. If it's very slow, reducing `n_iter` / `cv` folds and fixing `n_jobs` to a specific number (rather than `-1`) in that notebook's search cell speeds this up significantly on some setups.

### 5. Launch the app

```bash
streamlit run app.py
```

Then open the URL it prints (typically `http://localhost:8501`).

---

## 🛠️ Tech Stack

- **Data & ML:** Python, Pandas, NumPy, scikit-learn, XGBoost, imbalanced-learn
- **Visualization:** Matplotlib, Seaborn, Plotly
- **App:** Streamlit
- **Environment:** Jupyter Notebook

---

## 🔮 Possible Extensions

- Add SHAP/LIME explanations for individual predictions in the app
- Try additional models (LightGBM, CatBoost, a simple neural net / autoencoder)
- Add cost-sensitive learning (explicit false-positive vs. false-negative cost weighting) instead of F-beta threshold tuning
- Deploy the app publicly (Streamlit Community Cloud, Docker + cloud hosting)
- Add model monitoring / drift detection for a production setting

---

## 📄 License

This project uses the Kaggle Credit Card Fraud Detection dataset, released under the Open Database License (ODbL). Check Kaggle's dataset page for current license terms before any commercial use.
