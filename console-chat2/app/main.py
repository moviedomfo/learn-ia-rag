from pathlib import Path
from app.boot_HuggingFace import  LocalVectorChat

import traceback

from app.boot_openap_2 import ChatBootOpenApi2
from app.boot_llama import ChatBootLlama

print("Iniciando start...")
def main():
    try:
        # start bussiness code
        # start()
        # chat = LocalVectorChat()
        # chat = ChatBootOpenApi2()
        chat = ChatBootLlama()
        chat.run_chat()
    except Exception as e:
        
        print(f"⚠️ Error atrapado: {e}")
        traceback.print_exc()
 


if __name__ == "__main__": 
    main()
