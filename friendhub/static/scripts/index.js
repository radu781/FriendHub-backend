import { clearAndInsertStatus } from "./auth/base.js"

const postButton = document.querySelector("#submit-post-button")
const textArea = document.querySelector("#text")
if (textArea && postButton) {
    textArea.addEventListener("input", (event) => {
        if (textArea.value !== "") {
            postButton.disabled = false
            postButton.style.color = "white"
            postButton.style.backgroundColor = "#4b74e5"
            postButton.style.cursor = "pointer"
        } else {
            postButton.disabled = true
            postButton.style.color = "#6d6d6d"
            postButton.style.backgroundColor = "#839de4"
            postButton.style.cursor = "default"
        }
    })
}

const createPostForm = document.querySelector("#create-post-form")
createPostForm.onsubmit = function(event) {
    const textInput = document.querySelector("#text")
    const imageInput = document.querySelector("#image-upload")
    const videoInput = document.querySelector("#video-upload")
    const audioInput = document.querySelector("#audio-upload")

    event.preventDefault()
    if (textInput.value === "") {
        clearAndInsertStatus("bad-input", _("Post description cannot be empty"), "text")
        return
    }

    let formData = new FormData()
    formData.append("text", textInput.value)
    if (imageInput.files.length > 0) {
        formData.append("image-upload", imageInput.files[0])
    }
    if (videoInput.files.length > 0) {
        formData.append("video-upload", videoInput.files[0])
    }
    if (audioInput.files.length > 0) {
        formData.append("audio-upload", audioInput.files[0])
    }
    let xmlHttp = new XMLHttpRequest()
    xmlHttp.open("POST", `/api/upload`, true)
    xmlHttp.responseType = "json"
    xmlHttp.send(formData);
    xmlHttp.onload = function() {
        clearAndInsertStatus("good-input", _("Uploaded, redirecting soon..."), "text")
        window.location = "/"
    }
}