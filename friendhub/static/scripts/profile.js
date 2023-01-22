const addFriend = document.querySelector("#add-friend-form")
const targetId = addFriend.dataset.targetId
const requestType = addFriend.dataset.type
addFriend.addEventListener("submit", (event) => {
    event.preventDefault()
    let xmlHttp = new XMLHttpRequest()
    xmlHttp.open("POST", `/api/relationship?userId=${targetId}&type=${requestType}`, true)
    xmlHttp.responseType = "json"
    xmlHttp.send()
})

function changeButtonText(text) {
    const friendButton = document.querySelector(".profile-and-name-buttons").querySelector("button")
    friendButton.innerHTML = _("Request sent")
}