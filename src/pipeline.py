import argparse
import logging
import os
import time
import pandas as pd
from datetime import timedelta

# Import your custom modules
import database
import ingestion
import cleaning
import features
import quality_checks
from config import CITIES, MY_VARIABLES, START_DATE, END_DATE

# Setup Logging
os.makedirs("../logs", exist_ok=True)
logging.basicConfig(
    filename='../logs/pipeline.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

def run_pipeline(mode="full"):
    start_time = time.time()
    logging.info(f"🚀 Starting Weather Pipeline in '{mode.upper()}' mode.")
    
    conn = database.get_connection()
    database.create_schemas(conn)
    database.create_raw_tables(conn)
    
    output_path = "../data/raw/"
    os.makedirs(output_path, exist_ok=True)
    
    try:
        # --- STAGE 1: INGESTION ---
        logging.info("STAGE 1: Data Ingestion")
        max_dates = database.get_max_dates(conn) if mode == "incremental" else {}
        new_data_fetched = False
        
        for city in CITIES:
            city_name = city['name']
            
            # Determine date range for this city
            city_start = START_DATE
            if mode == "incremental" and city_name in max_dates and pd.notna(max_dates[city_name]):
                # Fetch data starting the day after the last recorded date
                last_date = pd.to_datetime(max_dates[city_name]).tz_localize(None)
                city_start = (last_date + timedelta(days=1)).strftime('%Y-%m-%d')
                
            if pd.to_datetime(city_start) > pd.to_datetime(END_DATE):
                logging.info(f"⏩ {city_name}: Data is already up to date (Latest: {last_date.date()}). Skipping fetch.")
                continue
                
            logging.info(f"📥 Fetching {city_name} from {city_start} to {END_DATE}...")
            df_hist = ingestion.fetch_historical(city_name, city['lat'], city['lon'], city_start, END_DATE, MY_VARIABLES)
            df_fore = ingestion.fetch_forecast(city_name, city['lat'], city['lon'], MY_VARIABLES)
            
            combined = pd.concat([df_hist, df_fore], ignore_index=True)
            
            # Save strictly as an incremental parquet to avoid overwriting base data 
            file_suffix = "_full" if mode == "full" else f"_inc_{city_start}"
            file_name = f"{city_name.lower()}{file_suffix}.parquet"
            combined.to_parquet(os.path.join(output_path, file_name), index=False)
            new_data_fetched = True
            
        # --- STAGE 2: DATABASE LOAD ---
        logging.info("STAGE 2: Loading to DuckDB Raw Layer")
        if mode == "full":
            database.load_raw_data(conn, output_path)
        elif new_data_fetched:
            # We only append files that have the incremental suffix we just created
            database.append_raw_data(conn, output_path)
            # Cleanup incremental parquets after loading so they don't load twice next time
            for f in os.listdir(output_path):
                if "_inc_" in f:
                    os.remove(os.path.join(output_path, f))
            
        df_raw = conn.execute("SELECT * FROM raw.weather_daily").df()
        logging.info(f"✅ Raw table contains {len(df_raw)} total rows.")
        
        # --- STAGE 3 & 4: CLEANING & FEATURES ---
        logging.info("STAGE 3: Cleaning (Raw -> Staging)")
        df_staging = cleaning.clean_raw_to_staging(conn)
        
        logging.info("STAGE 4: Feature Engineering (Staging -> Analytics)")
        df_features = features.create_features(conn)
        
        # --- STAGE 5: QUALITY GATES ---
        logging.info("STAGE 5: Running Quality Checks")
        qc_report = quality_checks.run_all_checks(df_raw, df_staging, df_features)
        
        print("\n" + "="*50)
        print("📊 DATA QUALITY REPORT")
        print("="*50)
        print(qc_report.to_string(index=False))
        print("="*50 + "\n")
        
        # Log failures or warnings
        issues = qc_report[qc_report['status'] != 'PASS']
        if not issues.empty:
            logging.warning(f"Quality checks flagged {len(issues)} issues.")
            
        duration = round(time.time() - start_time, 2)
        logging.info(f"🎉 Pipeline completed successfully in {duration} seconds.")

    except Exception as e:
        logging.error(f"❌ Pipeline failed: {str(e)}", exc_info=True)
        raise e
    finally:
        conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Weather Data Pipeline")
    parser.add_argument("--mode", type=str, choices=["full", "incremental"], default="full",
                        help="Run mode: 'full' (re-ingests everything) or 'incremental' (appends new data)")
    args = parser.parse_args()
    
    run_pipeline(mode=args.mode)