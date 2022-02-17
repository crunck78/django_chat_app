const userId = JSON.parse(document.getElementById('user_id').textContent);

/**
 * Gets the event.target FormData, fetch a Post request with FormData as Payload, updates FrontEnd after response
 * @param {SubmitEvent} event 
 * Possible issues :  //https://stackoverflow.com/questions/69050243/reportlab-in-django-application-error-forbidden-csrf-token-missing-or-incorre
 */
async function handleSubmit(event) {
    try {
        event.preventDefault(); // stop default submitting
        const formData = getFormData(event.target);
        const response = await fetch('/chat/', {
            method: 'POST',
            body: formData
        });
        if (!response.ok) // or check for response.status
            throw new Error(response.statusText);
        const jsonResponse = JSON.parse(await response.json());
        const newMessage = jsonResponse.fields;
        messageContainer.insertAdjacentHTML("beforeend", generateMessageHTML(newMessage));
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
        <div>
           <span>[${message.created_at}]</span>
            <span>${message.author}</span>:
            <span><i>${message.text}</i></span>
        </div>`;
}

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