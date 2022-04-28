import json
from flask import Response, Flask, render_template, request, redirect
from entry import entry
from exit import exit

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/entry', methods=['POST', 'GET'])
def entry_():
    plate_id = request.args.get("plate")
    parking_lot_id = request.args.get("parkingLot")
    response = entry(plate_id , parking_lot_id)

    if response == "Car Plate Already in parking lot":
        return Response(mimetype='application/json',
                        response="{'Error': 'Car Plate Already in parking lot'}",
                        status=404)

    return Response(mimetype='application/json',
                    response=json.dumps(response), status=200)


@app.route('/exit', methods=['POST', 'GET'])
def exit_():
    ticket_id = request.args.get("ticketId")
    response = exit(ticket_id)

    if response == "ticket number not recognized":
        return Response(mimetype='application/json',
                        response="{'Error': 'ticket number not recognized'}",
                        status=404)

    return Response(mimetype='application/json',
                    response=json.dumps(response), status=200)

