/**
 * Handles an input field value as for querying all users
 * @param {*} event 
 */
function handleSearch(event) {
    try {
        event.preventDefault();
        const formData = new FormData(event.target);
        const response = await fetch('/chat/', {
            method: 'POST',
            body: formData //this has to be type FormData!!!!
        });
        if (response.status == 400 || !response.ok) // check for bad request
            throw new Error(await response.text()); // in this case backend send a Bad Request Response as a text
        const jsonResponse = JSON.parse(await response.json());
        console.log(jsonResponse);
    } catch (error) {
        //errorLog.innerHTML = error;
        console.error(error);
    }
}