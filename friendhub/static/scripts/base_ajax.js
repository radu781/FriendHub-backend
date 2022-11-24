function onLogoutPressed() {
    let xmlHttp = new XMLHttpRequest()
    xmlHttp.open("POST", `/api/logout`, true)
    xmlHttp.responseType = "json"
    xmlHttp.send()
    xmlHttp.onload = function() { window.location = "/" }
}