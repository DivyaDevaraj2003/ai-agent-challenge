
// Generate or retrieve a persistent user_id for chat context per browser
let user_id = localStorage.getItem("user_id");
if (!user_id) {
  user_id = "user_" + Math.random().toString(36).substr(2, 9);
  localStorage.setItem("user_id", user_id);
}

let currentAssistant = "faq";

// --- Helper function to get the correct messages container ---
function getMessagesContainer() {
  // This is the ONLY element that should hold messages.
  return document.querySelector('.chat-messages');
}

// Assistant Toggle Buttons
document.getElementById("faq-btn").addEventListener("click", () => {
  currentAssistant = "faq";
  document.getElementById("faq-btn").classList.add("active");
  document.getElementById("wellness-btn").classList.remove("active");
  document.getElementById("assistant-description").innerHTML = "<p>Get quick answers to common questions..</p>";
  resetChat();
});
document.getElementById("wellness-btn").addEventListener("click", () => {
  currentAssistant = "wellness";
  document.getElementById("wellness-btn").classList.add("active");
  document.getElementById("faq-btn").classList.remove("active");
  document.getElementById("assistant-description").innerHTML = "<p>Ask personalized questions about your genes, wellness, fitness and more!</p>";
  resetChat();
});

// Dark Mode Toggle
document.getElementById('theme-toggle').addEventListener('click', function () {
  document.body.classList.toggle('dark-mode');
  this.textContent = document.body.classList.contains('dark-mode') ? '☀️' : '🌙';
});

// Chat Input & Send
document.getElementById('send-button').addEventListener('click', sendChat);
document.getElementById('user-input').addEventListener('keypress', function (e) {
  if (e.key === 'Enter') {
    e.preventDefault();
    sendChat();
  }
});

// Resets chat box/messages
function resetChat() {
  const messages = getMessagesContainer();
  if (messages) {
    messages.innerHTML = `<div class="bot-message">Hi 👋 I’m your Nuegenomics assistant. How can I help you today?</div>`;
    scrollToBottom();
  }
}

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

// Display a message (user or bot)
function displayMessage(message, isUser = false) {
  const messages = getMessagesContainer();
  if (!messages) return;

  const bubble = document.createElement("div");
  bubble.className = isUser ? "user-message" : "bot-message";
  bubble.textContent = message; // Use textContent for security unless you need HTML
  messages.appendChild(bubble);
  scrollToBottom();
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
    // Use textContent for the response as well for better security
    displayMessage(data.answer || data.response || 'Sorry, no answer found.', false);
  } catch (err) {
    removeTyping();
    displayMessage('Oops! Something went wrong.', false);
    console.error(err);
  }
}

// Initialize the chat with welcome message
resetChat();