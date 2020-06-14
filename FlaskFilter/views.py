from FlaskFilter import app, wd, mhdb
from flask import render_template, jsonify, request
from os import getcwd, path

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hello")
def hello():
    return "Testing"

@app.route("/init")
def init_board():
    return "Init"

@app.route("/headers/<weapon_type>")
def get_info(weapon_type):
    weapon = mhdb.selectable_weapons[weapon_type]
    weapon_info = dict();

    weapon_info["headers"] = weapon.HEADERS
    weapon_info["weapon_parameters"] = weapon.WEAPON_PARAMETERS
    weapon_info["filterables"] = weapon.FILTERABLES

    return weapon_info
@app.route("/weapon/list")
def get_weapon_list():
    return jsonify(list(mhdb.selectable_weapons.keys()))

@app.route("/weapon/<weapon_type>", methods=['GET'])
def palico(weapon_type):
    p = path.dirname(getcwd()) + "/Data/mhgu.db"
    weapon_db = mhdb.selectable_weapons[weapon_type](p)

    for filter in request.args:
        selected_value = int(request.args[filter])
        if filter != "order by":
            weapon_db.add_filter(filter, selected_value)
        else:
            weapon_db.order_results_by(selected_value)

    info = weapon_db.execute()
    info.insert(0, weapon_db.HEADERS)
    return jsonify(info)

@app.route("/about")
def about():
    return "All about Flask"
