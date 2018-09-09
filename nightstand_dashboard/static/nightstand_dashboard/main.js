// event handler for likes
$(".like-button").click(event => {
    $.ajax(`http://127.0.0.1:8000/like/${event.target.id.split("-")[1]}`, {
        "method": 'GET',
        "data": {},
        "credentials": "include",
        "headers": {
            "X-CSRFToken": document.cookie.split("=")[1],
            "Content-Type": "application/json",
        }
    })
    if (event.target.value == "Like") {
        $(`#${event.target.id}`).val("Unlike")
        let likeCount = parseInt($(`#like-count-${event.target.id.split("-")[1]}`).text());
        likeCount ++;
        $(`#like-count-${event.target.id.split("-")[1]}`).text( likeCount.toString())
    } else {
        $(`#${event.target.id}`).val("Like")
        let likeCount = parseInt($(`#like-count-${event.target.id.split("-")[1]}`).text());
        likeCount --;
        $(`#like-count-${event.target.id.split("-")[1]}`).text(likeCount.toString())
    }      
})

// event handler for completing chapters
$(".chapter-complete").click(event => {
    $.ajax(`http://127.0.0.1:8000/complete/${event.target.id.split("-")[1]}`, {
        "method": 'GET',
        "data": {},
        "credentials": "include",
        "headers": {
            "X-CSRFToken": document.cookie.split("=")[1],
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
    })
    if (event.target.id.split("-")[2] === "dashboard") {
        $(`#chapter-card-${event.target.id.split("-")[1]}`).remove()
    } else {
        $(`#${event.target.id}`).remove()
        $(`#chapter-card-${event.target.id.split("-")[1]}`).removeClass("overdue").addClass("completed") 
    }
})

// event handler to update duedate