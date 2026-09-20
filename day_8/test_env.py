from dotenv import load_dotenv # type: ignore
import os

load_dotenv()

APP_NAME=os.getenv("APP_NAME")
APP_VERSION=os.getenv("APP_VERSION")
PORT=os.getenv("PORT")
HOST=os.getenv("HOST")
APP_DEBUG=os.getenv("APP_DEBUG")
ENVIRONMENT=os.getenv("ENVIRONMENT")

print(f"APP_NAME: {APP_NAME}")
print(f"APP_VERSION: {APP_VERSION}")
print(f"PORT: {PORT}")
print(f"HOST: {HOST}")
print(f"APP_DEBUG: {APP_DEBUG}")
print(f"ENVIRONMENT: {ENVIRONMENT}")

print(type(APP_NAME))
print(type(APP_VERSION))
print(type(PORT))
print(type(HOST))
print(type(APP_DEBUG))
print(type(ENVIRONMENT))