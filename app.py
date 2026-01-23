from flask import Flask, jsonify, request, send_file
from repository.database import db
from model.payment import Payment
from datetime import datetime, timedelta
from payments.pix import Pix
app = Flask(__name__)


app.config['SECRET_KEY'] = "your_secret_key"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payments.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/webhook'

db.init_app(app)


@app.route('/payments/pix', methods=['POST'])
def create_payment_pix():
    data = request.get_json()

    if 'value' not in data:
        return jsonify({"message": "invalid value"}), 400

    expiration_date = datetime.now() + timedelta(minutes=30)

    new_payment = Payment(value=data['value'], expiration_date=expiration_date)
    pix_obj = Pix()
    data_payment_pix = pix_obj.create_payment()
    new_payment.bank_payment_id = data_payment_pix['banck_payment_id']
    new_payment.qr_code = ''
    new_payment.qr_code=data_payment_pix['qr_code']

    db.session.add(new_payment)
    db.session.commit()


    print(new_payment.to_dict())

    return jsonify({
        "message": "The payment has been created",
        "payment": new_payment.to_dict(),
    })

@app.route('/payments/pix/qr_code/<file_name>', methods=['GET'])
def get_image(file_name):
    return send_file(f"static/img/{file_name}.png", mimetype='image/png')

@app.route('/payments/pix/confirmation', methods=['POST'])
def confirmation_pix():
    return jsonify({"message": "The payment has been confirmed"})


@app.route('/payments/pix/<int:payment_id>', methods=['GET'])
def payment_pix_page(payment_id):
    return 'pagamento pix'


if __name__ == '__main__':
    app.run(debug=True)