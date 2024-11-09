import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os
import tempfile
import datetime
import wikipedia
import webbrowser
import smtplib
import time
import base64
import webbrowser
# Function to convert text to speech
# def speak(text):
#     tts = gTTS(text=text, lang='en')
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
#         tts.save(fp.name)
#         st.audio(fp.name, format='audio/mp3')
#     os.unlink(fp.name)

def speak(text):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        with open(fp.name, "rb") as audio_file:
            audio_bytes = audio_file.read()
    
    audio_base64 = base64.b64encode(audio_bytes).decode()
    audio_tag = f'<audio autoplay="true" src="data:audio/mp3;base64,{audio_base64}">'
    st.markdown(audio_tag, unsafe_allow_html=True)
    
    os.unlink(fp.name)

with st.sidebar:
    with st.echo():
        st.write("This code will be printed to the sidebar.")
    with st.spinner("Loading..."):
        time.sleep(5)
    st.success("Done! ")

st.markdown(
    """
    <style>
    [data-testid="stMain"]{
        background: rgb(2,0,36);
background: linear-gradient(90deg, rgba(2,0,36,1) 0%, rgba(9,98,121,0.8352591036414566) 35%, rgba(0,212,255,1) 100%);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to recognize speech
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = r.listen(source, timeout=5, phrase_time_limit=5)
    try:
        st.write("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        st.write(f"User said: {query}")
        return query.lower()
    except sr.WaitTimeoutError:
        return "Timeout"
    except sr.UnknownValueError:
        return "Unknown"
    except Exception as e:
        st.write(f"An error occurred: {str(e)}")
        return "Error"

def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        return "Good Morning!"
    elif 12 <= hour < 18:
        return "Good Afternoon!"
    else:
        return "Good Evening!"

def search_google(query):
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('skbhagoji97@gmail.com', 'jsoq tvkh ijov iayo')
    server.sendmail('skbhagoji97@gmail.com', to, content)
    server.close()

st.title("AI Assistant - Veer 🤖")
st.image("bot.gif")
def main():
    greeting = wishMe()
    speak(f"{greeting} How can I assist you today?")
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        greeting = wishMe()
        speak(f"{greeting} How can I assist you today?")

    if 'listening' not in st.session_state:
        st.session_state.listening = False

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Start Listening"):
            st.session_state.listening = True
            st.rerun()
    
    with col2:
        if st.button("Stop Listening"):
            st.session_state.listening = False
            st.rerun()

    output = st.empty()

    if st.session_state.listening:
        output.write("Listening... Say something!")
        query = takeCommand()
        
        if query not in ["Timeout", "Unknown", "Error"]:
            output.write(f"Processing: {query}")
            
            if 'wikipedia' in query:
                speak('Searching Wikipedia...')
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                output.write(results)
                speak(results)

            elif 'open youtube' in query:
                webbrowser.open("https://youtube.com")
                speak("Opening YouTube")

            elif 'open google' in query:
                webbrowser.open("https://google.com")
                speak("Opening Google")

            elif 'the time' in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")    
                speak(f"The time is {strTime}")

            elif 'search' in query or 'google' in query:
                search_query = query.replace("search", "").replace("google", "").strip()
                speak(f"Searching Google for {search_query}")
                search_google(search_query)
                output.write(f"Searched Google for: {search_query}")

            elif 'sleep' in query or 'quit' in query:
                speak('Thank you! See you again.')
                st.session_state.listening = False

            else:
                speak("I'm not sure how to help with that. Can you please try again?")
        
        elif query == "Timeout":
            speak("Didn't hear anything. Please try again.")
        elif query == "Unknown":
            speak("Couldn't understand. Please try again.")
        else:
            speak("An error occurred. Please try again.")
        
        time.sleep(5)  # Give some time for the user to read the output
        st.rerun()  # Rerun the script to continue listening

if __name__ == "__main__":
    main()