import os
import requests
import openai
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Twilio credentials
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_client = Client(account_sid, auth_token)

# OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to make a test call
def make_test_call(to_number, from_number, twiml_url):
    call = twilio_client.calls.create(
        to=to_number,
        from_=from_number,
        url=twiml_url,
        record=True
    )
    print("Call SID:", call.sid)
    return call.sid

# Function to get the recording URL
def get_call_recording(call_sid):
    recordings = twilio_client.recordings.list(call_sid=call_sid)
    if recordings:
        rec = recordings[0]
        recording_url = f"https://api.twilio.com{rec.uri.replace('.json', '.wav')}"
        return recording_url
    return None

# Function to transcribe the audio file using OpenAI Whisper API
def transcribe_with_whisper(recording_url):
    response = requests.get(recording_url, auth=(account_sid, auth_token))
    with open("call_recording.wav", "wb") as f:
        f.write(response.content)

    with open("call_recording.wav", "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript["text"]

# Function to summarize the transcript using GPT
def summarize_call(transcript):
    prompt = f"""
    You are a patient care AI. Summarize the call.
    Provide the patient's name if mentioned, the reason for the call, and any next steps. 
    Return JSON with keys: patient_name, reason, next_steps.

    Transcript: {transcript}
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}],
        temperature=0.2
    )
    return response["choices"][0]["message"]["content"]

if __name__ == "__main__":
    # Set your own test phone numbers and TwiML URL
    TO_NUMBER = "YOUR_TEST_PHONE_NUMBER"
    FROM_NUMBER = "YOUR_TWILIO_PHONE_NUMBER"
    TWIML_URL = "YOUR_TWIML_URL"

    call_sid = make_test_call(TO_NUMBER, FROM_NUMBER, TWIML_URL)
    recording_url = get_call_recording(call_sid)

    if recording_url:
        transcript = transcribe_with_whisper(recording_url)
        summary = summarize_call(transcript)
        print("Summary:", summary)
    else:
        print("No recording found.")
