from flask import Flask, jsonify, request
from repository.database import db
from model.payment import Payment
from datetime import datetime, timedelta


app = Flask(__name__)


app.config['SECRET_KEY'] = "your_secret_key"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/webhook'


db.init_app(app)


@app.route('/payments/pix', methods=['POST'])
def create_payment_pix():
    data = request.get_json()

    if 'value' not in data:
        return jsonify({"message": "invalid value"}), 400

    expiration_date = datetime.now() + timedelta(minutes=30)

    new_payment = Payment(value=data['value'], expiration_date=expiration_date)

    db.session.add(new_payment)
    db.session.commit()

    return jsonify({
        "message": "The payment has been created",
        "payment": new_payment.to_dict(),
        })


@app.route('/payments/pix/confirmation', methods=['POST'])
def confirmation_pix():
    return jsonify({"message": "The payment has been confirmed"})


@app.route('/payments/pix/<int:payment_id>', methods=['GET'])
def payment_pix_page(payment_id):
    return 'pagamento pix'


if __name__ == '__main__':
    app.run(debug=True)