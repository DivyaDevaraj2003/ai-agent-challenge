// Generate or retrieve a persistent user_id for chat context per browser
let user_id = localStorage.getItem("user_id");
if (!user_id) {
    user_id = "user_" + Math.random().toString(36).substr(2, 9);
    localStorage.setItem("user_id", user_id);
}

// --- Helper function to get the correct messages container ---
function getMessagesContainer() {
    return document.querySelector('.chat-messages');
}

// --- SIMPLIFIED: Functions to save and load a single chat history ---
function saveChatHistory() {
    const messagesContainer = getMessagesContainer();
    if (messagesContainer) {
        localStorage.setItem('chatHistory', messagesContainer.innerHTML);
    }
}

function loadChatHistory() {
    const messagesContainer = getMessagesContainer();
    const savedHistory = localStorage.getItem('chatHistory');
    
    if (messagesContainer) {
        if (savedHistory) {
            messagesContainer.innerHTML = savedHistory;
        } else {
            // A single, unified welcome message
            messagesContainer.innerHTML = `<div class="bot-message">Hi 👋 I’m your Nuegenomics assistant. How can I help you today?</div>`;
        }
        scrollToBottom();
    }
}


// --- Event Listeners ---

// DELETED: The toggle button listeners are no longer needed.

// Dark Mode Toggle
document.getElementById('theme-toggle').addEventListener('click', function () {
    document.body.classList.toggle('dark-mode');
    this.textContent = document.body.classList.contains('dark-mode') ? '☀️' : '🌙';
});

// New Chat Button
document.getElementById('new-chat-btn').addEventListener('click', () => {
    if (confirm('Are you sure you want to start a new chat? This will clear the current conversation.')) {
        localStorage.removeItem('chatHistory');
        loadChatHistory();
    }
});

// Chat Input & Send
document.getElementById('send-button').addEventListener('click', sendChat);
document.getElementById('user-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        sendChat();
    }
});


// --- Core Chat Functions ---

// Show Typing Animation
function showTyping() {
    const messages = getMessagesContainer();
    if (!messages) return;
    const typing = document.createElement('div');
    typing.className = 'bot-message typing';
    typing.id = 'typing';
    typing.textContent = 'Bot is typing...';
    messages.appendChild(typing);
    scrollToBottom();
}

// Remove Typing Animation
function removeTyping() {
    const typing = document.getElementById('typing');
    if (typing) typing.remove();
}

// Scroll to bottom utility
function scrollToBottom() {
    const messages = getMessagesContainer();
    if (messages) messages.scrollTop = messages.scrollHeight;
}

// Display a message and save history
function displayMessage(message, isUser = false) {
    const messages = getMessagesContainer();
    if (!messages) return;

    const bubble = document.createElement("div");
    bubble.className = isUser ? "user-message" : "bot-message";
    bubble.innerHTML = message.replace(/\n/g, '<br>');
    messages.appendChild(bubble);
    
    scrollToBottom();
    saveChatHistory();
}

// Main Send Chat Logic
async function sendChat() {
    const inputBox = document.getElementById('user-input');
    const query = inputBox.value.trim();
    if (!query) return;

    displayMessage(query, true);
    inputBox.value = '';
    showTyping();

    // UPDATED: Always use the single '/ask' endpoint
    const endpoint = '/ask';
    const payload = { query: query, user_id: user_id };

    try {
        const res = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        removeTyping();
        displayMessage(data.answer || data.response || 'Sorry, no answer found.', false);
    } catch (err) {
        removeTyping();
        displayMessage('Oops! Something went wrong.', false);
        console.error(err);
    }
}

// --- Initialize App ---
document.addEventListener('DOMContentLoaded', () => {
    loadChatHistory();
});