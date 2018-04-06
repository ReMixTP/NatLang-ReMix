from flask import Flask, jsonify, make_response, request


app = Flask(__name__)

VERSION = (0, 1, 0)
VERSION_STRING = "{}.{}.{}".format(*VERSION)

LANG_ID = "lang.natural.english"


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route("/")
def entry():
    return jsonify([{
        "id": "com.natlang",
        "name": "NatLang",
        "website": "https://aaron.stockdill.nz/",
        "version": VERSION_STRING,
        "description": "A placeholder natural language reasoner.",
        "icon": "",
        "base": "http://aarons-macbook.local:5003/api/{}".format(VERSION_STRING),
        "provides": {
            "reason": "/reason",
            "translate": "/translate"
        }
    }])


@app.route("/api/{}/reason".format(VERSION_STRING))
def reason_base():
    return jsonify({
        "result": "success",
        "reasoning": [[LANG_ID, "manual", "reasonEnglish", "Manually reason with natural language."]]
    })


def common_transform(json_data, key):
    old_goal = json_data.get(key)
    new_goal_data = json_data.get("extraInfo")
    new_goal = old_goal.copy()
    new_goal["data"] = new_goal_data
    new_goal["language"] = LANG_ID
    print(new_goal)
    return new_goal


@app.route("/api/{}/reason/apply".format(VERSION_STRING), methods=["GET", "POST"])
def reason_apply():
    rule_id = request.args.get("id")
    if rule_id == "reasonEnglish":
        json_data = request.get_json()
        new_goal = common_transform(json_data, "goal")
        return jsonify({
            "result": "success",
            "newGoals": [new_goal] if new_goal["data"] else []
        })
    else:
        return jsonify({
            "result": "failure",
            "reason": "Unknown rule ID."
        })


@app.route("/api/{}/translate".format(VERSION_STRING))
def translate_base():
    other_languages = ["lang.speedith", "lang.isabelle"]
    def all_pairs(xs, ys):
        for x in xs:
            for y in ys:
                yield (x, y)
                yield (y, x)
    return jsonify({
        "result": "success",
        "translations": [(from_lang, to_lang, "manual")
                         for (from_lang, to_lang) in all_pairs(other_languages, [LANG_ID])]
    })


@app.route("/api/{}/translate/translate".format(VERSION_STRING), methods=["GET", "POST"])
def translate_apply():
    from_language = request.args.get("from")
    to_language = request.args.get("to")
    print(LANG_ID in {from_language, to_language}, LANG_ID, from_language, to_language)
    if LANG_ID in {from_language, to_language}:
        json_data = request.get_json()
        new_goal = common_transform(json_data, "formula")
        return jsonify({
            "result": "success",
            "formula": new_goal
        })
    else:
        return jsonify({
            "result": "failure",
            "reason": "Unable to translate when one of the languages is not {}".format(LANG_ID)
        })

if __name__ == "__main__":
    app.run()
