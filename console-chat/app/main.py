from pathlib import Path
from app.boot_HuggingFace import  LocalVectorChat

import traceback

from app.boot_openapi import ChatBootOpenApi

print("Iniciando start...")
def main():
    try:
        # start bussiness code
        # start()
        # chat = LocalVectorChat()
        chat = ChatBootOpenApi()
        chat.run_chat()
    except Exception as e:
        
        print(f"⚠️ Error atrapado: {e}")
        traceback.print_exc()
 


if __name__ == "__main__": 
    main()
