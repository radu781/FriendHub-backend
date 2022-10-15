const profileMenu = document.querySelector(".my-profile")
const profileOptions = document.querySelector("#options-list")
const optionsList = document.querySelector("#options-list")

function onMouseOver() {
    profileOptions.style.display = "inline"
}

function onMouseOff() {
    profileOptions.style.display = "none"
}
profileMenu.addEventListener("mouseenter", onMouseOver)
profileMenu.addEventListener("mouseleave", onMouseOff)
