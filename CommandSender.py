import assist
import requests
import time
import os
from datetime import datetime

def main():
                response = assist.ask_question_memory("Hello")
                done = assist.TTS(response)

                exit

if __name__ == '__main__':
    main()