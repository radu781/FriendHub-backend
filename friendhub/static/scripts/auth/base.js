export function clearOldDiv() {
    let statusDiv = document.querySelector(".bad-input")
    if (statusDiv) {
        statusDiv.parentElement.removeChild(statusDiv)
    }
    statusDiv = document.querySelector(".good-input")
    if (statusDiv) {
        statusDiv.parentElement.removeChild(statusDiv)
    }
}

export function clearAndInsertStatus(className, text) {
    let newDiv = document.createElement("div")
    clearOldDiv()
    newDiv.classList.add(className)
    newDiv.innerHTML = text
    let inputs = document.querySelector("#inputs")
    inputs.insertAdjacentElement("afterend", newDiv)
}