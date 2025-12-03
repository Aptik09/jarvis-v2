// JARVIS v2.0 Web Dashboard JavaScript

// Initialize Socket.IO
const socket = io();

// DOM Elements
const chatMessages = document.getElementById('chat-messages');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const clearButton = document.getElementById('clear-button');
const statusIndicator = document.getElementById('status');
const statusText = document.getElementById('status-text');
const quickActions = document.querySelectorAll('.quick-action');
const statsDiv = document.getElementById('stats');

// Connection handlers
socket.on('connect', () => {
    console.log('Connected to JARVIS');
    statusIndicator.classList.add('connected');
    statusText.textContent = 'Connected';
    addSystemMessage('Connected to JARVIS');
});

socket.on('disconnect', () => {
    console.log('Disconnected from JARVIS');
    statusIndicator.classList.remove('connected');
    statusText.textContent = 'Disconnected';
    addSystemMessage('Disconnected from JARVIS');
});

socket.on('connected', (data) => {
    console.log(data.message);
});

// Message handlers
socket.on('response', (data) => {
    addMessage('assistant', data.message, data.timestamp);
    messageInput.disabled = false;
    sendButton.disabled = false;
});

socket.on('error', (data) => {
    addSystemMessage(`Error: ${data.error}`, 'error');
    messageInput.disabled = false;
    sendButton.disabled = false;
});

socket.on('conversation_cleared', (data) => {
    clearMessages();
    addSystemMessage(data.message);
});

// Send message
function sendMessage() {
    const message = messageInput.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addMessage('user', message);
    
    // Send to server
    socket.emit('message', { message: message });
    
    // Clear input and disable while processing
    messageInput.value = '';
    messageInput.disabled = true;
    sendButton.disabled = true;
    
    // Show typing indicator
    addTypingIndicator();
}

// Add message to chat
function addMessage(role, content, timestamp = null) {
    // Remove typing indicator if exists
    removeTypingIndicator();
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;
    
    messageDiv.appendChild(contentDiv);
    
    if (timestamp) {
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = new Date(timestamp).toLocaleTimeString();
        messageDiv.appendChild(timeDiv);
    }
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Add system message
function addSystemMessage(content, type = 'info') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `system-message ${type}`;
    messageDiv.textContent = content;
    messageDiv.style.textAlign = 'center';
    messageDiv.style.padding = '10px';
    messageDiv.style.margin = '10px 0';
    messageDiv.style.opacity = '0.7';
    messageDiv.style.fontSize = '0.9rem';
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Add typing indicator
function addTypingIndicator() {
    const indicator = document.createElement('div');
    indicator.id = 'typing-indicator';
    indicator.className = 'message assistant';
    indicator.innerHTML = '<div class="message-content">JARVIS is thinking...</div>';
    chatMessages.appendChild(indicator);
    scrollToBottom();
}

// Remove typing indicator
function removeTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
        indicator.remove();
    }
}

// Clear messages
function clearMessages() {
    chatMessages.innerHTML = '';
}

// Scroll to bottom
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Load statistics
function loadStats() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const stats = data.data;
                statsDiv.innerHTML = `
                    <p><strong>Total Memories:</strong> ${stats.memory.total_memories}</p>
                    <p><strong>Active Sessions:</strong> ${stats.active_sessions}</p>
                `;
            }
        })
        .catch(error => {
            console.error('Error loading stats:', error);
            statsDiv.innerHTML = '<p>Error loading stats</p>';
        });
}

// Event listeners
sendButton.addEventListener('click', sendMessage);

messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

clearButton.addEventListener('click', () => {
    if (confirm('Clear conversation history?')) {
        socket.emit('clear_conversation');
    }
});

// Quick actions
quickActions.forEach(button => {
    button.addEventListener('click', () => {
        const action = button.dataset.action;
        let message = '';
        
        switch(action) {
            case 'search':
                message = 'Search for ';
                break;
            case 'weather':
                message = 'What\'s the weather like?';
                break;
            case 'news':
                message = 'Show me the latest news';
                break;
            case 'calculate':
                message = 'Calculate ';
                break;
            case 'remember':
                message = 'Remember that ';
                break;
        }
        
        messageInput.value = message;
        messageInput.focus();
    });
});

// Load stats on page load
loadStats();

// Refresh stats every 30 seconds
setInterval(loadStats, 30000);

// Focus input on load
messageInput.focus();
