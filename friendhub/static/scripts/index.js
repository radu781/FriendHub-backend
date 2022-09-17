const postButton = document.querySelector("#submit-post-button")
const textArea = document.querySelector("#text")
textArea.addEventListener("input", (event) => {
    console.log(textArea.value)
    if (textArea.value !== "") {
        postButton.disabled = false
        postButton.style.color = "white"
        postButton.style.backgroundColor = "#4b74e5"
    } else {
        postButton.disabled = true
        postButton.style.color = "#6d6d6d"
        postButton.style.backgroundColor = "#839de4"
    }
})