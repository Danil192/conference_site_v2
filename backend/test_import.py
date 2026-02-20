import requests

url = "http://localhost:8000/api/import/participants/"
files = {'file': open('C:/Users/danil/OneDrive/Рабочий стол/Study/ДИПЛОМ/reqs.xlsx', 'rb')}
try:
    response = requests.post(url, files=files)
    print(f"Status: {response.status_code}")
    print(response.json())
except Exception as e:
    print(f"Error: {e}")