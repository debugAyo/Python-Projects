import requests
import tkinter as tk
from PIL import Image, ImageTk, ImageOps
from io import BytesIO
from requests.exceptions import RequestException, Timeout, ConnectionError

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Dashboard")
        self.root.geometry("500x650")  # Increased height for better display
        
        # Configure styles
        self.bg_color = "#f0f8ff"
        self.entry_bg = "#ffffff"
        self.button_bg = "#4682b4"
        self.root.configure(bg=self.bg_color)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        tk.Label(self.root, text="Weather Dashboard", font=("Arial", 16, "bold"), 
                bg=self.bg_color, pady=10).pack()
        
        # Input frame
        input_frame = tk.Frame(self.root, bg=self.bg_color)
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Enter city name (e.g., 'London,UK'):", 
                font=("Arial", 10), bg=self.bg_color).grid(row=0, column=0, columnspan=3)
        
        self.city_entries = []
        for i in range(3):
            entry = tk.Entry(input_frame, font=('Arial', 12), width=20, 
                           bg=self.entry_bg, relief=tk.GROOVE, bd=2)
            entry.grid(row=1, column=i, padx=5, pady=5)
            self.city_entries.append(entry)
        
        # Search button
        tk.Button(self.root, text="Get Weather", command=self.search_weather,
                 font=("Arial", 12), bg=self.button_bg, fg="white",
                 relief=tk.RAISED, bd=2).pack(pady=10)
        
        # Results frames
        self.result_frames = []
        for _ in range(3):
            frame = tk.Frame(self.root, bg=self.bg_color, padx=10, pady=10,
                           relief=tk.GROOVE, bd=2)
            frame.pack(fill=tk.X, padx=20, pady=5)
            self.result_frames.append(frame)
    
    def get_weather_icon(self, icon_code, frame):
        try:
            icon_url = f'http://openweathermap.org/img/wn/{icon_code}@2x.png'
            response = requests.get(icon_url, timeout=5)
            response.raise_for_status()
            
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            
            # Resize and make background transparent
            img = img.resize((80, 80), Image.LANCZOS)
            img = img.convert("RGBA")
            
            # Create a transparent background
            datas = img.getdata()
            new_data = []
            for item in datas:
                # Change white/semi-white pixels to transparent
                if item[0] > 200 and item[1] > 200 and item[2] > 200:
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)
            img.putdata(new_data)
            
            return ImageTk.PhotoImage(img)
            
        except Exception as e:
            print(f"Error loading icon: {e}")
            return None
    
    def get_weather(self, city, frame):
        api_key = "b2c03cc4f37b1914d3b9cb8f89d26127"
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        
        # Clear previous results
        for widget in frame.winfo_children():
            widget.destroy()
        
        try:
            # Try different query formats if needed
            query_formats = [
                {'q': city, 'appid': api_key, 'units': 'metric'},
                {'q': f"{city},US", 'appid': api_key, 'units': 'metric'},
                {'q': f"{city},UK", 'appid': api_key, 'units': 'metric'}
            ]
            
            response = None
            for params in query_formats:
                try:
                    response = requests.get(base_url, params=params, timeout=(3, 10))
                    if response.status_code == 200:
                        break
                except:
                    continue
            
            if response and response.status_code == 200:
                data = response.json()
                temp = data['main']['temp']
                desc = data['weather'][0]['description'].capitalize()
                icon_code = data['weather'][0]['icon']
                wind = data['wind']['speed']
                humidity = data['main']['humidity']
                city_name = data.get('name', city)
                
                # Create a container frame for icon and text
                container = tk.Frame(frame, bg=self.bg_color)
                container.pack(fill=tk.X)
                
                # Get and display weather icon
                icon_img = self.get_weather_icon(icon_code, frame)
                if icon_img:
                    icon_label = tk.Label(container, image=icon_img, bg=self.bg_color)
                    icon_label.image = icon_img  # Keep reference
                    icon_label.pack(side=tk.LEFT, padx=10)
                
                # Weather information
                weather_info = (
                    f"📍 {city_name}\n"
                    f"🌡 {temp}°C | 💧 {humidity}%\n"
                    f"🌬 {wind} m/s | {desc}"
                )
                
                tk.Label(container, text=weather_info, font=('Arial', 11), 
                        bg=self.bg_color, justify=tk.LEFT, anchor='w').pack(side=tk.LEFT)
                
            else:
                error_msg = f"City '{city}' not found"
                suggestions = {
                    "new york": "Try 'New York,US'",
                    "london": "Try 'London,UK'",
                    "paris": "Try 'Paris,FR'"
                }
                
                if city.lower() in suggestions:
                    error_msg += f"\n{suggestions[city.lower()]}"
                
                tk.Label(frame, text=error_msg, font=('Arial', 10), 
                        bg=self.bg_color, fg="red").pack()
        
        except Timeout:
            tk.Label(frame, text="Request timed out. Try again later.", 
                    font=('Arial', 10), bg=self.bg_color, fg="red").pack()
        except ConnectionError:
            tk.Label(frame, text="No internet connection.", 
                    font=('Arial', 10), bg=self.bg_color, fg="red").pack()
        except Exception as e:
            tk.Label(frame, text=f"Error: {str(e)}", 
                    font=('Arial', 10), bg=self.bg_color, fg="red").pack()
    
    def search_weather(self):
        cities = [entry.get().strip() for entry in self.city_entries if entry.get().strip()]
        for i, city in enumerate(cities):
            if i < len(self.result_frames):
                self.get_weather(city, self.result_frames[i])

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()