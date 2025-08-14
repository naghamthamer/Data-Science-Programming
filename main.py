import pandas as pd
import multiprocessing

data = pd.read_csv(r"C:\Users\Nagham\Downloads\Datascience Programming\proj\new.csv")
data.to_json(r"C:\Users\Nagham\Downloads\Datascience Programming\proj\original_data.json")


def read_sleep_json(filename):
    return pd.read_json(filename)


if __name__ == "__main__":
    file1 = r"C:\Users\Nagham\Downloads\Datascience Programming\proj\original_data.json"
    file2 = r"C:\Users\Nagham\Downloads\Datascience Programming\proj\resampled_sleep_data.json"

    pool = multiprocessing.Pool(processes=2)

    df1_result = pool.apply_async(read_sleep_json, args=(file1,))
    df2_result = pool.apply_async(read_sleep_json, args=(file2,))

    pool.close()
    pool.join()

    combined_df = pd.concat([df1_result.get(), df2_result.get()], axis=0, ignore_index=True)
    print("✅ Combined data shape:", combined_df.shape)
    print(combined_df.head())

print("."*100)

# Web Scraping using PyQuery and requests
import requests
from pyquery import PyQuery as pq
import json

# This function scrapes sleep tips from the given website
def scrape_sleep_tips_pyquery():
    url = "https://www.sleepfoundation.org/sleep-hygiene"
    print(f"📡 Fetching content from: {url}")

    # Add headers to make the request look like it comes from a browser
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
    }

    try:
        # Make the request with headers
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            doc = pq(response.text)
            tips = []

            # Extract all list items from unordered and ordered lists
            for li in doc("ul li, ol li").items():
                tip = li.text()
                if tip:
                    tips.append(tip)

            # Save first 10 tips to a JSON file
            with open("sleep_tips_pyquery.json", "w", encoding="utf-8") as f:
                json.dump(tips[:10], f, indent=2, ensure_ascii=False)

            print("✅ Sleep tips saved to sleep_tips_pyquery.json")
            for i, tip in enumerate(tips[:5], 1):
                print(f"{i}. {tip}")
        else:
            print("❌ Failed to fetch page, status code:", response.status_code)
    except Exception as e:
        print("❌ Error scraping tips:", e)

# This ensures the function only runs when the script is executed directly
if __name__ == "__main__":
    scrape_sleep_tips_pyquery()
