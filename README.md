# Transcription and Summarization Tool

A web application that records audio, transcribes it to text on the client side, sends it to a backend for summarization, and displays both the raw transcription and a refined summary.

## Features
- **Audio Recording**: Records audio directly from the user's microphone.
- **Speech to Text**: Converts the recorded audio to text on the client side.
- **Summarization**: Sends the transcribed text to the backend, which processes it using an LLM (Large Language Model) to return a structured summary.
- **Real-Time Display**: Displays both the raw transcription and the refined summary.

## Technologies Used
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: FastAPI (Python)
- **LLM**: OpenRouter API for summarization
- **Audio Recording**: Web Audio API (JavaScript)


