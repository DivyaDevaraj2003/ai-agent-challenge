// Generate or retrieve a persistent user_id for chat context per browser
let user_id = localStorage.getItem("user_id");
if (!user_id) {
    user_id = "user_" + Math.random().toString(36).substr(2, 9);
    localStorage.setItem("user_id", user_id);
}

// Set the default assistant
let currentAssistant = "faq";

// --- Helper function to get the correct messages container ---
function getMessagesContainer() {
    return document.querySelector('.chat-messages');
}

// --- Functions to save and load chat history ---
/**
 * Saves the current chat messages for a specific assistant to localStorage.
 * @param {string} assistantName - The name of the assistant (e.g., 'faq', 'wellness').
 */
function saveChatHistory(assistantName) {
    const messagesContainer = getMessagesContainer();
    if (messagesContainer) {
        localStorage.setItem(`chatHistory_${assistantName}`, messagesContainer.innerHTML);
    }
}

/**
 * Loads the chat history for a specific assistant from localStorage.
 * @param {string} assistantName - The name of the assistant (e.g., 'faq', 'wellness').
 */
function loadChatHistory(assistantName) {
    const messagesContainer = getMessagesContainer();
    const savedHistory = localStorage.getItem(`chatHistory_${assistantName}`);
    
    if (messagesContainer) {
        if (savedHistory) {
            // If history exists, load it
            messagesContainer.innerHTML = savedHistory;
        } else {
            // If no history, show the default welcome message
            messagesContainer.innerHTML = `<div class="bot-message">Hi 👋 I’m your ${assistantName} assistant. How can I help you today?</div>`;
        }
        scrollToBottom();
    }
}


// --- Event Listeners ---
// Assistant Toggle Buttons
document.getElementById("faq-btn").addEventListener("click", () => {
    saveChatHistory(currentAssistant);
    currentAssistant = "faq";
    document.getElementById("faq-btn").classList.add("active");
    document.getElementById("wellness-btn").classList.remove("active");
    document.getElementById("assistant-description").innerHTML = "<p>Get quick answers to common questions.</p>";
    loadChatHistory(currentAssistant);
});

document.getElementById("wellness-btn").addEventListener("click", () => {
    saveChatHistory(currentAssistant);
    currentAssistant = "wellness";
    document.getElementById("wellness-btn").classList.add("active");
    document.getElementById("faq-btn").classList.remove("active");
    document.getElementById("assistant-description").innerHTML = "<p>Ask personalized questions about your genes, wellness, fitness and more!</p>";
    loadChatHistory(currentAssistant);
});

// Dark Mode Toggle
document.getElementById('theme-toggle').addEventListener('click', function () {
    document.body.classList.toggle('dark-mode');
    this.textContent = document.body.classList.contains('dark-mode') ? '☀️' : '🌙';
});

// New Chat Button
document.getElementById('new-chat-btn').addEventListener('click', () => {
    if (confirm('Are you sure you want to start a new chat? This will clear the current conversation.')) {
        localStorage.removeItem(`chatHistory_${currentAssistant}`);
        loadChatHistory(currentAssistant);
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
    saveChatHistory(currentAssistant);
}

// Main Send Chat Logic
async function sendChat() {
    const inputBox = document.getElementById('user-input');
    const query = inputBox.value.trim();
    if (!query) return;

    displayMessage(query, true);
    inputBox.value = '';
    showTyping();

    const endpoint = currentAssistant === 'wellness' ? '/wellness/ask' : '/faq/ask';
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
// Load the chat history for the default agent when the page loads
document.addEventListener('DOMContentLoaded', () => {
    loadChatHistory(currentAssistant);
});