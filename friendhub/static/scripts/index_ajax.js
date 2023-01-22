function upvotePost(postId) {
    let upvoteIcon = document.querySelector(`#upvote_${postId}`)
    let downvoteIcon = document.querySelector(`#downvote_${postId}`)

    let currentState = upvoteIcon.src
    let nextState = ""
    let isPressed = false
    if (currentState.indexOf("_pressed_icon") != -1) {
        nextState = currentState.replace("_pressed_icon", "_icon")
        isPressed = true
    } else {
        nextState = currentState.replace("_icon", "_pressed_icon")
        isPressed = false
    }
    upvoteIcon.src = "static/assets/icons/spinner_icon.svg"
    upvoteIcon.classList.add("spinner")
    let xmlHttp = new XMLHttpRequest()
    const vote = isPressed ? "clear" : "upvote"
    xmlHttp.open("PUT", `/api/post/${postId}?vote=${vote}`, true)
    xmlHttp.responseType = "json"
    xmlHttp.send()
    xmlHttp.onload = function() {
        let xmlHttp = new XMLHttpRequest()
        xmlHttp.open("GET", `/api/post/${postId}`, true)
        xmlHttp.responseType = "json"
        xmlHttp.send()
        xmlHttp.onload = function() {
            let downvoteP = document.querySelector(`#downvote-${postId}`)
            downvoteP.innerHTML = xmlHttp.response["dislikes"]
            let upvoteP = document.querySelector(`#upvote-${postId}`)
            upvoteP.innerHTML = xmlHttp.response["likes"]

            downvoteIcon.src = downvoteIcon.src.replace("_pressed_icon", "_icon")
            upvoteIcon.src = nextState
            upvoteIcon.classList.remove("spinner")
        }
    }
}

function downvotePost(postId) {
    let upvoteIcon = document.querySelector(`#upvote_${postId}`)
    let downvoteIcon = document.querySelector(`#downvote_${postId}`)

    let currentState = downvoteIcon.src
    let nextState = ""
    let isPressed = false
    if (currentState.indexOf("_pressed_icon") != -1) {
        nextState = currentState.replace("_pressed_icon", "_icon")
        isPressed = true
    } else {
        nextState = currentState.replace("_icon", "_pressed_icon")
        isPressed = false
    }
    downvoteIcon.src = "static/assets/icons/spinner_icon.svg"
    downvoteIcon.classList.add("spinner")
    let xmlHttp = new XMLHttpRequest()
    const vote = isPressed ? "clear" : "downvote"
    xmlHttp.open("PUT", `/api/post/${postId}?vote=${vote}`, true)
    xmlHttp.responseType = "json"
    xmlHttp.send()
    xmlHttp.onload = function() {
        let xmlHttp = new XMLHttpRequest()
        xmlHttp.open("GET", `/api/post/${postId}`, true)
        xmlHttp.responseType = "json"
        xmlHttp.send()
        xmlHttp.onload = function() {
            let downvoteP = document.querySelector(`#downvote-${postId}`)
            downvoteP.innerHTML = xmlHttp.response["dislikes"]
            let upvoteP = document.querySelector(`#upvote-${postId}`)
            upvoteP.innerHTML = xmlHttp.response["likes"]

            upvoteIcon.src = upvoteIcon.src.replace("_pressed_icon", "_icon")
            downvoteIcon.src = nextState
            downvoteIcon.classList.remove("spinner")
        }
    }
}