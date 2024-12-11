# PDF Chat API

## Overview

The **PDF Chat API** is a backend service built with **FastAPI** that allows users to:

1. Upload PDF documents.
2. Extract text and metadata from the uploaded PDFs.
3. Interact with the PDF content using a Large Language Model (LLM) - in this case, Google’s Gemini API.
4. Query the PDF content through a chat-like interface and receive context-aware answers.

This application showcases:
- Integration with external LLM (Gemini API).
- File handling and PDF text extraction.
- Rate limiting to control request frequency.
- Logging and error handling.
- Testing with pytest.
- Containerization with Docker.

## Key Features

- **Upload PDF Files**: Upload a PDF and get back a `pdf_id` for future references.
- **Chat with a PDF**: Query the previously uploaded PDF content and get contextually relevant answers from the LLM.
- **LLM Integration (Gemini)**: Leverages Google’s Gemini 1.5 model to generate intelligent responses.
- **Rate Limiting**: Uses `slowapi` to prevent abuse and rate-limit requests per IP.
- **Robust Logging**: Logs are written to both console and rotating log files. Errors are also logged separately.
- **Testing**: Includes integration tests for both PDF upload and chat functionalities.
- **Docker**: Easily build and run the application in a containerized environment.

## Project Structure

```
PDF-Chat-API/
├─ app/
│  ├─ core/
│  │  ├─ config.py
│  │  └─ logger.py
│  ├─ models/
│  │  └─ state.py
│  ├─ routers/
│  │  ├─ pdf.py
│  │  └─ chat.py
│  ├─ services/
│  │  ├─ pdf_service.py
│  │  └─ llm_service.py
│  ├─ utils/
│  │  └─ pdf_utils.py
│  └─ main.py
├─ tests/
│  ├─ test_chat.py
│  ├─ test_pdf.py
│  └─ dummy.pdf
├─ logs/
│  ├─ app.log
│  └─ error.log
├─ requirements.txt
├─ Dockerfile
├─ .env (not committed to version control)
└─ README.md
```

## Setup Instructions

### 1. Prerequisites

- **Python 3.9+** recommended.
- A **Google Gemini API Key** (`GEMINI_API_KEY`).

### 2. Clone the Repository

```bash
git clone https://github.com/kerem-ozt/PDF-Chat-API.git
cd PDF-Chat-API
```

### 3. Create and Activate a Virtual Environment (if running locally)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

**Key Dependencies:**
- **FastAPI**, **uvicorn**, **gunicorn**: For the API server.
- **python-dotenv**: For loading environment variables from `.env`.
- **google-generativeai**: For integrating with the Gemini API.
- **pypdf**: For reading PDF files.
- **slowapi**: For rate limiting.
- **python-json-logger**: For JSON formatted logs.
- **fpdf**, **pytest**: For testing.

### 5. Environment Variables

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

Ensure your `.env` file is listed in `.gitignore` to avoid committing secrets.

### 6. Running the Application Locally

```bash
uvicorn app.main:app --reload
```

The app runs at [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 7. Docker Usage

A `Dockerfile` is included to build and run the application in a container.

**Build the image:**
```bash
docker build -t pdf-chat-api .
```

**Run the container:**
You must supply the `GEMINI_API_KEY` as an environment variable:
```bash
docker run -p 8000:8000 -e GEMINI_API_KEY=your_actual_key pdf-chat-api
```

Access the API at [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 8. API Endpoints

#### Health Check

- **GET** `/health`
- **Description:** Check if the API is up.
- **Rate Limit:** 1 request per minute.

**Example:**
```bash
curl http://127.0.0.1:8000/health
```

#### Upload PDF

- **POST** `/v1/pdf`
- **Description:** Upload and register a PDF, returns a `pdf_id`.
- **Input:** `multipart/form-data` with a `file` field containing the PDF.
- **Rate Limit:** 5 requests per minute (global default, can adjust in code).

**Example:**
```bash
curl -X POST "http://127.0.0.1:8000/v1/pdf" \
-F "file=@/path/to/your.pdf"
```

**Response:**
```json
{
  "pdf_id": "unique_pdf_identifier"
}
```

#### Chat with PDF

- **POST** `/v1/chat/{pdf_id}`
- **Description:** Query the content of an already uploaded PDF.
- **Input:** JSON body with a `"message"` field.
- **Rate Limit:** 3 requests per minute for this endpoint.

**Example:**
```bash
curl -X POST "http://127.0.0.1:8000/v1/chat/{pdf_id}" \
-H "Content-Type: application/json" \
-d '{"message":"What is this PDF about?"}'
```

**Response:**
```json
{
  "response": "The PDF is about ..."
}
```

### 9. Logging

Logs are stored in `logs/` directory:

- **app.log**: INFO and above logs. Uses `RotatingFileHandler` with max size of 5MB and keeps 5 backups.
- **error.log**: ERROR and above logs for critical issues.
- Logs are also printed to the console in JSON format.

You can tail the logs:
```bash
tail -f logs/app.log
```

### 10. Testing

The project includes integration tests under `tests/`:

- `test_pdf.py`: Tests the PDF upload endpoint.
- `test_chat.py`: Tests the chat endpoint (uploads a PDF first, then queries it).

To run tests:
```bash
python -m pytest
```