from repository.database import db

class Payment(db.Model):
    # id, value, paid, bank_payment_id, qr_code, expiration_date
    id = db.Column(db.Integer, primary_key=True)
    value=db.Column(db.Float)
    paid = db.Column(db.Boolean, default=False)
    bank_payment_id = db.Column(db.Integer, nullable=True)
    qr_code= db.Column(db.String(100), nullable=True)
    expirate_date=db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'value': self.value,
            'paid': self.paid,
            'bank_payment_id': self.bank_payment_id,
            'qr_code': self.qr_code,
            'expirate_date': self.expirate_date.isoformat() if self.expirate_date else None
        }