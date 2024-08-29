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
import edge_tts
import cv2


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

# Set wolframa path
app_id = 'WRY2E9-9RWL2TRQ5P'
client = wolframalpha.Client(app_id)

def listOrDict(var):
    if isinstance(var, list):
        return var[0]['plaintext']
    else:
        return var['plaintext']


def search_wolframalpha(keyword = ''):
    response = client.query(keyword)
  
    # @success: Wolfram Alpha was able to resolve the query
    # @numpods: Number of results returned
    # pod: List of results. This can also contain subpods

    # Query not resolved
    if response['@success'] == 'false':
        speak('I could not compute')
    # Query resolved
    else: 
        result = ''
        # Question
        pod0 = response['pod'][0]
        # May contain answer (Has highest confidence value) 
        # if it's primary or has the title of result or definition, then it's the official result
        pod1 = response['pod'][1]
        if (('result') in pod1['@title'].lower()) or (pod1.get('@primary', 'false') == 'true') or ('definition' in pod1['@title'].lower()):
            # Get the result
            result = listOrDict(pod1['subpod'])
            # Remove bracketed section
            return result.split('(')[0]
        else:
            # Get the interpretation from pod0
            question = listOrDict(pod0['subpod'])
            # Remove bracketed section
            question = question.split('(')[0]
            # Could search wiki instead here? 
            return question
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
            if query[0] == 'open' and query[1] == 'map':
                chrome_path = '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge'
                webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
                map = folium.Map(location=[39.82, -100], zoom_start=4)
                folium.Marker(location=[39.82, -100]).add_to(map)
                filename = 'Map.html'
                map.save(filename)
                filepath = os.getcwd()
                file_uri = 'file:///' + filepath + '/' + filename
                webbrowser.get('chrome').open_new_tab(file_uri)
                speak('Here is your location')
            
            # Open websites using Google Chrome
            if query[0] == 'go' and query[1] == 'to':
                speak('Browsing...')
                chrome_path = '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge'
                webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
                web_query = ' '.join(query[2:])
                webbrowser.get('chrome').open_new_tab(web_query)
            
            # Wikipedia search
            if query[0] == 'wikipedia':
                search_query = ' '.join(query[1:])
                speak('Accessing universal databank')
                summary = search_wiki(search_query)
                speak(summary)
            
            # Wolfram Alpha computational knowledge search
            if query[0] == 'compute' or query[0] == 'computer':
                query = ' '.join(query[1:])
                try:
                    result = search_wolframalpha(query)
                    speak(result)
                except:
                    speak('Unable to compute')

            
            # Record a note
            if query[0] == 'login':
                speak('Ready to record your note')
                new_note = parseCommand().lower()
                now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                with open(f'note_{now}.txt', 'w') as new_file:
                    new_file.write(new_note)
                speak('Note written')
            
            # Play music
            if query[0] == 'play' and query[1] == 'music':
                speak('Playing music.')
                music_directory = "/Users/nguyenthanhvinh/Music/Music/Media.localized/Music"
                play_random_song(music_directory)
                
            #OpenCv    
            if query[0] == 'screen' and query[1] == 'on':
                video_capture = cv2.VideoCapture(0)

                if not video_capture.isOpened():
                    print("Error: Could not open video capture.")
                    return

                while True:
                    # Capture frame-by-frame
                    ret, frame = video_capture.read()

                    if not ret:
                        print("Error: Failed to capture image.")
                        break

                    # Display the resulting frame
                    cv2.imshow('Video', frame)

                    # Break the loop if 'q' is pressed
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                # Release the webcam and close the window
                video_capture.release()
                cv2.destroyAllWindows()
                            
                            
                
                
                # Extra Feature
                
                
                

            # Exit system
            elif query[0] == 'turn' and query[1] == 'off':
                speak("Goodbye")
                break

if __name__ == '__main__':
    # Greet the user
    greet_text = "Hello, I am Friday. How can I assist you today, sir?"
    speak(greet_text)
    
    main()