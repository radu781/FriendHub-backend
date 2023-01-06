function run(code) {
    document.write(_("Processing..."))

    json = JSON.parse(code)
    let xmlHttp = new XMLHttpRequest()
    xmlHttp.responseType = "json"
    let params = ""
    for (const key in json["params"]) {
        params += `${key}=${json["params"][key]}&`
    }
    params = params.slice(0, params.length - 1)
    xmlHttp.open(json["method"], `${json["endpoint"]}?${params}`, true)
    xmlHttp.send(json["body"])
    xmlHttp.onload = function() {
        if (xmlHttp.status >= 400 && xmlHttp.status < 500) {
            document.write("Got client side error: ", xmlHttp.response["error"])
        } else if (xmlHttp.status >= 200 && xmlHttp.status < 300) {
            document.write(_("Redirecting soon..."))
            window.location.replace(json["redirect"])
        } else {
            document.write("Unexpected error", xmlHttp.status, xmlHttp.response["error"] | xmlHttp.response["reason"])
        }
    }
}