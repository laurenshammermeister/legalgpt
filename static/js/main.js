document.addEventListener('DOMContentLoaded', function() {
    // Get the form and analyze button
    const legalForm = document.getElementById('legal-form');
    const analyzeBtn = document.getElementById('analyze-btn');
    
    // Add loading state to the form submission
    if (legalForm) {
        legalForm.addEventListener('submit', function() {
            // Show loading state on button
            if (analyzeBtn) {
                analyzeBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Analyzing...';
                analyzeBtn.disabled = true;
            }
        });
    }
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Add copy functionality for text blocks
    const copyButtons = document.querySelectorAll('.copy-btn');
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const textToCopy = this.getAttribute('data-text');
            navigator.clipboard.writeText(textToCopy).then(() => {
                // Change button text temporarily
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-check"></i> Copied!';
                setTimeout(() => {
                    this.innerHTML = originalText;
                }, 2000);
            });
        });
    });
    
    // Word counter for text area
    const legalTextArea = document.getElementById('legal_text');
    const wordCountDisplay = document.getElementById('word-count');
    
    if (legalTextArea && wordCountDisplay) {
        legalTextArea.addEventListener('input', function() {
            const text = this.value.trim();
            const wordCount = text ? text.split(/\s+/).length : 0;
            wordCountDisplay.textContent = `${wordCount} words`;
        });
        
        // Trigger on page load to show initial count
        legalTextArea.dispatchEvent(new Event('input'));
    }
    
    // Make text area auto-resize to content
    if (legalTextArea) {
        legalTextArea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    }
});
