require('dotenv').config();
const twilio = require('twilio');
const axios = require('axios');
const fs = require('fs');

// Twilio configuration
const accountSid = process.env.TWILIO_ACCOUNT_SID;
const authToken = process.env.TWILIO_AUTH_TOKEN;
const twilioClient = twilio(accountSid, authToken);
const twilioPhoneNumber = process.env.TWILIO_PHONE_NUMBER;

// OpenAI configuration
const openAiApiKey = process.env.OPENAI_API_KEY;

// Outbound Call Function
async function makeCall(toNumber) {
    try {
        const call = await twilioClient.calls.create({
            to: toNumber,
            from: twilioPhoneNumber,
            url: 'http://demo.twilio.com/docs/voice.xml',
            record: true
        });

        console.log('Call initiated:', call.sid);
        return call.sid;
    } catch (error) {
        console.error('Error making the call:', error.message);
        return null;
    }
}

// Transcribe & Summarize Function
async function transcribeAndSummarize(audioUrl) {
    try {
        const response = await axios.post('https://api.openai.com/v1/audio/transcriptions', {
            file: audioUrl,
            model: 'whisper-1'
        }, {
            headers: {
                'Authorization': `Bearer ${openAiApiKey}`,
                'Content-Type': 'multipart/form-data'
            }
        });

        const transcription = response.data.text;
        console.log('Transcription:', transcription);

        const summaryResponse = await axios.post('https://api.openai.com/v1/completions', {
            model: 'text-davinci-003',
            prompt: `Summarize the following conversation: ${transcription}`,
            temperature: 0.5,
            max_tokens: 200
        }, {
            headers: {
                'Authorization': `Bearer ${openAiApiKey}`,
                'Content-Type': 'application/json'
            }
        });

        const summary = summaryResponse.data.choices[0].text.trim();
        console.log('Summary:', summary);

        return { transcription, summary };
    } catch (error) {
        console.error('Error transcribing or summarizing:', error.message);
        return null;
    }
}

// Test the Call
(async () => {
    const callSid = await makeCall('+1234567890'); // Replace with the receiver's phone number
    if (callSid) {
        console.log(`Call initiated successfully. Call SID: ${callSid}`);
    }
})();
