import { clearAndInsertStatus, clearOldDiv } from "./base.js"

const requiredFields = [
    document.querySelector("#email"),
    document.querySelector("#password"),
]
for (let item of requiredFields) {
    item.addEventListener("keyup", onKeyPressed)
}

function onKeyPressed(event) {
    if (event.key !== "Enter") {
        return
    }
    for (let item of requiredFields) {
        if (item.value === "") {
            clearAndInsertStatus("bad-input", _("Missing required fields"), "status")
            return
        }
    }

    const emailValue = document.querySelector("#email").value
    const passwordValue = document.querySelector("#password").value
    let xmlHttp = new XMLHttpRequest()
    xmlHttp.open("POST", `/api/login?email=${emailValue}&password=${passwordValue}`, true)
    xmlHttp.responseType = "json"
    xmlHttp.send()
    xmlHttp.onload = function() {
        clearOldDiv()
        if (xmlHttp.status < 400) {
            clearAndInsertStatus("good-input", _('Redirecting soon...'), "status")
            window.location = "/"
        } else {
            let newDivText = ""
            switch (xmlHttp.response["reason"]) {
                case "user does not exist":
                    newDivText = _("Email address does not match any account")
                    break
                case "incorrect password":
                    newDivText = _("Incorrect password")
                    break
                default:
                    newDivText = xmlHttp.response["reason"]
            }
            clearAndInsertStatus("bad-input", newDivText, "status")
        }
    }
}