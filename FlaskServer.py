# FlaskServ.py
from flask import Flask, request, abort, render_template
import queryandmap as qm
app = Flask(__name__)

mappath = qm.main()
print(mappath)
@app.route("/")
def JinjaTemplate():
    render_template('index.html', my_string="Wheeeee!", my_list=[0,1,2,3,4,5], map_path = mappath)

if __name__ == "__main__":
    app.run(port=8000, debug=True)
