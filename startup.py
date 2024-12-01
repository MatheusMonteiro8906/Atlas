import assist
import requests
import time
import os
from datetime import datetime

api_key = os.getenv('WEATHER_API_KEY')
url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={os.getenv('WEATHER_CITY')}"

def get_weather():
                print("GETTING WEATHER")
                response = requests.get(url)
                if response.status_code == 200:
                    return response.json()
                else:
                    return {"error": f"Failed to retrieve data: {response.status_code}"}
    
def main():
                current_time = time.time()
                weather_data = get_weather()
                local_time = weather_data['location']['localtime']
                local_time = datetime.strptime(local_time, '%Y-%m-%d %H:%M')
                hour = local_time.hour

                if hour < 12:
                    ask = "Good morning, Jarvis. What's up for today?"
                elif 12 <= hour < 18:
                    ask = "Good afternoon, Jarvis. What's up for today?"
                else:
                    ask = "Good night, Jarvis. What's up for today?"

                response = assist.ask_question_memory(ask + 'also, Give a brief description of how the time is, based on this: (only talk about temperature in C° ant not F°, its maximum and minimum for today[you MUST say at least the temperature, humidity, how the clouds are, wind speeds and the chances of rain])' + str(weather_data))
                done = assist.TTS(response)

                exit

if __name__ == '__main__':
    main()