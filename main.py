import cv2
import speech_recognition as sr
import openai
from gtts import gTTS
import os
import time

# Initialize the recognizer and OpenAI API key
recognizer = sr.Recognizer()
openai.api_key = 'your-openai-api-key'

# Function to capture video and audio input
def capture_audio():
    # Open the webcam (0 is typically the default webcam)
    cap = cv2.VideoCapture(0)

    # Start the timer
    start_time = time.time()

    # Capture a single frame (for display purposes only)
    ret, frame = cap.read()
    
    # Release the webcam (only need one frame)
    cap.release()
    
    # Convert frame to gray scale for quicker processing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Display the captured frame for feedback
    cv2.imshow('Captured Frame', gray)
    
    # Wait for a brief moment to show the image
    cv2.waitKey(1)
    
    # Measure the elapsed time
    elapsed_time = time.time() - start_time
    
    # Check if the elapsed time is less than 3 seconds
    if elapsed_time < 3:
        time.sleep(3 - elapsed_time)  # Ensure the entire process takes at least 3 seconds

    # Close the image display window
    cv2.destroyAllWindows()
    
    # Capture audio from the microphone
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        
        try:
            # Recognize speech using Google's Speech Recognition
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            print("Could not understand the audio")
            return None
        except sr.RequestError:
            print("Could not request results from the speech recognition service")
            return None

def process(text):
    # Send the text to the OpenAI API and get a response
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message['content']

def speak(text):
    # Convert the text to speech using gTTS
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    
    # Play the converted audio file
    os.system("mpg321 response.mp3")

def main():
    while True:
        print("\nSay something or 'quit' to exit...")
        text = capture_audio()
        if text is not None:
            if "quit" in text.lower():
                break
            
            response = process(text)
            print("Bot:", response)
            speak(response)

if __name__ == "__main__":
    main()
