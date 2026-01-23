import base64
from datetime import datetime
from repository.database import db


class Payment(db.Model):
    # id, value, paid, bank_payment_id, qr_code, expiration_date
    id = db.Column(db.Integer, primary_key=True)
    value=db.Column(db.Float)
    paid = db.Column(db.Boolean, default=False)
    bank_payment_id = db.Column(db.String(200), nullable=True)
    qr_code= db.Column(db.String(100), nullable=True)
    expiration_date=db.Column(db.DateTime)

    def to_dict(self):
        # converte as colunas para um dict e trata bytes/datetime
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for k, v in d.items():
            if isinstance(v, bytes):
                try:
                    d[k] = v.decode('utf-8')  # tenta decodificar como UTF-8
                except Exception:
                    d[k] = base64.b64encode(v).decode('ascii')  # fallback: base64
            elif isinstance(v, datetime):
                d[k] = v.isoformat()
        return d