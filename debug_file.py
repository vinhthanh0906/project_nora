from datetime import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha
import pyaudio
import os
import folium
import random

# Initialize the text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    if voice.id == 'com.apple.voice.compact.en-US.Samantha':
        engine.setProperty('voice', voice.id)
        break

engine.setProperty('rate', 140)
engine.setProperty('volume', 1)

def speak(text, rate=140):
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()

def parseCommand():
    recognizer = sr.Recognizer()
    print("Listening for command...")

    with sr.Microphone() as source:
        recognizer.pause_threshold = 2
        recognizer.adjust_for_ambient_noise(source)
        input_speech = recognizer.listen(source)
    
    try:
        print("Recognizing speech...")
        query = recognizer.recognize_google(input_speech, language='en-US')
        print(f'The input speech was: {query}')
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        speak("Sorry, I could not understand the audio.")
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
        speak("Could not request results from Google Speech Recognition service.")
    
    return ""

def search_wiki(query):
    summary = wikipedia.summary(query, sentences=2)
    return summary

def search_wolframalpha(query):
    app_id = 'YOUR_WOLFRAMALPHA_APP_ID'
    client = wolframalpha.Client(app_id)
    res = client.query(query)
    answer = next(res.results).text
    return answer

def get_all_songs(directory):
    song_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.mp3', '.m4a', '.aac')):
                song_files.append(os.path.join(root, file))
    return song_files

def play_random_song(directory):
    try:
        songs = get_all_songs(directory)
        if not songs:
            print("No songs found in the directory.")
            return
        song_path = random.choice(songs)
        os.system(f'afplay "{song_path}"')
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    activation_word = 'friday'  # Define the activation word
    
    while True:
        query = parseCommand()
        
        if query.startswith(activation_word):
            query = query[len(activation_word):].strip().split()
            if not query:
                continue

            # Say command
            if query[0] == 'say':
                if 'hello' in query:
                    speak("Good morning")
                else:
                    speech = ' '.join(query[1:])
                    speak(speech)
            
            # Folium and navigation map feature
            elif query[0] == 'open' and query[1] == 'map':
                map = folium.Map(location=[39.82, -100], zoom_start=4)
                folium.Marker(location=[39.82, -100]).add_to(map)
                filename = 'Map.html'
                map.save(filename)
                filepath = os.getcwd()
                file_uri = 'file:///' + filepath + '/' + filename
                webbrowser.get('edge').open_new_tab(file_uri)
            
            # Open websites using Google Chrome
            elif query[0] == 'go' and query[1] == 'to':
                speak('Browsing...')
                web_query = ' '.join(query[2:])
                webbrowser.get('chrome').open_new_tab(web_query)
            
            # Wikipedia search
            elif query[0] == 'wikipedia':
                search_query = ' '.join(query[1:])
                speak('Accessing universal databank')
                summary = search_wiki(search_query)
                speak(summary)
            
            # Wolfram Alpha computational knowledge search
            elif query[0] == 'compute' or query[0] == 'computer':
                search_query = ' '.join(query[1:])
                speak('Computing')
                try:
                    result = search_wolframalpha(search_query)
                    speak(result)
                except:
                    speak("Unable to compute")
            
            # Record a note
            elif query[0] == 'login':
                speak('Ready to record your note')
                new_note = parseCommand().lower()
                now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                with open(f'note_{now}.txt', 'w') as new_file:
                    new_file.write(new_note)
                speak('Note written')
            
            # Play music
            elif query[0] == 'play' and query[1] == 'music':
                speak('Playing music.')
                music_directory = "/Users/nguyenthanhvinh/Music/Music/Media.localized/Music"
                play_random_song(music_directory)
            
            # Exit system
            elif query[0] == 'turn' and query[1] == 'off':
                speak("Goodbye")
                break

if __name__ == '__main__':
    # Greet the user
    greet_text = "Hello, I am Friday. How can I assist you today, sir?"
    speak(greet_text)
    
    main()