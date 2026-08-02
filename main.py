import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import sys
# pip install pocketsphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init()


def speak(text):
    engine.say(text)
    engine.runAndWait()


def play_music(song_name):
    song_name = song_name.lower().strip()

    if song_name in musicLibrary.songs:
        link = musicLibrary.songs[song_name]
        speak(f"Playing {song_name}")
        print(f"Playing: {link}")
        webbrowser.open(link)
    else:
        speak("Sorry, I don't have that song")
        print(f"Song not found: {song_name}")


def processCommand(c):
    c = c.lower()
    if "open google" in c:
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c:
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")
    elif "play" in c:
        song = c.replace("play", "").strip()
        if song:
            play_music(song)
        else:
            speak("Please tell me the song name")
    elif "stop" in c or "exit" in c or "quit" in c or "shut down" in c or "bye" in c:
        speak("Goodbye, shutting down")
        print("Shutting down...")
        sys.exit()
    else:
        speak("Sorry, I did not understand that command")
        print("No matching command found.")


if __name__ == "__main__":
    speak("Initializing Jarvis....")
    print("Initializing Jarvis....")

    with sr.Microphone() as source:
        print("Calibrating microphone for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
    print("Calibration done. Ready to listen.")

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)

            word = recognizer.recognize_google(audio)
            print(f"Heard: '{word}'")

            if "jarvis" in word.lower():
                speak("Ya")
                print("Jarvis Active... speak now")

                try:
                    with sr.Microphone() as source:
                        print("Listening for command...")
                        audio = recognizer.listen(source, timeout=6, phrase_time_limit=6)

                    command = recognizer.recognize_google(audio)
                    print(f"Command: {command}")
                    processCommand(command)

                except sr.WaitTimeoutError:
                    print("No command heard in time.")
                    speak("I didn't hear a command")
                except sr.UnknownValueError:
                    print("Could not understand the command.")
                    speak("Sorry, I couldn't understand that")

        except sr.WaitTimeoutError:
            continue

        except sr.UnknownValueError:
            continue

        except Exception as e:
            print("Error: {0}".format(e))