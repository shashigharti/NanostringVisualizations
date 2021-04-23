from flask import Flask, send_file, make_response
from libraries.plot import heatmap_plot
from libraries.volcano_plot import volcano_plot

from bokeh.sampledata.unemployment1948 import data

app = Flask(__name__)


@app.route("/api/plots/volcano", methods=["GET"])
def volcano():
    return volcano_plot()

    # return send_file(bytes_obj, attachment_filename="plot.png", mimetype="image/png")


@app.route("/api/plots/heatmap", methods=["GET"])
def heatmap():
    bytes_obj = heatmap_plot()

    return send_file(bytes_obj, attachment_filename="plot.png", mimetype="image/png")


if __name__ == "__main__":
    app.run(debug=True)