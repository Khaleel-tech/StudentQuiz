(function () {
  const sendBtn = document.getElementById('sendBtn');
  const input = document.getElementById('chatInput');
  const chatBox = document.getElementById('chatBox');
  if (!sendBtn || !input || !chatBox) return;

  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

  function addMessage(sender, message, cls) {
    const item = document.createElement('div');
    item.className = `chat-message ${cls}`;
    item.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatBox.appendChild(item);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  async function sendMessage() {
    const message = input.value.trim();
    if (!message) return;
    addMessage('You', message, 'user-message');
    input.value = '';

    const response = await fetch('/api/chatbot/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken') || ''
      },
      body: JSON.stringify({ message })
    });

    const data = await response.json();
    addMessage('Bot', data.response, 'bot-message');
  }

  sendBtn.addEventListener('click', sendMessage);
  input.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      sendMessage();
    }
  });
})();
