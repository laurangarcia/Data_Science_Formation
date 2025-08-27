# 1. Instalar libreria  pip install requests
# 2. pip freeze | Select-String -Pattern "requests"
# 3. Creas requirements y pegas lo que te de en el paso 2, luego sigues con este código

import requests

def get_location(ip):
    url = f'https://freeipapi.com/api/json/{ip}'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return {
        "country": data["countryName"],
        "region": data["regionName"],
        "city": data["cityName"],
    }

if __name__ == "__main__":
    ip = "8.8.8.8" #ip de google
    location = get_location(ip)
    print(location)

   