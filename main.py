import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup

def main():
    # URL that lists the PDF files (update this to the actual page URL)
    index_url = "https://oagf.gov.ng/publications/faac-report/"

    # Get a list of PDF URLs from the index page
    pdf_urls = get_pdf_urls(index_url)
    print(f"Found {len(pdf_urls)} PDF files.")

    all_data = []
    processed_files = set()  # Set to keep track of files already downloaded/processed

    for url in pdf_urls:
        # Use the file name from the URL instead of a UUID
        filename = os.path.basename(url)

        # Check if this file has already been processed
        if filename in processed_files:
            print(f"{filename} has already been processed. Skipping download.")
            continue
        processed_files.add(filename)

        # Extract month and year from the file name.
        # This example assumes a naming format like "Disbursement-October-2024.pdf"
        match = re.search(r'Disbursement-([A-Za-z]+)-(\d{4})\.pdf$', filename)
        if match:
            month = match.group(1)
            year = match.group(2)
        else:
            month, year = None, None

        try:
            # Only download if the file doesn't exist on disk
            if not os.path.exists(filename):
                download_pdf(url, filename)
            else:
                print(f"{filename} already exists on disk. Skipping download.")
            data = extract_data_from_pdf(filename, month=month, year=year)
            all_data.extend(data)
        except Exception as e:
            print(f"Error processing {url}: {e}")
        finally:
            # Optionally remove the downloaded PDF file after processing
            if os.path.exists(filename):
                os.remove(filename)

    # Save the combined extracted data to a JSON file
    output_file = "combined_data.json"
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(all_data, json_file, indent=4)
    print(f"Data extraction complete. Saved to {output_file}")

if __name__ == "__main__":
    main()