import google.generativeai as genai
import os
from app.core.config import GEMINI_API_KEY
from app.core.logger import logger
import asyncio

genai.configure(api_key=GEMINI_API_KEY)

def generate_chat_response(pdf_text: str, user_message: str) -> str:
    try:
        prompt = f"""
        The user has a PDF with the following content:
        {pdf_text}

        The user's question is: {user_message}

        Please answer concisely and accurately using only the information from the PDF.
        """

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        if response.candidates and len(response.candidates) > 0:
            first_candidate = response.candidates[0]
            if first_candidate.content and first_candidate.content.parts:
                answer = first_candidate.content.parts[0].text.strip()
                return answer
            else:
                logger.warning("No content parts returned from Gemini API")
                return "Sorry, I couldn't generate a response."
        else:
            logger.warning("No candidates returned from Gemini API")
            return "Sorry, I couldn't generate a response."
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return "An error occurred while communicating with the LLM."


async def ask_llm(pdf_text: str, user_message: str) -> str:
    try:
        return await asyncio.wait_for(
            asyncio.to_thread(generate_chat_response, pdf_text, user_message),
            timeout=20 
        )
    except asyncio.TimeoutError:
        logger.error("LLM API call timed out.")
        return "The LLM took too long to respond, please try again later."
