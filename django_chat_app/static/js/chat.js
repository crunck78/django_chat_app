const selected_chat = JSON.parse(document.getElementById('selected_chat').textContent);
console.log(selected_chat);

/**
 * Gets the event.target FormData, fetch a Post request with FormData as Payload, updates FrontEnd after response
 * @param {SubmitEvent} event
 * Possible issues :  //https://stackoverflow.com/questions/69050243/reportlab-in-django-application-error-forbidden-csrf-token-missing-or-incorre
 */
async function handleSubmit(event) {
    try {
        event.preventDefault();
        const formData = new FormData(event.target);
        formData.append('selected_chat', selected_chat.pk);
        formData.append('csrfmiddlewaretoken', csrfmiddlewaretoken);
        const response = await fetch('/message-post/', {
            method: 'POST',
            body: formData //this has to be type FormData!!!!
        });
        if (!response.ok) // or check for response.status
            throw new Error(response.statusText);
        const jsonResponse = JSON.parse(await response.json());
        const newMessage = jsonResponse.fields;
        console.log(newMessage);
        messageContainer.insertAdjacentHTML("beforeend", generateMessageHTML(newMessage));
        chatToBottom();
        clearInput();
    } catch (error) {
        console.error(error);
    }
}

/**
 * Generates a Front-End HTML Message View
 * @param {*} message - fields from a response serialized Message
 * @returns {string} - a message HTML format
 */
function generateMessageHTML(message) {
    return `<!--html-->
    <div id="message${message.pk}" class="mdl-card mdl-shadow--4dp ml-auto">
        <div class="mdl-card__title">
           <div>
            <p class="mdl-typography--text-capitalize">${user}</p>
            <h4 class="mdl-card__title-text"><b>${message.text}</b></h4>
           </div>
        </div>
        <div class="mdl-card__supporting-text">
            <span>[${message.created_at}]</span>
        </div>
    </div>`;
}

function chatToBottom() {
    let scrollingChat = setInterval(() => {
        if (reachedBottom(messageContainer)) {
            clearInterval(scrollingChat);
        }
        messageContainer.scrollTop += 10;
    });
}

function clearInput() {
    document.getElementById('messageField').value = "";
}

/**
 * Check wheatear the @param container is scrolled to the bottom
 * @param {HTMLElement} container
 * @returns {boolean} true | false
 */
function reachedBottom(container) {
    return Math.round(container.scrollTop) + 1 + //because scrollTop is a float we may never reached bottom
        container.clientHeight >=
        container.scrollHeight;
}

/**
 * @deprecated
 * @param {HTMLFormElement} form
 * @returns {object}
 */
function getFormData(form) {
    const data = new FormData(form);
    const value = Object.fromEntries(data.entries());
    return value;
}

/**
 * @deprecated
 * @returns {string} - a custom date format
 */
function getDateNowFormat() {
    const monthNames = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];
    const now = new Date();
    return monthNames[now.getMonth()] + ". " + now.getDay() + ", " + now.getFullYear();
}

async function handleDeleteMessage(messageId){
    console.log(messageId);
    try {
        const formData = new FormData();
        formData.append('selected_message_id', messageId);
        formData.append('csrfmiddlewaretoken', csrfmiddlewaretoken);
        const response = await fetch('/message-delete/', {
            method: 'POST',
            body: formData //this has to be type FormData!!!!
        });
        if (!response.ok) // or check for response.status
            throw new Error(response.statusText);
        delete_messageHTML(messageId);
    } catch (error) {
        console.error(error);
    }
}

function delete_messageHTML(messageId){
    document.getElementById(`message${messageId}`).remove();
}

window.onload = () => {
    chatToBottom();
    //chatListenToScroll();
}

// function chatListenToScroll() {
//     document.getElementById("messageContainer")
//         .addEventListener("scroll", () => {
//             document.getElementsByClassName("mdl-menu")
//                 .forEach( mdlMenu => updatePosition(mdlMenu) )
//         });
// }

// function updatePosition(mdlMenu){

// }