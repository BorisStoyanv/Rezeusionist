import requests

def fetch_text_from_api(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.text.strip()  # Remove any leading/trailing whitespace
    except requests.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None

def save_to_file(text, filename):
    try:
        with open(filename, 'w') as file:
            file.write(text)
        print(f"Text saved to {filename} successfully.")
    except IOError as e:
        print(f"Error saving data to file: {e}")

if __name__ == "__main__":
    api_url = "http://127.0.0.1:8000/api/get-text"
    filename = "information.txt"

    text_content = fetch_text_from_api(api_url)
    
    if text_content:
        save_to_file(text_content, filename)
