// ------------------- Global Functions -------------------

// Loading overlay
function showLoading(message = 'Processing...') {
    const overlay = document.getElementById('loading-overlay');
    const loadingText = document.getElementById('loading-text');
    if (overlay && loadingText) {
        loadingText.textContent = message;
        overlay.classList.add('active');
    }
}

function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) overlay.classList.remove('active');
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
});

// Form validation enhancement
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        const requiredFields = this.querySelectorAll('[required]');
        let isValid = true;
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                field.classList.add('error');
                field.addEventListener('input', function() {
                    this.classList.remove('error');
                }, { once: true });
            }
        });
        if (!isValid) {
            e.preventDefault();
            alert('Please fill in all required fields');
        }
    });
});

// IntersectionObserver for stat cards
const observerOptions = { threshold: 0.3, rootMargin: '0px 0px -100px 0px' };
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'fadeInUp 0.6s ease-out';
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);
document.querySelectorAll('.stat-card, .feature-card').forEach(card => observer.observe(card));

// FadeInUp animation style
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
`;
document.head.appendChild(style);

// Copy to clipboard
async function copyToClipboard(text) {
    try { await navigator.clipboard.writeText(text); return true; }
    catch (err) { console.error('Failed to copy: ', err); return false; }
}

// Mobile menu toggle
function toggleMobileMenu() {
    const navMenu = document.querySelector('.nav-menu');
    if (navMenu) navMenu.classList.toggle('active');
}

// Auto-resize textareas
document.querySelectorAll('textarea').forEach(textarea => {
    textarea.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
});

// Format numbers
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Debounce
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => { clearTimeout(timeout); func(...args); };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Session storage for form persistence
function saveFormData(formId) {
    const form = document.getElementById(formId);
    if (form) {
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        sessionStorage.setItem(formId, JSON.stringify(data));
    }
}

function loadFormData(formId) {
    const saved = sessionStorage.getItem(formId);
    if (saved) {
        const data = JSON.parse(saved);
        const form = document.getElementById(formId);
        if (form) {
            Object.keys(data).forEach(key => {
                const field = form.elements[key];
                if (field) field.value = data[key];
            });
        }
    }
}

// ------------------- Form Submissions -------------------

// Campaign Form
async function submitCampaignForm(event) {
    event.preventDefault();
    const form = event.target;
    const data = Object.fromEntries(new FormData(form));

    showLoading('Generating campaign...');
    try {
        const response = await fetch('/api/generate_campaign', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();

        if (result.success && result.campaign) {
            const campaign = result.campaign;
            const outputHtml = `
                <p><strong>Objective:</strong> ${campaign.campaign_objective}</p>
                <p><strong>Timeline:</strong> ${campaign.campaign_timeline}</p>
                <p><strong>Expected Metrics:</strong> ${campaign.expected_metrics}</p>
                <p><strong>Content Ideas:</strong> ${campaign.content_ideas.join(', ')}</p>
                <p><strong>Ad Copies:</strong> ${campaign.ad_copy.join(', ')}</p>
                <p><strong>Call to Action:</strong> ${campaign.call_to_action}</p>
                <p><strong>Hashtags:</strong> ${campaign.hashtags.join(', ')}</p>
            `;
            const outputDiv = document.getElementById('campaign-output');
            if (outputDiv) outputDiv.innerHTML = outputHtml;
        } else {
            alert('Error generating campaign: ' + (result.error || 'Unknown error'));
        }
    } catch (err) {
        console.error('Campaign request failed:', err);
        alert('Failed to generate campaign. Check console for details.');
    } finally {
        hideLoading();
    }
}

// Pitch Form
async function submitPitchForm(event) {
    event.preventDefault();
    const form = event.target;
    const data = Object.fromEntries(new FormData(form));

    showLoading('Generating pitch...');
    try {
        const response = await fetch('/api/generate_pitch', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();

        if (result.success && result.pitch) {
            const pitch = result.pitch;
            const outputHtml = `
                <p><strong>Elevator Pitch:</strong> ${pitch.elevator_pitch}</p>
                <p><strong>Value Proposition:</strong> ${pitch.value_proposition}</p>
                <p><strong>Key Differentiators:</strong> ${pitch.key_differentiators.join(', ')}</p>
                <p><strong>Pain Points Solved:</strong> ${pitch.pain_points_solved}</p>
                <p><strong>Call to Action:</strong> ${pitch.call_to_action}</p>
                <p><strong>Email Template:</strong> ${pitch.email_pitch_template}</p>
                <p><strong>LinkedIn Message:</strong> ${pitch.linkedin_outreach_message}</p>
            `;
            const outputDiv = document.getElementById('pitch-output');
            if (outputDiv) outputDiv.innerHTML = outputHtml;
        } else {
            alert('Error generating pitch: ' + (result.error || 'Unknown error'));
        }
    } catch (err) {
        console.error('Pitch request failed:', err);
        alert('Failed to generate pitch. Check console for details.');
    } finally {
        hideLoading();
    }
}

// Lead Form
async function submitLeadForm(event) {
    event.preventDefault();
    const form = event.target;
    const data = Object.fromEntries(new FormData(form));

    showLoading('Scoring lead...');

    try {
        const response = await fetch('/api/score_lead', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();

        if (result.success && result.lead_score) {
            const lead = result.lead_score;

            // Safe default: recommended_actions might be missing
            const actions = Array.isArray(lead.recommended_actions) ? lead.recommended_actions : [];

            // Safe defaults for all fields
            const leadScore = lead.lead_score ?? 'N/A';
            const leadCategory = lead.lead_category ?? 'N/A';
            const conversion = lead.conversion_probability ?? 'N/A';
            const explanation = lead.explanation ?? 'No explanation provided';

            const outputHtml = `
                <p><strong>Lead Score:</strong> ${leadScore}</p>
                <p><strong>Category:</strong> ${leadCategory}</p>
                <p><strong>Conversion Probability:</strong> ${conversion}</p>
                <p><strong>Explanation:</strong> ${explanation}</p>
                <p><strong>Recommended Actions:</strong></p>
                <ul>${actions.map(a => `<li>${a}</li>`).join('')}</ul>
            `;
            const outputDiv = document.getElementById('lead-output');
            if (outputDiv) outputDiv.innerHTML = outputHtml;

            if (actions.length > 0) await copyToClipboard(actions[0]);

        } else {
            alert('Error scoring lead: ' + (result.error || 'Unknown error'));
        }

    } catch (err) {
        console.error('Lead scoring request failed:', err);
        alert('Failed to score lead. Check console for details.');
    } finally {
        hideLoading();
    }
}
// ------------------- DOMContentLoaded -------------------
document.addEventListener('DOMContentLoaded', () => {
    // Load saved form data
    ['campaignForm', 'pitchForm', 'leadForm'].forEach(formId => loadFormData(formId));

    // Auto-save forms
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('input', debounce(() => saveFormData(form.id), 1000));
    });

    // Attach form submissions
    const campaignForm = document.getElementById('campaignForm');
    if (campaignForm) campaignForm.addEventListener('submit', submitCampaignForm);

    const pitchForm = document.getElementById('pitchForm');
    if (pitchForm) pitchForm.addEventListener('submit', submitPitchForm);

    const leadForm = document.getElementById('leadForm');
    if (leadForm) leadForm.addEventListener('submit', submitLeadForm);
});
