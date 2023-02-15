import requests
import json


class GardenCommunication():
    def __init__(self):
        pass

    def tempSensor(self, number):
        response = requests.get(f"https://dt.miet.ru/ppo_it/api/temp_hum/{number}", headers={"X-Auth-Token": atoken})
        return response.json()['id'], response.json()['humidity'],  response.json()['temperature']

    def humSensor(self, number):
        response = requests.get(f"https://dt.miet.ru/ppo_it/api/hum/{number}", headers={"X-Auth-Token": atoken})
        return response.json()['id'], response.json()['humidity']

    def windowOpen(self, state_value):
        response = requests.patch("https://dt.miet.ru/ppo_it/api/fork_drive", params ={"state": state_value})
        return response.status_code

    def waterGarden(self, device_id, state_value):
        response = requests.request('patch', "https://dt.miet.ru/ppo_it/api/watering", params ={"id": device_id, "state": state_value}, headers={"X-Auth-Token": atoken})
        return response.status_code

    def globalWaterGarden(self, state_value):
        response = requests.patch("https://dt.miet.ru/ppo_it/api/total_hum", params={"state": state_value})
        return response.status_code

class MainApp():
    def __init__(self):
        atoken = "efegr"

    def run(self):
        print(GardenCommunication().windowOpen(1))
        pass

if __name__ == "__main__":
    MainApp().run()
