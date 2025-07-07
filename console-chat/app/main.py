from pathlib import Path
from app.boot_openapi import  start

import traceback

print("Iniciando start...")
def main():
    try:
        # start bussiness code
        start()
    except Exception as e:
        
        print(f"⚠️ Error atrapado: {e}")
        traceback.print_exc()
 


if __name__ == "__main__": 
    main()
