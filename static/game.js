let pollInterval = null;

function pollForUpdate(gid) {
    if (pollInterval) return; // prevent multiple intervals

    pollInterval = setInterval(() => {
        fetch(`/game/${gid}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error("Failed to fetch game state");
                }
                return response.text();
            })
            .then(html => {
                document.body.innerHTML = html;
            })
            .catch(err => {
                console.error("Polling error:", err);
                clearInterval(pollInterval);
                pollInterval = null;
            });
    }, 2000);
}

