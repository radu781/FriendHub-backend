let copyButtons = document.querySelectorAll(".copy-clipboard")
for (let copyButton of copyButtons) {
    copyButton.addEventListener("click", (event) => {
        let whole = event.target.parentElement.childNodes[1]
        let endpoint = whole.childNodes[1].innerHTML
        let params = whole.childNodes[2].data || ""
        navigator.clipboard.writeText(`https://friendhub.social${endpoint}${params}`)
    })
}