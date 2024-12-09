import google.generativeai as genai
import os
from app.core.config import GEMINI_API_KEY
from app.core.logger import logger
import asyncio

genai.configure(api_key=GEMINI_API_KEY)

def generate_chat_response(pdf_text: str, user_message: str) -> str:
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"The user has a PDF with the following content:\n{pdf_text}"},
            {"role": "user", "content": user_message}
        ]

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("Explain how AI works")
        print(response.candidates[0].content.parts[0].text)
        if "candidates" in response and len(response["candidates"]) > 0:
            answer = response["candidates"][0]["content"]
            return answer
        else:
            logger.warning("No candidates returned from Gemini API")
            return "Sorry, I couldn't generate a response."
    except Exception as e:
        logger.error(f"Error in generate_chat_response: {str(e)}")
        return "An error occurred while generating a response."

async def ask_llm(pdf_text: str, user_message: str) -> str:
    return await asyncio.to_thread(generate_chat_response, pdf_text, user_message)
