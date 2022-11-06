import { clearAndInsertStatus } from "./base.js"

const requiredFields = [
    document.querySelector("#email"),
    document.querySelector("#password"),
    document.querySelector("#password-confirm"),
    document.querySelector("#first-name"),
]
const extraFields = [
    document.querySelector("#middle-name"),
    document.querySelector("#last-name"),
    document.querySelector("#country"),
    document.querySelector("#city"),
]

for (let item of requiredFields) {
    item.addEventListener("keyup", onKeyPressed)
}
for (let item of extraFields) {
    item.addEventListener("keyup", onKeyPressed)
}


function onKeyPressed(event) {
    if (event.key !== "Enter") {
        return
    }
    for (let item of requiredFields) {
        if (item.value === "") {
            clearAndInsertStatus("bad-input", _("Missing required fields"), "inputs")
            return
        }
    }

    let xmlHttp = new XMLHttpRequest();
    let mainArgs = ""
    for (let item of requiredFields) {
        mainArgs += `${item.name}=${item.value}&`
    }
    mainArgs = mainArgs.slice(0, -1)
    let extraArgs = ""
    for (let item of extraFields) {
        if (item.value !== "") {
            extraArgs += `&${item.name}=${item.value}`
        }
    }
    xmlHttp.open("POST", `/api/register?${mainArgs}${extraArgs}`, true);
    xmlHttp.responseType = "json"
    xmlHttp.send();
    xmlHttp.onload = function() {
        if (xmlHttp.status < 400) {
            clearAndInsertStatus("good-input", _('Account created'), "inputs")

            let xmlHttp = new XMLHttpRequest();
            xmlHttp.open("POST", `/api/login?email=${requiredFields[0].value}&password=${requiredFields[1].value}`, true);
            xmlHttp.responseType = "json"
            xmlHttp.send();
            xmlHttp.onload = function() {
                clearAndInsertStatus("good-input", _('Redirecting soon...'), "inputs")
                window.location = "/"
            }
        } else {
            let newDivText = ""
            switch (xmlHttp.response["reason"]) {
                case "user already exists":
                    newDivText = _("An user with the same email address already exists")
                    break
                case "password mismatch":
                    newDivText = _("Passwords are not matching")
                    break
                default:
                    newDivText = xmlHttp.response["reason"];
            }
            clearAndInsertStatus("bad-input", newDivText, "inputs")
        }
    }
}

let passwordField = document.querySelector("#password")
let passwordConfirmField = document.querySelector("#password-confirm")

passwordField.addEventListener("keyup", onPasswordFieldChanged, false)
passwordConfirmField.addEventListener("keyup", onPasswordFieldChanged, false)

function onPasswordFieldChanged(event) {
    if (event.key === "Enter") {
        return
    }
    if (passwordField.value !== passwordConfirmField.value) {
        passwordConfirmField.style.borderColor = "red"
        passwordConfirmField.style.borderWidth = "2px"
    } else {
        passwordConfirmField.style.borderColor = "#445a9b"
        passwordConfirmField.style.borderWidth = "1px"
    }
}