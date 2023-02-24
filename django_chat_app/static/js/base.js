/**
 * Handles an input field value as for querying all users
 * @param {SubmitEvent} event
 */
async function handleSearch(event) {
    try {
        event.preventDefault();
        const formData = new FormData(event.target);
        const response = await fetch('/search-users/', {
            method: 'POST',
            body: formData //this has to be type FormData!!!!
        });
        if (response.status == 400 || !response.ok) // check for bad request
            throw new Error(await response.text()); // in this case backend send a Bad Request Response as a text

        const searchResult = JSON.parse(await response.json());
        if (searchResult.length > 0) {
            searchUsers.value = ""
            // searchResultsContainer.innerHTML = "";
            searchResult.forEach((sR) => {
                searchResultsContainer
                    .insertAdjacentHTML(
                        "beforeend",
                        generateUserHTML(sR)
                    );
            })
        } else {
            searchResultsContainer.innerHTML = `<h2>Could not find anybody with "${searchUsers.value}" as search Value.</h2>`;
        }

    } catch (error) {
        //errorLog.innerHTML = error;
        console.error(error);
    }
}


function generateUserHTML(searchResult) {
    const user = searchResult.fields;
    return `<!--html-->
        <div onclick="handleChoice(${searchResult.pk}, this)" class="mdl-list__item mdl-card mdl-card--border mdl-shadow--16dp">
            <span class="mdl-list__item-primary-content">
                <i class="material-icons mdl-list__item-avatar">person</i>
                <span class="mdl-typography--text-capitalize">${user.username || user.firstname + ' ' + user.lastname || user.email || user}</span>
            </span>
        </div>`;
}


/**
 *
 * @param {number} uuid - User Uniq Id
 * @param {HTMLElement} - User Frontend Choice Container
 */
async function handleChoice(uuid, container) {
    try {
        const formData = new FormData();
        formData.append('csrfmiddlewaretoken', baseToken);
        formData.append('userId', uuid);
        const response = await fetch('/request-chat/', {
            method: 'POST',
            body: formData
        });
        if (response.status == 400 || !response.ok) // check for bad request
            throw new Error(await response.text()); // in this case backend send a Bad Request Response as a text
        container.remove();
        window.location.replace(response.url);

    } catch (error) {
        console.error(error);
    }
}