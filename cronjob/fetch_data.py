import requests
import pandas as pd


def fetch_and_convert(url, output_file):
    response = requests.get(url)
    data = response.json()
    df = pd.json_normalize(data)
    df.to_csv(output_file, index=False)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python fetch_data.py <url> <output_file>")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2]
    fetch_and_convert(url, output_file)
