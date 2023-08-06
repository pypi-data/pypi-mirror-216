import requests
from peduncle.peduncle import extract_text

def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Example usage
url = "https://blog.rust-lang.org/2023/05/29/RustConf.html"
print(extract_text(get_html(url)))