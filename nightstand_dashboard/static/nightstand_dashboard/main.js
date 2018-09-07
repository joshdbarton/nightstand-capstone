



// event handler for likes
$(".like-button").onclick(event => {
    fetch(`/like/${event.target.id.split("-")[1]}`, {
        "method": 'GET',
        "body": {},
        "headers": {
            "X-CSRFToken": browser.cookies.get('csrftoken'),
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
    })
    event.target.value == "Like" ? $(`#${event.target.id}`).val("Unlike"):$(`#${event.target.id}`).val("Like")
})
// event handler to update duedate


// event handler for completing chapters
$(".chapter-complete").onclick(event => {
    fetch(`/complete/${event.target.id.split("-")[1]}`, {
        "method": 'GET',
        "body": {},
        "headers": {
            "X-CSRFToken": browser.cookies.get('csrftoken'),
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
    })
    if ($(`#${event.target.id.split("-")[2]}`) === "dashboard") {
        $(`#chapter-card-${event.target.id.split("-")[1]}`).remove()
    } else {
        $(`#${event.target.id}`).remove()
        // change class to reflect completed on card. 
    }
})
