import uuid
import qrcode

class Pix:
    def __init__(self, key: str, amount: float):
        self.key = key
        self.amount = amount

    def create_payment(self) -> str:
        # Simulate QR code generation for Pix payment
        bank_payment_id = str(uuid.uuid4())
        hash_payment = f'hash_payment_{bank_payment_id}'

        #qr code generation
        img = qrcode.make(hash_payment)

        img.save(f"../static/img/qr_code_payment_{bank_payment_id}.png")

        return {"bank_payment_id": bank_payment_id,
                "qr_code": f"qr_code_payment_{bank_payment_id}"
                }