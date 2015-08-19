import requests, time



while True:
    requests.post('http://localhost:5000/connected', data={'deviceId': 'buttonBoard'})
    requests.post('http://localhost:5000/buttonpress', data={'buttonId': 'light'})

    time.sleep(1)





