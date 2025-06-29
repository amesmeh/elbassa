#!/usr/bin/env python3
import urllib.request
import urllib.error

try:
    print("Testing homepage...")
    response = urllib.request.urlopen('http://localhost:8000/')
    print(f"Status: {response.getcode()}")
    content = response.read().decode('utf-8')
    print(f"Content length: {len(content)} chars")
    if len(content) < 1000:
        print("Content preview:")
        print(content)
    else:
        print("Content preview (first 500 chars):")
        print(content[:500])
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code}")
    print("Error response:")
    print(e.read().decode('utf-8')[:1000])
except Exception as e:
    print(f"Error: {e}") 