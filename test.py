import cv2
import speech_recognition as sr

def detect_faces_in_frame(frame, face_cascade):
    """Detect faces in the frame using OpenCV's Haar Cascade."""
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    return frame, len(faces)

def initialize_recognizer():
    """Initialize the speech recognizer."""
    return sr.Recognizer()

def listen_for_commands(recognizer):
    """Listen for voice commands and return the recognized command."""
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print("You said: " + command)
            return command
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError as e:
            print("Sorry, there was an error with the speech recognition service.")
            return None

def run_face_detection(face_cascade, recognizer):
    """Run face detection and listen for voice commands."""
    video_capture = cv2.VideoCapture(0)
    
    while True:
        ret, frame = video_capture.read()
        frame, face_count = detect_faces_in_frame(frame, face_cascade)
        cv2.imshow('Video', frame)

        command = listen_for_commands(recognizer)
        if command:
            if "start" in command:
                print("Starting face detection...")
                while True:
                    ret, frame = video_capture.read()
                    frame, face_count = detect_faces_in_frame(frame, face_cascade)
                    cv2.imshow('Video', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            elif "stop" in command:
                print("Stopping face detection...")
                break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Load the pre-trained Haar Cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Initialize the speech recognizer
    recognizer = initialize_recognizer()
    
    # Run the face detection and command listening loop
    run_face_detection(face_cascade, recognizer)