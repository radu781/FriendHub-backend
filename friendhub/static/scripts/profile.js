const addFriend = document.querySelector("#add-friend-form")
addFriend.addEventListener("submit", (event) => {
    event.preventDefault()
    let xmlHttp = new XMLHttpRequest()
    xmlHttp.open("POST", `/api/relationship?userId=${1}&type=request_sent`, true)
    xmlHttp.responseType = "json"
    xmlHttp.send()
    xmlHttp.onload = function() { window.location = "/" }
})

function changeButtonText(text) {
    const friendButton = document.querySelector(".profile-and-name-buttons").querySelector("button")
    friendButton.innerHTML = _("Request sent")
}