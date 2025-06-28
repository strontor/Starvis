import pyttsx3 
import speech_recognition as sr 
import datetime
import wikipedia 
import webbrowser
import os
import smtplib
import requests # This module in Python is a popular library used for making HTTP requests to communicate with web servers. It simplifies sending and receiving data over the internet, such as retrieving data from APIs, submitting forms, or downloading files.
import yfinance as yfp
from pytube import Search # pytube module is generally used to download yt videos whereas importing Search class will help in searching for youtube results.

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.setProperty('voice', voices[1].id)
    engine.say(audio)   
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("Sir, This is Starvis, how may I assist you?")       

def takeCommand():

    r = sr.Recognizer()  #Creates a new Recognizer instance, which represents a collection of speech recognition functionality.
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1.5 # means if there is a gap of 1.5sec in the input audio. The sentence will be called as completed and break the listening 
        audio = r.listen(source) # sirf sunta hai
        
    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-us')  # ye suna hua baat samajhta hai(process krta hai)
        print(f"User said: {query}\n")

    except Exception as e: 
        print("Say that again please...")  
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('name@gmail.com', 'password')
    server.sendmail('name@gmail.com', to, content)
    server.close()
    
def getStockPrice(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    stock_info = stock.info
    current_price = stock_info.get('currentPrice', 'N/A')
    return f"The current price of {stock_symbol} is {current_price}"

def showYouTubeResults(song_name):
    search = Search(song_name)
    results = search.results
    if results:
        video_url = results[0].watch_url
        webbrowser.open(video_url)
        speak(f"Showing results for {song_name} on YouTube")
    else:
        speak("Song not found on YouTube")
    
def getWeather(city):
    api_key = "2a1b67d9c312d584b7b0bb2ab988d956"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "q=" + city + "&appid=" + api_key   #very important line (location specific)
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"] != "404":
        main = data.get("main", {})
        weather = data.get("weather", [{}])[0]
        temperature = round(main.get("temp", "N/A") -273.15, 2)
        pressure = main.get("pressure", "N/A")
        humidity = main.get("humidity", "N/A")
        description = weather.get("description", "N/A")
        weather_report = f"Temperature: {temperature}°C\nPressure: {pressure}hPa\nHumidity: {humidity}%\nDescription: {description}"
        return weather_report
    else:
        return "City not found."
    

if __name__ == "__main__":
    wishMe()
    while True:
    
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak("what do you want to search?")
            query = takeCommand().lower()
            print(f"Search term: {query}")  # Debugging statement
            speak('Searching Wikipedia...')
            if query:
                try:
                    results = wikipedia.summary(query, sentences=2)
                    speak("According to Wikipedia")
                    print(results)
                    speak(results)
                except wikipedia.exceptions.DisambiguationError as e:
                    speak("There are multiple results for your query, please be more specific.")
                    print(e.options)
                except wikipedia.exceptions.PageError:
                    speak("The page does not exist.")
                except wikipedia.exceptions.WikipediaException as e:
                    speak("An error occurred while searching Wikipedia.")
                    print(e)
            else:
                speak("Please provide a search term.")
                      
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open facebook' in query:
            webbrowser.open("facebook.com")

        elif 'open instagram' in query:
            webbrowser.open("instagram.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")
            
        elif 'search google' in query or 'search on google' in query:
            if query == 'search google' or 'search on google':
                    speak("what do you want to search?")
                    search_term = takeCommand().lower()
                    webbrowser.open(f"https://www.google.com/search?q={search_term}")
                    speak(f"Searching Google for {search_term}")  
            elif 'for' in query:
                search_term = query.replace("search google for", "").strip()
                webbrowser.open(f"https://www.google.com/search?q={search_term}")
                speak(f"Searching Google for {search_term}")                    
                    
                     
        elif ('open'or'play') and 'youtube' and 'video' in query:
            speak("Which YouTube video?")
            song_name = takeCommand().lower()
            showYouTubeResults(song_name)


        elif 'what is the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")
            
        elif 'weather' in query:
            speak('Which city?')
            city = takeCommand().lower()
            weather_report = getWeather(city)
            speak(weather_report)
            print(weather_report)

        elif 'open code' in query:
            codePath = os.path.join(os.environ['LOCALAPPDATA'], "Programs", "Microsoft VS Code", "Code.exe")
            os.startfile(codePath)
            
        elif 'send email' in query:
            try:
                speak("To whom should I send the email?")
                to = takeCommand().lower()
                speak("What should I say?")
                content = takeCommand()
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry SIR. I am not able to send this email") 

        elif 'stock price' in query:
            speak("Which stock?")
            stock_symbol = takeCommand().upper()
            stock_price = getStockPrice(stock_symbol)
            speak(stock_price)
            print(stock_price)  
            
        elif any(keyword in query for keyword in ["end", "stop", "break", "terminate"]):
            print("User ended the program")
            speak("user terminated the program")
            break

        else:
            print("No query matched")
            # break
