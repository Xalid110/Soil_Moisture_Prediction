# 🧾 Data Quality Report

- A total of 85 records were analyzed.  
- Forward fill (ffill) was applied to handle NaN values since weather variables change slowly over time.  
- NaN values in the “soil moisture” column were left untouched, as this column is the target variable.  
- Outliers were not removed because they can be used as flags or informative features during the modeling stage.  

| Feature | Purpose |
|----------|----------|
| day_of_year | To capture seasonality patterns |
| precip_sum_7d | To represent the effect of cumulative 7-day precipitation |
| prev_soil_moisture | To model the inertial behavior of soil moisture |

No significant duplicates or date gaps were detected.  
Repetitions in `precipitation_hours` and `precipitation_sum` are considered normal weather data behavior rather than data errors.
