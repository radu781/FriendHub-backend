function upvotePost(postId) {
    let xmlHttp = new XMLHttpRequest()
    xmlHttp.open("PUT", `/api/post/${postId}?upvote`, true)
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

            let likeIcon = upvoteP.parentNode.childNodes[1].firstElementChild
            likeIcon.src = likeIcon.src.replace("_icon", "_pressed_icon")
            let dislikeIcon = downvoteP.parentNode.childNodes[7].firstElementChild
            dislikeIcon.src = dislikeIcon.src.replace("_pressed_icon", "_icon")
        }
    }
}

function downvotePost(postId) {
    let xmlHttp = new XMLHttpRequest()
    xmlHttp.open("PUT", `/api/post/${postId}?downvote`, true)
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

            let likeIcon = upvoteP.parentNode.childNodes[1].firstElementChild
            likeIcon.src = likeIcon.src.replace("_pressed_icon", "_icon")
            let dislikeIcon = downvoteP.parentNode.childNodes[7].firstElementChild
            dislikeIcon.src = dislikeIcon.src.replace("_icon", "_pressed_icon")
        }
    }
}