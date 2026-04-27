# SoilSense

> **An end-to-end soil moisture predictor and analytical pipeline.**

## 🚀 Developed by Team **QUADRA COSMOS**

### Team Members
* **Orkhan Nuriyev** – Database Design & Pipeline
* **Ibrahim Suleymanov** – Machine Learning Modeling, Statistical Analysis
* **Khalid Ahmedov** – Data Cleaning & Web Application Development
* **Revan Khanbabayev** – Exploratory Data Analysis (EDA)

---

## 📌 Problem Statement
Can we accurately predict soil moisture levels for the next 7 days across diverse climatic zones in Azerbaijan? By systematically analyzing a decade of historical weather patterns, **SoilSense serves as a robust soil moisture predictor** aimed at providing high-precision irrigation guidance specifically tailored for regional agriculture, such as cotton cultivation in Saatli and tea farming in Lankaran.

## 💡 Why It Matters
Reliable soil moisture forecasting is the backbone of efficient agricultural water management. This pipeline addresses genuine climate data challenges—such as seasonal non-stationarity and sensor gaps—to help farmers and agricultural planners optimize irrigation scheduling, conserve water resources, and maximize crop yields in varying climates. 

## 🎯 Target Definition
* **Objective:** Predict future soil moisture levels based on historical weather patterns.
* **Metric of Success:** Achieve a Mean Absolute Error (MAE) of **< 0.05 $m^3/m^3$** on the prediction set.
* **Prediction Horizon:** Next 7 rolling days.

## 📊 Dataset & Horizon
* **Date Range:** 10+ years of historical data (2015–2026) alongside real-time 7-day forecasts.
* **Granularity:** Daily aggregated records.
* **Target Regions:**
  * **Baku:** Semi-arid climate (Urban/Control)
  * **Saatli:** Arid climate (Cotton focus)
  * **Lankaran:** Humid climate (Tea focus)
  * **Zardab:** Semi-arid / Central Aran climate (General agricultural focus)
  * **Guba:** Temperate / Mountainous climate (Orchard and fruit focus)

## 📖 Key Definitions
* **DuckDB:** An embedded, high-performance analytical database used locally to rapidly query and transform our large weather datasets.
* **Medallion Architecture:** Our DuckDB schema is designed with structured layers—**Raw** (direct ingest), **Staging** (cleaned and validated), and **Analytics** (feature-engineered) to ensure strict data quality.
* **Open-Meteo API:** A free, open-source weather API providing access to both our historical archive endpoint and the forecasting endpoint without requiring API keys.

---

## 📅 Project Roadmap & Daily Activities

Below is the execution timeline of our two-week sprint, detailing completed and planned milestones. 

| Status | Day | Focus Area | Key Activities |
| :---: | :---: | :--- | :--- |
| ✅ **Done** | **Day 1** | Project Kick-Off | Repo setup, Open-Meteo API exploration, city/variable selection. |
| ✅ **Done** | **Day 2** | Data Ingestion | Developed ingestion module, fetched 10 years of historical data and 7-day forecasts. |
| ✅ **Done** | **Day 3** | Database Design | Configured local DuckDB instance; built Raw, Staging, and Analytics schemas. |
| ✅ **Done** | **Day 4** | Data Cleaning | Implemented automated cleaning rules, handled missing values, engineered features (e.g., rolling averages). |
| ✅ **Done** | **Day 5** | Pipeline Automation | Orchestrated end-to-end Python pipeline with logging and automated quality gates. |
| ✅ **Done** | **Day 6** | Exploratory Data Analysis | Conducted statistical descriptions, temporal visualizations, and cross-city comparisons. |
| 🔄 **Plan** | **Day 7** | Statistical Analysis | Execute formal hypothesis testing, feature correlation analysis, and finalize modeling features. |
| 🔄 **Plan** | **Day 8** | Predictive Modeling | Train Random Forest & baseline regression models, evaluate MAE, compute confidence intervals. |
| 🔄 **Plan** | **Day 9** | Final Presentation | Prepare live pipeline demo, project submission, and presentation deck. |
