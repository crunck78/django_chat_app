let user = '{{request.user}}';

async function sendMessage() {
    try {
        let formData = new FormData();
        let token = '{{csrf_token}}';
        formData.append('textmessage', messageField.value);
        formData.append('csrfmiddlewaretoken', token);

        let response = await fetch('/chat/', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) // or check for response.status
            throw new Error(response.statusText);
        let jsonResponse = JSON.parse(await response.json());
        console.log(jsonResponse);
        let newMessage = jsonResponse.fields;
        //let newMessage = { created_at: getDateNowFormat(), author: user, text: messageField.value };
        messageContainer.insertAdjacentHTML("beforeend", getMessageHTML(newMessage));


    } catch (error) {
        console.error(error);
    }
}

function getDateNowFormat() {
    const monthNames = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];
    let now = new Date();
    return monthNames[now.getMonth()] + ". " + now.getDay() + ", " + now.getFullYear();
}

function getMessageHTML(message) {
    return `<!--html-->
        <div>
           <span>[${getDateNowFormat()}]</span>
            <span>{{ request.user }}</span>:
            <span><i>${message.text}</i></span>
        </div>`;
}