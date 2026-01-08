from jobspy import scrape_jobs
import pandas as pd

# This script will search for jobs on LinkedIn using the jobspy library.
# Roles will be read from roles.txt

def get_job_roles(file_path):
    with open(file_path, 'r') as f:
        roles = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
    return roles

if __name__ == "__main__":
    roles_file = "roles.txt"
    job_roles = get_job_roles(roles_file)

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
                hours_ago=24, # You can adjust this to search for jobs posted in the last X hours
                country_indeed='USA'
            )
            if jobs is not None and not jobs.empty:
                print(f"Columns available in scraped data for '{role}': {jobs.columns.tolist()}")
                all_jobs = pd.concat([all_jobs, jobs], ignore_index=True)
            else:
                print(f"No jobs found for '{role}'.")
        
        if not all_jobs.empty:
            print("Search complete. Displaying results:")
            selected_columns = ['job_url', 'title', 'company', 'location', 'date_posted']
            print(all_jobs[selected_columns])
            # You can also save the results to a CSV file
            all_jobs[selected_columns].to_csv("linkedin_jobs.csv", index=False)
        else:
            print("No jobs found for any of the specified roles.")
