function initItemList() {
    u('button.item-info-button').on('click', function(e) {
        toggleInfoBlock(this);
    });
    u('button.item-buy-button').on('click', function(e) {
        addClaim(this);
    });
    u('button.item-remove-button').on('click', function(e) {
        removeClaim(this);
    });
}

function toggleInfoBlock(e) {
    item_id = u(e).parent().attr("x-item-id");
    toggle_div = "#item_" + item_id + "_detail";

    if (u(toggle_div).hasClass("hidden")) {
        u(toggle_div).removeClass("hidden");
    } else {
        u(toggle_div).addClass("hidden");
    }
}

async function addClaim(e) {
    item_id = u(e).parent().attr("x-item-id");

    await postData("/claim/add", { 'item_id': item_id });
    window.location.reload();
}

async function removeClaim(e) {
    item_id = u(e).parent().attr("x-item-id");

    await postData("/claim/remove", { 'item_id': item_id });
    window.location.reload();
}

async function postData(url = '', data = {}) {
    response = await fetch(url, {
        method: 'POST',
        cache: 'no-cache',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    return response.json(); // parses JSON response into native JavaScript objects
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}