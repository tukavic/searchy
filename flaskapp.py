from flask import Flask, render_template, request
import searchy
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    # if request.method == "POST":
    #     name = request.form["search"]
    #     return render_template("index.html", name=name)

    # # input_value = get_input()
    # # return render_template("index.html", name=None, input_value=input_value)
    return render_template("index.html", name=None, variable='Enter your search...')

@app.route("/get_input", methods=["POST"])
def get_input():
    input_value = request.form["input"]
    return input_value

@app.route("/run_searchy", methods=["POST"])
def run_searchy():
    input_value = request.form["input"]
    search_output = searchy.return_results(input_value)
    return search_output

if __name__ == "__main__":
    app.run(debug=True)