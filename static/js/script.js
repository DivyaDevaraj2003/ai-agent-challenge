let currentAssistant = "faq";

// ----- Assistant Toggle Buttons -----
document.getElementById("faq-btn").addEventListener("click", () => {
  currentAssistant = "faq";
  document.getElementById("faq-btn").classList.add("active");
  document.getElementById("wellness-btn").classList.remove("active");
  document.getElementById("assistant-description").innerHTML = "<p>Ask about our services, pricing, or process.</p>";
  resetChat();
  let select = document.getElementById("assistant-choice");
  if (select) select.value = "faq";
});
document.getElementById("wellness-btn").addEventListener("click", () => {
  currentAssistant = "wellness";
  document.getElementById("wellness-btn").classList.add("active");
  document.getElementById("faq-btn").classList.remove("active");
  document.getElementById("assistant-description").innerHTML = "<p>Ask personalized questions about your genes, wellness, fitness and more!</p>";
  resetChat();
  let select = document.getElementById("assistant-choice");
  if (select) select.value = "genetic";
});

// Optionally: Sync when dropdown changes
const select = document.getElementById("assistant-choice");
if (select) {
  select.addEventListener("change", function () {
    if (this.value === "faq") {
      document.getElementById("faq-btn").click();
    } else if (this.value === "genetic") {
      document.getElementById("wellness-btn").click();
    }
  });
}

// ----- Dark Mode Toggle -----
document.getElementById('theme-toggle').addEventListener('click', function () {
  document.body.classList.toggle('dark-mode');
  this.textContent = document.body.classList.contains('dark-mode') ? '☀️' : '🌙';
});

// ----- Chat Input & Send -----
document.getElementById('send-button').addEventListener('click', sendChat);
document.getElementById('user-input').addEventListener('keypress', function (e) {
  if (e.key === 'Enter') {
    e.preventDefault();
    sendChat();
  }
});

function resetChat() {
  const chatBox = document.getElementById('chat-box');
  if (chatBox) chatBox.innerHTML = `
    <div class="bot-message">Hi 👋 I’m your Nuegenomics assistant. How can I help you today?</div>
  `;
}

// Show Typing Animation
function showTyping() {
  const chatBox = document.getElementById('chat-box');
  const typing = document.createElement('div');
  typing.className = 'bot-message typing';
  typing.id = 'typing';
  typing.textContent = 'Bot is typing...';
  chatBox.appendChild(typing);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Remove Typing Animation
function removeTyping() {
  const typing = document.getElementById('typing');
  if (typing) typing.remove();
}

// ----- Message Rendering with Newlines Preserved -----
function displayMessage(message, isUser = false) {
  // Format double \n\n as <br><br> and single \n as <br>
  const formattedMessage = message
    .replace(/\n\n/g, '<br><br>')
    .replace(/\n/g, '<br>');
  const chatBox = document.getElementById('chat-box');
  const bubble = document.createElement("div");
  bubble.className = isUser ? "user-message" : "bot-message";
  bubble.innerHTML = formattedMessage;
  chatBox.appendChild(bubble);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// ----- Main Send Chat Logic -----
async function sendChat() {
  const inputBox = document.getElementById('user-input');
  const query = inputBox.value.trim();
  if (!query) return;

  displayMessage(query, true); // User message
  inputBox.value = '';
  showTyping();

  // Determine endpoint based on assistant mode
  let assistantType = currentAssistant;
  if (select && select.value) {
    assistantType = (select.value === "faq") ? "faq" : "wellness";
  }

  let endpoint = '/faq/ask';
  let payload = { query: query };
  if (assistantType === 'wellness') {
    endpoint = '/wellness/ask';
    payload.session_id = "user123";
  }

  try {
    const res = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    removeTyping();
    displayMessage(data.answer || data.response || 'Sorry, no answer found.', false); // Bot message
  } catch (err) {
    removeTyping();
    displayMessage('Oops! Something went wrong.', false);
    console.error(err);
  }
}

// ----- Initialize the chat with welcome message -----
resetChat();
