from flask import Flask, request, render_template, jsonify
from models import db, Patient
from playhouse.shortcuts import model_to_dict

app = Flask(__name__)

db.connect()
db.create_tables([Patient])

@app.route('/data', methods=['GET'])
def get_query_string():
    all_args = request.args.to_dict()
    return render_template('index.html', all_data=all_args, username=all_args["username"], type=all_args["type"])

# Find Patient using "Phone Number" in query params
# http://127.0.0.1:5000/edit?phone=16692419870
@app.route('/get_profile')
def get_profile():
    all_args = request.args.to_dict()
    pat = Patient.get(Patient.phone == all_args["phone"])
    patient = {
        "username" : pat.username,
        "type" : pat.type,
        "calltime": pat.calltime,
        "phone": pat.phone,
        "timezone": pat.timezone
    }
    print(f"patient: {patient}")
    return jsonify(patient)

# Edit Patient using "Phone Number" in query params
# http://127.0.0.1:5000/edit?username=Alice&&new_username=Reggie&&phone=16692419870
@app.route('/edit')
def edit_profile():
    all_args = request.args.to_dict()
    pat_details = Patient.select(
        ).where(
            Patient.phone == all_args["phone"]
        ).get()
    pat_details.username = all_args["new_username"]
    pat_details.save()
    edited_pat = Patient.select(
        ).where(
            Patient.username == all_args["new_username"]
        ).get()
    return {"success" : 200, "newuser" : model_to_dict(edited_pat)}

# http://127.0.0.1:5000/new_user?username=testuser&&type=patient&&timezone=US/Pacific&&calltime=5:30:00&&phone=123-456-789
@app.route('/new_user')
def new_user():
    all_args = request.args.to_dict()
    rec1 = Patient.create(**all_args)
    rec1.save()
    return {"success" : 200, "newuser" : model_to_dict(rec1)}

if __name__ == "__main__":
    app.run(debug=True)