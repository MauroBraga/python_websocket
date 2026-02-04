from flask import Flask, jsonify, request, send_file, render_template
from jinja2 import TemplateNotFound
from repository.database import db
from model.payment import Payment
from datetime import datetime, timedelta
from payments.pix import Pix
from pathlib import Path
from flask_socketio import SocketIO


app = Flask(__name__, template_folder=str(Path(__file__).parent / "template"))

app.config['SECRET_KEY'] = "your_secret_key"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payments.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/webhook'

db.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*")

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
    data = request.get_json()

    if "bank_payment_id" not in data and "value" not in data:
        return jsonify({"message": "Invalid payment data"}), 400

    payment = Payment.query.filter_by(bank_payment_id=data.get('bank_payment_id')).first()

    if not payment or payment.paid:
        return jsonify({"message": "Payment not found"}), 404

    if payment.value != float(data.get('value')):
        return jsonify({"message": "Invalid payment data"}), 400

    payment.paid= True
    db.session.commit()

    socketio.emit(f'payment-confirmed-{payment.id}')

    return jsonify({"message": "The payment has been confirmed"})


@app.route('/payments/pix/<int:payment_id>', methods=['GET'])
def payment_pix_page(payment_id):
    try:
        payment = Payment.query.get(payment_id)

        if payment.paid:
            return render_template('confirmed_payment.html',
                                   payment_id=payment.id,
                                   value=payment.value
                                   )

        return render_template('payment.html',
                               payment_id=payment.id,
                               value=payment.value,
                               host="http://localhost:5000",
                               qr_code=payment.qr_code)
    except TemplateNotFound:
        return "Template `payment.html` not found in the `templates` folder.", 500

@socketio.on('connect')
def hadle_conect():
    print('Client connected')

if __name__ == "__main__":
    # Only allow Werkzeug when explicitly debugging.
    # In real production, you should run SocketIO with an async server.
    debug = 1
    socketio.run(
        app,
        host="127.0.0.1",
        port="5000",
        debug=debug,
        allow_unsafe_werkzeug=debug,
    )
