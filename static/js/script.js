// Toggle Dark Mode
document.getElementById('theme-toggle').addEventListener('click', function () {
  document.body.classList.toggle('dark-mode');
  this.textContent = document.body.classList.contains('dark-mode') ? '☀️' : '🌙';
});

// Send Message and Get Bot Response
document.getElementById('send-button').addEventListener('click', function () {
  const inputBox = document.getElementById('user-input');
  const query = inputBox.value.trim();
  if (!query) return;

  appendMessage('You', query);
  inputBox.value = '';

  showTyping();

  fetch('/faq/ask', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ query })  // ✅ FIXED: match Python code expecting "query"
  })
    .then(res => res.json())
    .then(data => {
      removeTyping();
      appendMessage('Bot', data.answer || 'Sorry, no answer found.');
    })
    .catch(err => {
      removeTyping();
      appendMessage('Bot', 'Oops! Something went wrong.');
      console.error(err);
    });
});

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

// Remove Typing
function removeTyping() {
  const typing = document.getElementById('typing');
  if (typing) typing.remove();
}

// Append Chat Message
function appendMessage(sender, text) {
  const chatBox = document.getElementById('chat-box');
  const msg = document.createElement('div');
  msg.className = sender === 'You' ? 'user-message' : 'bot-message';

  let i = 0;
  const interval = setInterval(() => {
    if (i < text.length) {
      msg.textContent += text[i++];
    } else {
      clearInterval(interval);
    }
  }, 20);

  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Allow Enter to Send
document.getElementById('user-input').addEventListener('keypress', function (e) {
  if (e.key === 'Enter') {
    e.preventDefault();
    document.getElementById('send-button').click();
  }
});
