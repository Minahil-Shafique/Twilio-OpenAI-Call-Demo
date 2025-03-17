# Mini Twilio + OpenAI "Outbound Call" Demo

This project demonstrates a simple implementation of Twilio outbound calling, call recording, transcription using OpenAI Whisper, and summarization using OpenAI GPT. The final output is a structured JSON object containing key conversation points.

## 🚀 Features
- Outbound call to a specified phone number via Twilio.
- Recording of the call.
- Transcription of the recorded audio using OpenAI Whisper.
- Summarization of the transcription using OpenAI GPT.
- Display of structured JSON output.

## 📋 Requirements
- Python 3.x
- Twilio Account & API credentials
- OpenAI API Key

## 📁 Installation
1. Clone the repository:
```bash
   git clone https://github.com/Minahil-Shafique/Twilio-OpenAI-Call-Demo
```
2. Navigate to the project directory:
```bash
   cd Twilio-OpenAI-Call-Demo
```
3. Create and activate a virtual environment:
```bash
   python -m venv venv
   source venv/bin/activate    # On Windows: .\venv\Scripts\activate
```
4. Install the dependencies:
```bash
   pip install -r requirements.txt
```

## 🔑 Environment Variables
Create a `.env` file in the root directory with the following keys:
```env
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
OPENAI_API_KEY=your_openai_api_key
```

## 💡 Usage
1. Modify the `main.py` file to enter your `to_number`, `from_number`, and `twiml_url`.
2. Run the script:
```bash
   python main.py
```
3. View the JSON summary output in the terminal.

## 📄 Example Output
```json
{
  "patient_name": "John Snow",
  "reason": "Prescription inquiry",
  "next_steps": "Send follow-up email"
}
```

## 📌 Important Notes
- Make sure your Twilio number has outbound call capability.
- Ensure your TwiML URL is publicly accessible.
- Hide your credentials by adding `.env` to your `.gitignore` file.

## 📜 License
This project is for assessment purposes only.

