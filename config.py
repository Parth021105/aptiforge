import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'aptiforge-super-secret-key-2026')
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/aptiforge')
    AI_API_KEY = os.environ.get('AI_API_KEY', '')
    AI_PROVIDER = os.environ.get('AI_PROVIDER', 'groq').lower() # groq, openai, openrouter, ollama, or fallback
    AI_MODEL = os.environ.get('AI_MODEL', '')
    OLLAMA_HOST = os.environ.get('OLLAMA_HOST', 'http://localhost:11434')

