from jobspy import scrape_jobs
import pandas as pd
from datetime import datetime
import time

# This script will search for jobs on LinkedIn using the jobspy library.
# Roles will be read from roles.txt

def get_job_roles(file_path):
    with open(file_path, 'r') as f:
        roles = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
    return roles

def get_excluded_words(file_path):
    with open(file_path, 'r') as f:
        words = [line.strip().lower() for line in f if line.strip() and not line.strip().startswith('#')]
    return words

if __name__ == "__main__":
    roles_file = "roles.txt"
    excluded_words_file = "excluded_words.txt"
    
    job_roles = get_job_roles(roles_file)
    excluded_words = get_excluded_words(excluded_words_file)

    if not job_roles:
        print(f"No job roles found in {roles_file}. Please add roles to search for.")
    else:
        all_jobs = pd.DataFrame()
        for role in job_roles:
            print(f"Searching for '{role}' on LinkedIn...")
            jobs = scrape_jobs(
                site_name=['linkedin'],
                search_term=role,
                results_wanted=10, # You can adjust this number
                hours_ago=168, # You can adjust this to search for jobs posted in the last X hours
                location='Sweden'
            )
            time.sleep(5) # Add a 5-second delay to avoid being too aggressive
            if jobs is not None and not jobs.empty:
                print(f"Columns available in scraped data for '{role}': {jobs.columns.tolist()}")
                all_jobs = pd.concat([all_jobs, jobs], ignore_index=True)
            else:
                print(f"No jobs found for '{role}'.")
        
        if not all_jobs.empty:
            if excluded_words:
                initial_count = len(all_jobs)
                for word in excluded_words:
                    all_jobs = all_jobs[~all_jobs['title'].str.contains(word, case=False, na=False)]
                if len(all_jobs) < initial_count:
                    print(f"Filtered out {initial_count - len(all_jobs)} jobs based on excluded words.")

            print("Search complete. Displaying filtered results:")
            selected_columns = ['job_url', 'title', 'company', 'location', 'date_posted']
            print(all_jobs[selected_columns])

            current_date = datetime.now().strftime("%Y-%m-%d")
            csv_filename = f"linkedin_jobs_{current_date}.csv"
            all_jobs[selected_columns].to_csv(csv_filename, index=False)
            print(f"Results saved to {csv_filename}")

            # Check for and remove duplicates in the CSV file
            try:
                df = pd.read_csv(csv_filename)
                initial_rows = len(df)
                df.drop_duplicates(inplace=True)
                if len(df) < initial_rows:
                    print(f"Removed {initial_rows - len(df)} duplicate rows from {csv_filename}")
                    df.to_csv(csv_filename, index=False)
            except FileNotFoundError:
                print(f"Error: {csv_filename} not found for duplicate removal.")
        else:
            print("No jobs found for any of the specified roles.")
