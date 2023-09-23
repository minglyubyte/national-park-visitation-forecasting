import subprocess

# Run the other script
if __name__ == "__main__":
    while True:
        try:
            subprocess.run(["python3", "visit_data_web_scrape.py"])
        except:
            continue