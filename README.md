# Airline Loyalty Retention Project

## Team Members
1. Kanishka Gupta (IIT Roorkee)
2. Anurag Sain (IIT Roorkee)

## Live Dashboard
Working Prototype: https://airline-loyalty-project-snvj4uwmy3ir8pevzy5tyw.streamlit.app/

## GitHub Repository
https://github.com/KanishkaGupta28/airline-loyalty-project

## Project Overview
This project analyzes ~16,737 Canadian airline loyalty members to:
1. Predict customer churn using a Random Forest model (ROC-AUC: 0.889)
2. Segment customers into 5 actionable groups based on behavior and value
3. Recommend specific retention actions for each segment

## How to Run the Dashboard Locally (Reproducibility)

### Prerequisites
- Python 3.10 or higher installed
- Git installed

### Steps

1. Clone the repository:git clone https://github.com/KanishkaGupta28/airline-loyalty-project.git
cd airline-loyalty-projec

2. Create and activate a virtual environment:
python -m venv venv
- Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

3. Install dependencies:
pip install -r src/requirements.txt

4. Run the dashboard:
cd src
streamlit run app.py

5. The app will open automatically in your browser at `http://localhost:8501`

The dashboard reads pre-processed data from `data/processed/customer_segments_final.csv` and the trained model from `src/model/`, both of which are already included in this repository — no additional setup or data download is required.

## How to Reproduce the Full Analysis (Optional)

If you want to regenerate the processed data and model from scratch instead of using the included files, run the notebooks in this order after completing steps 1-3 above:

1. `notebooks/01_data_exploration.ipynb` - initial data exploration
2. `notebooks/02_data_cleaning.ipynb` - cleaning, merging, churn label creation
3. `notebooks/03_churn_model.ipynb` - churn prediction model training
4. `notebooks/04_segmentation.ipynb` - customer segmentation
5. `notebooks/05_apply_model.ipynb` - applies the model to generate churn risk scores

Each notebook saves its outputs to `data/processed/` or `src/model/`, which the dashboard then reads.

## Project Structure
- `data/raw/` : original CSV datasets
- `data/processed/` : cleaned and feature-engineered datasets
- `notebooks/` : 01 data exploration, 02 cleaning, 03 churn model, 04 segmentation, 05 apply model
- `src/app.py` : Streamlit dashboard (working prototype)
- `src/model/` : saved trained model + column list
- `outputs/` : charts used in the technical report
- `report/` : Technical Report (.docx)

## Key Findings
- CLV does not differentiate customer segments despite churn rates ranging 4%-64%
- Recency (months since last flight) is the strongest churn predictor
- 5 segments identified: Loyal Frequent Flyers, New Members, Lapsed/Critical Risk, Engaged Redeemers, and Point Hoarders

