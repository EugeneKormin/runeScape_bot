from flask import Flask, render_template
from Utility import Utility


app = Flask(__name__)
utility = Utility()


@app.route('/', methods=['GET', 'POST'])
def home():
    data = utility.read_json(json_name="status")
    return render_template(
        "index.html",

        x=data["player_position"]["x"],
        y=data["player_position"]["y"],

        current_ore_type=data["current_ore_type"],
        current_ore_status=data["current_ore_status"],

        player_location=data["player_location"],
        distance_to_mine=data["distances"]["to_mine"],
        distance_to_furnace=data["distances"]["to_furnace"],
        distance_to_forge_and_anvil=data["distances"]["to_forge_and_anvil"],
        hovered_ore=data["hovered_ore"],
        current_action=data["current_action"],
        click_is_required=data["click_is_required"]
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
