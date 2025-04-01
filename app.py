import os
import logging
from flask import Flask, render_template, request, jsonify, session, flash, redirect, url_for

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")

# Import routes after app initialization to avoid circular imports
from services.legal_analysis import analyze_legal_text

@app.route('/')
def index():
    """Render the main page with the input form."""
    return render_template('index.html')

@app.route('/about')
def about():
    """Render the about page with information about the app."""
    return render_template('about.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Handle legal text analysis requests."""
    try:
        legal_text = request.form.get('legal_text', '')
        audience = request.form.get('audience', 'layperson')
        
        if not legal_text:
            flash('Please enter some legal text to analyze.', 'warning')
            return redirect(url_for('index'))
        
        # Call the OpenAI API to analyze the text
        analysis_result = analyze_legal_text(legal_text, audience)
        
        return render_template('index.html', 
                               legal_text=legal_text,
                               audience=audience,
                               analysis=analysis_result)
        
    except Exception as e:
        logging.error(f"Error analyzing text: {str(e)}")
        flash('An error occurred while analyzing the text. Please try again.', 'danger')
        return render_template('index.html', legal_text=request.form.get('legal_text', ''))

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return render_template('index.html'), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors."""
    logging.error(f"Server error: {str(e)}")
    return render_template('index.html'), 500
