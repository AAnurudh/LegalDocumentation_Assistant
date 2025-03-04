import requests
import pytest

url = 'http://localhost:5000/api/upload'

def test_upload_document():
    print("Starting document upload test...")  # Log the start of the test

    files = {'document': open('uploads/test_file.txt', 'rb')}  # Use the test text file
    response = requests.post(url, files=files)
    print(f"Response Status Code: {response.status_code}")  # Log the response status code
    assert response.status_code == 200  # Check if the upload was successful
    print(f"Response Message: {response.json().get('message')}")  # Log the response message

    assert response.json().get('message') == 'File uploaded successfully!'  # Check the response message
