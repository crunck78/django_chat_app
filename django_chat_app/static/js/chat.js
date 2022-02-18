// const userId = JSON.parse(document.getElementById('user_id').textContent);


setTimeout(() => {
    chatToBottom();
}, 300);

/**
 * Gets the event.target FormData, fetch a Post request with FormData as Payload, updates FrontEnd after response
 * @param {SubmitEvent} event 
 * Possible issues :  //https://stackoverflow.com/questions/69050243/reportlab-in-django-application-error-forbidden-csrf-token-missing-or-incorre
 */
async function handleSubmit(event) {
    try {
        event.preventDefault();
        const formData = new FormData(event.target);
        const response = await fetch('/chat/', {
            method: 'POST',
            body: formData //this has to be type FormData!!!!
        });
        if (!response.ok) // or check for response.status
            throw new Error(response.statusText);
        const jsonResponse = JSON.parse(await response.json());
        const newMessage = jsonResponse.fields;
        messageContainer.insertAdjacentHTML("beforeend", generateMessageHTML(newMessage));
        chatToBottom();
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
    <div class="mdl-card mdl-shadow--4dp">
        <div class="mdl-card__title">
           <div>
            <p>${message.author.first_name | message.author.username | message.author.email | message.author}</p>
            <h4 class="mdl-card__title-text"><b>${message.text}</b></h4>
           </div>
        </div>
        <div class="mdl-card__supporting-text">
            <span>[${message.created_at}]</span>
        </div>
    </div>`;
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

function chatToBottom() {
    let scrollingChat = setInterval(() => {
        if (messageContainer.scrollTop == messageContainer.scrollHeight) {
            clearInterval(scrollingChat);
        }
        messageContainer.scrollTop += 10;
    });
}