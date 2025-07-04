import requests
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO
from requests.exceptions import Timeout, RequestException

def get_weather(city, frame):
    api_key = "6bc7e35e805a64a5d41e4c8c1ea8554e"
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {'q': city,'appid': api_key, 'units': 'metric'}

    for widget in frame.winfo_children():
        widget.destroy()

    try: 
        response = requests.get(base_url, params=params, timeout=(3.05, 10))
        response.raise_for_status()
        data = response.json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description'].capitalize()
        icon_code = data['weather'][0]['icon']
        wind = data['wind']['speed']

            #icon URL
        try:
            icon_url =f'http://openweathermap.org/img/wn/{icon_code}@2x.png'
            icon_data = requests.get(icon_url).content
            img = Image.open(BytesIO(icon_data))
            img = img.resize((50, 50), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            #Keep the Image Reference
            frame.icon_image = photo
        except Exception as icon_error:
            print(f"Icon download faild: {icon_error}")

            result = (
                f"Weather in {city.capitalize(): } \n"
                f"Temperature: {temp}°C\n"
                f"Description: {desc} \n"
                f"Wind Speed: {wind}.m/s" 
            )
        else:
            result = f'{city.capitalize()}: City not found'

    except TimeoutError:
        result = f"Error: {response.status_code}"
    except RequestException as e:
        result = f"Error: {str(e)}"
    except Exception as e:
        result = f'Error {str(e)}'
    tk.Label(frame,text=result, font=('Arial', 10), justify='left').pack()

def search_weather():
    cities = [entry.get().strip() for entry in city_entries if entry.get().strip()]
    for i, city in enumerate(cities):
        if i <len(result_frames):
            get_weather(city, result_frames[i])
        

#GUI setup
root = tk.Tk()
root.title("Beta Weather Dashboard")
root.geometry("500x600")

tk.Label(root, text="Enter up to 3 cities:", font=("Arial", 14)).pack(pady=10)

input_frame= tk.Frame(root)
input_frame.pack()

city_entries =[]
for i in range(3):
    entry = tk.Entry(input_frame, font=('Arial', 12), width=15)
    entry.grid(row=0, column=i, padx=5)
    city_entries.append(entry)

tk.Button(root, text="Get Weather", command=search_weather, font=("Arial", 12), bg="skyblue").pack(pady=10)

result_frames = []
for _ in range(3):
    frame = tk.Frame(root,pady=10)
    frame.pack()
    result_frames.append(frame)

root.mainloop()







