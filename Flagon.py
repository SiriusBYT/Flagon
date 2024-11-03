import flask
import json
import os

app = flask.Flask("Flagon")
Route_Prefix = "/flashcord/store/addons"

""" Common Error Codes """
@app.errorhandler(404)
def Not_Found(Error):
    return flask.redirect("https://dev.sirio-network.com/404")
@app.errorhandler(401)
def Unauthorised():
    return flask.redirect("https://dev.sirio-network.com/401")
@app.errorhandler(403)
def Access_Denied():
    return flask.redirect("https://dev.sirio-network.com/403")
@app.errorhandler(500)
def Server_Error():
    return flask.redirect("https://dev.sirio-network.com/500")

""" Web Pages """

# Unnecessary, this isn't the API.
@app.route(f"{Route_Prefix}/<addon_type>")
def addons(addon_type=None):
    if addon_type == "plugins" or addon_type == "themes":
        Addons = ls(f"addons/{addon_type}/")
        if Addons[0] == None:
            return "No addons found."
        return Addons[0]
    else:
        return "Invalid Addon Type"

# Builds and returns the Addon page following the Flagon format.
@app.route(f"{Route_Prefix}/<addon_type>/<addon>")
def addon(addon_type=None, addon=None):
    Plugins = ls(f"addons/{addon_type}/")
    if addon in Plugins[0]:
        Addon_Files = ls(f"addons/{addon_type}/{addon}")

        with open(f"addons/{addon_type}/{addon}/manifest.json", "r", encoding="UTF-8") as Manifest:
            manifest = json.load(Manifest)
        with open(f"addons/{addon_type}/{addon}/description.html", "r", encoding="UTF-8") as Description:
            description = ""
            for line in Description:
                description+=line
        return Build_Addon_Page(addon_type, addon, manifest, description)
    else:
        return "Addon not found"

""" Functions """
def Build_Addon_Page(addon_type, addon, manifest, description):
    return [addon_type, addon, manifest, description]

def ls(Folder):
    Path = os.getcwd() + "/" + Folder
    try:
        Results = next(os.walk(Path))
        return [Results[1], Results[2]]
    except: return [None, None]

if __name__ == '__main__':
    app.run(debug=True, host = '192.168.1.2', port = 8000)