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

## How to Run Locally
1. Create virtual environment: `python -m venv venv`
2. Activate it: `venv\Scripts\activate`
3. Install dependencies: `pip install -r src/requirements.txt`
4. Run notebooks in order (notebooks/01 through 05) to reproduce the analysis
5. Run dashboard: `cd src`, then `streamlit run app.py`

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

