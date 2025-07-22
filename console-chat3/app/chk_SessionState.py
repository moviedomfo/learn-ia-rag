
from app.common.Session.SessionState import SessionState

nro = "1234567890"
def run_check():
    try:
        state1 :SessionState= SessionState(phone=nro)
        print(state1.socio)
  
        state1.socio.nombre = "John Doe"
        state1.persist_socio()
        print("Socio updated:", state1.socio)


        socio = state1.has_socio(nro)
        print("Has socio 1 :", socio)

        state2 :SessionState= SessionState(phone="123921087")
        state2.socio.nombre = "Catalina Oviedo "
        state2.socio.nro_socio = "8090"
        state2.socio.nro_abonado = "8090"
        state2.persist_socio()
        print("Has socio 2:", state2.socio)

    except Exception as e:
        print(f"❌ Error {e}")

if __name__ == "__main__":
    run_check()