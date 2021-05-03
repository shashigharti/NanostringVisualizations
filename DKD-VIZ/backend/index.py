from flask import Flask, send_file, make_response
from libraries.volcano_plot import volcano_plot
from libraries.umap import umap_plot

app = Flask(__name__)


# @app.route("/api/plots/volcano", methods=["GET"])
# def volcano():
#     return volcano_plot()

#     # return send_file(bytes_obj, attachment_filename="plot.png", mimetype="image/png")


@app.route("/api/plots/umap", methods=["GET"])
def plot(plot_type="map"):
    if plot_type == "map":
        return umap_plot()
    elif plot_type == "volcano":
        return volcano_plot()


if __name__ == "__main__":
    app.run(debug=True)