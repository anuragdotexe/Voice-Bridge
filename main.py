import speech_recognition as sr
import pyttsx3
import time
from transformers import pipeline

tts_engine = pyttsx3.init()
llm_pipeline = pipeline("text-generation", model="gpt2")

def transcribe_audio_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        audio_data = r.listen(source, phrase_time_limit=5)
    try:
        text = r.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print(f"Could not request results from speech service; {e}")
        return None

def query_llm(prompt):
    responses = llm_pipeline(prompt, max_length=50, do_sample=True, temperature=0.7)
    generated_text = responses[0]["generated_text"]
    return generated_text.strip()

def speak_text(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

def main():
    while True:
        choice = input("Press Enter to start speaking, or 'q' to quit: ").strip()
        if choice.lower() == 'q':
            break
        start_time = time.time()
        user_text = transcribe_audio_to_text()
        if user_text:
            print("User said:", user_text)
            response_text = query_llm(user_text)
            print("Bot response:", response_text)
            speak_text(response_text)
        else:
            print("No valid speech captured or recognition failed.")
        elapsed = time.time() - start_time
        print(f"Interaction took {elapsed:.2f} seconds.")

if __name__ == "__main__":
    main()
