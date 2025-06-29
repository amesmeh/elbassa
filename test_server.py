#!/usr/bin/env python3
import urllib.request
import urllib.error

def test_url(url):
    try:
        response = urllib.request.urlopen(url)
        return response.getcode()
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:
        return f"Error: {e}"

# Test URLs
urls = [
    'http://localhost:8000/',
    'http://localhost:8000/martyrs/',
    'http://localhost:8000/injured/',
    'http://localhost:8000/orphans/',
    'http://localhost:8000/damages/',
    'http://localhost:8000/civil-registry/',
    'http://localhost:8000/medical/',
]

print("Testing server URLs:")
print("-" * 50)
for url in urls:
    status = test_url(url)
    print(f"{url}: {status}") 