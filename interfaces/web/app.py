"""
Flask Web Application for JARVIS v2.0
Web dashboard with real-time chat interface
"""

from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from datetime import datetime
from config.settings import Settings
from core.brain import Brain
from core.memory import MemorySystem
from core.conversation import ConversationManager
from core.intent_detector import IntentDetector
from skills import *
from utils.logger import setup_logger

logger = setup_logger(__name__)


def create_app(settings: Settings) -> Flask:
    """
    Create and configure Flask app
    
    Args:
        settings: Application settings
        
    Returns:
        Configured Flask app
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = settings.FLASK_SECRET_KEY
    app.config['DEBUG'] = settings.DEBUG_MODE

    # Enable CORS
    CORS(app)

    # Initialize SocketIO
    socketio = SocketIO(app, cors_allowed_origins="*")

    # Initialize core components
    brain = Brain(settings)
    memory = MemorySystem(settings)
    intent_detector = IntentDetector()

    # Store conversations per session
    conversations = {}

    @app.route('/')
    def index():
        """Render main page"""
        return render_template('index.html')

    @app.route('/api/health')
    def health():
        """Health check endpoint"""
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0"
        })

    @app.route('/api/stats')
    def stats():
        """Get system statistics"""
        try:
            memory_stats = memory.get_memory_stats()
            return jsonify({
                "success": True,
                "data": {
                    "memory": memory_stats,
                    "active_sessions": len(conversations)
                }
            })
        except Exception as e:
            logger.error(f"Stats error: {e}")
            return jsonify({"success": False, "error": str(e)}), 500

    @socketio.on('connect')
    def handle_connect():
        """Handle client connection"""
        session_id = request.sid
        conversations[session_id] = ConversationManager(settings)
        logger.info(f"Client connected: {session_id}")
        emit('connected', {'message': 'Connected to JARVIS'})

    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection"""
        session_id = request.sid
        if session_id in conversations:
            del conversations[session_id]
        logger.info(f"Client disconnected: {session_id}")

    @socketio.on('message')
    def handle_message(data):
        """Handle incoming message"""
        try:
            session_id = request.sid
            user_message = data.get('message', '')

            if not user_message:
                emit('error', {'error': 'Empty message'})
                return

            # Get or create conversation
            if session_id not in conversations:
                conversations[session_id] = ConversationManager(settings)

            conversation = conversations[session_id]

            # Add user message
            conversation.add_message('user', user_message)

            # Detect intent
            intent_data = intent_detector.detect_intent(user_message)

            # Get AI response
            messages = conversation.get_context_messages()
            response = brain.generate_response(messages)

            # Add assistant response
            conversation.add_message('assistant', response)

            # Store in memory
            memory.store_conversation(user_message, response)

            # Send response
            emit('response', {
                'message': response,
                'timestamp': datetime.now().isoformat(),
                'intent': intent_data['primary_intent']
            })

        except Exception as e:
            logger.error(f"Message handling error: {e}")
            emit('error', {'error': str(e)})

    @socketio.on('clear_conversation')
    def handle_clear():
        """Clear conversation history"""
        try:
            session_id = request.sid
            if session_id in conversations:
                conversations[session_id].clear_conversation()
            emit('conversation_cleared', {'message': 'Conversation cleared'})
        except Exception as e:
            logger.error(f"Clear conversation error: {e}")
            emit('error', {'error': str(e)})

    # Attach socketio to app
    app.socketio = socketio

    logger.info("Flask app created")
    return app
