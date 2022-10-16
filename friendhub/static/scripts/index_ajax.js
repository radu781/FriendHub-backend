function sendVote(id, voteType) {
    let xmlHttp = new XMLHttpRequest();
    xmlHttp.open("PUT", `/api/post/${id}?${voteType}`, true);
    xmlHttp.responseType = "json"
    xmlHttp.send();
    xmlHttp.onload = () => console.log("Done", xmlHttp.status)
}

function getNewVoteText(id) {
    let xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", `/api/post/${id}`, true);
    xmlHttp.send();
    console.log("-------------");
    console.log(xmlHttp.responseXML);
    return xmlHttp.responseText
}

function upvotePost(postId) {
    let xmlHttp = new XMLHttpRequest();
    xmlHttp.open("PUT", `/api/post/${postId}?upvote`, true);
    xmlHttp.responseType = "json"
    xmlHttp.send();
    xmlHttp.onload = function() {
        let xmlHttp = new XMLHttpRequest();
        xmlHttp.open("GET", `/api/post/${postId}`, true);
        xmlHttp.responseType = "json"
        xmlHttp.send();
        xmlHttp.onload = function() {
            let downvoteP = document.querySelector(`#downvote-${postId}`)
            downvoteP.innerHTML = xmlHttp.response["dislikes"]
            let upvoteP = document.querySelector(`#upvote-${postId}`)
            upvoteP.innerHTML = xmlHttp.response["likes"]
        }
    }
}

function downvotePost(postId) {
    let xmlHttp = new XMLHttpRequest();
    xmlHttp.open("PUT", `/api/post/${postId}?downvote`, true);
    xmlHttp.responseType = "json"
    xmlHttp.send();
    xmlHttp.onload = function() {
        let xmlHttp = new XMLHttpRequest();
        xmlHttp.open("GET", `/api/post/${postId}`, true);
        xmlHttp.responseType = "json"
        xmlHttp.send();
        xmlHttp.onload = function() {
            let downvoteP = document.querySelector(`#downvote-${postId}`)
            downvoteP.innerHTML = xmlHttp.response["dislikes"]
            let upvoteP = document.querySelector(`#upvote-${postId}`)
            upvoteP.innerHTML = xmlHttp.response["likes"]
        }
    }
}