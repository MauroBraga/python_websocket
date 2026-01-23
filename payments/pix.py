import uuid
import qrcode

class Pix:
    def __init__(self):
        pass

    def create_payment(self) -> str:
        #cria um pagamento pix falso

        bank_payment_id = str(uuid.uuid4())

        # Gera um QR code simples com o bank_payment_id
        hash_payment = f"hash_payment://{bank_payment_id}"
        img = qrcode.make(hash_payment)
        img.save(f"static/img/qr_code_{bank_payment_id}.png")



        return {"banck_payment_id": bank_payment_id, "qr_code": f"qr_code_{bank_payment_id}"}