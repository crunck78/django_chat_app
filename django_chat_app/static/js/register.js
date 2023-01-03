/**
 * Gets the event.target FormData, fetch a Post request with FormData as Payload, updates FrontEnd after response
 * @param {SubmitEvent} event
 * Possible issues :  //https://stackoverflow.com/questions/69050243/reportlab-in-django-application-error-forbidden-csrf-token-missing-or-incorre
 */
 async function handleSubmit(event) {
    try {
        event.preventDefault();
        const formData = new FormData(event.target);
        if(formData['password'] !== formData['check_password'])
            throw new Error("Password does not Match!")
        const response = await fetch('/create-account/', {
            method: 'POST',
            body: formData //this has to be type FormData!!!!
        });
        if (response.status == 400 || !response.ok) // check for bad request
            throw new Error(await response.text()); // in this case backend send a Bad Request Response as a text
        // const jsonResponse = JSON.parse(await response.json());
        // console.log(jsonResponse);
        window.location.replace(response.url);
    } catch (error) {
        errorLog.innerHTML = error;
        console.error(error);
    }
}