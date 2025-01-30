import os
from dotenv import load_dotenv


# Ruta del archivo .env
env_path = os.path.join(os.path.dirname(__file__), '../.env')
print(f"Intentando cargar el archivo .env desde: {env_path}")  # Depuración

# Carga el archivo .env
load_dotenv(dotenv_path=env_path)

# Obtén la API Key
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("API Key no encontrada en el archivo .env.")
else:
    print(f"API Key cargada correctamente: {API_KEY[:5]}...")  # Depuración (solo parte de la clave)