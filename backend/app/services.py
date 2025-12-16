import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from .models import MemoryProfile

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class LLMService:

    @staticmethod
    def extract_memory(chat_text: str) -> dict:
        """
        Extracts structured memory from raw text.
        Handles JSON parsing errors robustly.
        """
        system_prompt = """
        You are a Psychographic Extraction Engine. Analyze the chat logs.
        Return ONLY valid JSON with these keys:
        - "user_preferences": list of strings
        - "emotional_patterns": list of strings (moods, triggers)
        - "facts": dictionary of key-value pairs (names, dates, entities)
        
        Do not include markdown formatting.
        """ 

        try:
            response = client.chat.completions.create(
                model = "gpt-4o-mini",
                messages=[
                    {"role": "system", "content":system_prompt},
                    {"role": "user", "content": f"Chat Logs:\n{chat_text}"}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            # Parse JSON 
            content = response.choices[0].message.content
            return json.loads(content)
        
        except Exception as e:
            # Fallback for errors
            return {
                "user_preferences": [],
                "emotional_patterns": ["Error analyzing emotions"],
                "facts": {"error": str(e)}
            }
        
    @staticmethod
    def generate_response(query: str, memory: dict, persona: str):
        """
        Generates two responses:
        1. Standard (Before)
        2. Personalized (After)
        """

        # 1. Standard Response
        std_response= client.chat.completions.create(
            model= "gpt-4o-mini",
            messages=[
                {"role": "user", "content": query}
            ]
        )

        normal_text = std_response.choices[0].message.content

        # 2. Personalized "Engine" Response
        persona_instructions = {
            "Calm Mentor": "Tone: Wise, patient, encouraging. Use metaphors.",
            "Witty Friend": "Tone: Casual, sarcastic, uses emojis. Short sentences.",
            "Therapist": "Tone: Empathetic, validating, asks deep questions."
        }

        system_prompt = f"""
        ACT AS: {persona}
        {persona_instructions.get(persona, "Tone: Helpful")}

        CORE MEMORY (Use this to personalize):
        {json.dumps(memory, indent=2)}

        INSTRUCTIONS:
        1. Acknowledge the user's specific context (from memory).
        2. Match the requested tone perfectly.
        3. Do not explicitly say "According to my memory". Be natural.
        """

        pers_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages= [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0.7
        )

        personalized_text= pers_response.choices[0].message.content

        return normal_text, personalized_text
    
    

