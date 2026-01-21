document.addEventListener('DOMContentLoaded', () => {
    const chatContainer = document.getElementById('chat-container');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const showSourcesCk = document.getElementById('show-sources');
    const roleSelect = document.getElementById('role-select');
    const langSelect = document.getElementById('lang-select');

    function appendMessage(text, isUser, sources = []) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', isUser ? 'user-message' : 'bot-message');

        const bubble = document.createElement('div');
        bubble.classList.add('bubble');
        bubble.textContent = text;

        messageDiv.appendChild(bubble);

        if (!isUser && sources.length > 0) {
            const sourcesDiv = document.createElement('div');
            sourcesDiv.classList.add('sources');
            sourcesDiv.textContent = 'Sources: ' + sources.join(', ');
            messageDiv.appendChild(sourcesDiv);
        }

        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    async function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;

        // UI Updates
        appendMessage(text, true);
        userInput.value = '';
        userInput.setAttribute('disabled', 'true');
        sendBtn.setAttribute('disabled', 'true');

        // Prepare Payload
        const payload = {
            question: text,
            show_sources: showSourcesCk.checked,
            role: roleSelect.value,
            language: langSelect.value
        };

        try {
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            appendMessage(data.answer, false, data.sources);

        } catch (error) {
            console.error('Error:', error);
            appendMessage("Sorry, something went wrong. Please check your connection or API key.", false);
        } finally {
            userInput.removeAttribute('disabled');
            sendBtn.removeAttribute('disabled');
            userInput.focus();
        }
    }

    sendBtn.addEventListener('click', sendMessage);

    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Initial focus
    userInput.focus();
});
