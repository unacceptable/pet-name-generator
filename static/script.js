// API Configuration
let API_BASE = window.location.protocol + '//' + window.location.hostname;

if (!['80', '443'].includes(window.location.port)) {
    API_BASE += `:${window.location.port}`;
}

// Pet facts cache (will be populated from API)
let PET_FACTS_CACHE = {};

// DOM Elements
const petCards = document.querySelectorAll('.pet-card');
const generateBtn = document.getElementById('generateNames');
const randomBtn = document.getElementById('randomName');
const nameCountInput = document.getElementById('nameCount');
const countBtns = document.querySelectorAll('.count-btn');
const optionsSection = document.getElementById('optionsSection');
const resultsSection = document.getElementById('resultsSection');
const namesContainer = document.getElementById('namesContainer');
const copyBtn = document.getElementById('copyNames');
const loadingSpinner = document.getElementById('loadingSpinner');
const errorMessage = document.getElementById('errorMessage');
const errorText = document.getElementById('errorText');
const closeError = document.getElementById('closeError');
const funFact = document.getElementById('funFact');

// State
let selectedPetType = null;
let currentNames = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    updateButtonStates();
    loadRandomFact();
});

// Event Listeners Setup
function setupEventListeners() {
    // Pet card selection
    petCards.forEach(card => {
        card.addEventListener('click', () => selectPetType(card));
    });

    // Count selector buttons
    countBtns.forEach(btn => {
        btn.addEventListener('click', () => adjustCount(btn));
    });

    // Generate names button
    generateBtn.addEventListener('click', generateNames);

    // Random name button
    randomBtn.addEventListener('click', getRandomName);

    // Copy names button
    copyBtn.addEventListener('click', copyNamesToClipboard);

    // Close error message
    closeError.addEventListener('click', hideError);

    // Name count input validation
    nameCountInput.addEventListener('change', validateCount);

    // Auto-hide error after 5 seconds
    setTimeout(() => {
        if (errorMessage.classList.contains('show')) {
            hideError();
        }
    }, 5000);
}

// Pet Type Selection
function selectPetType(card) {
    // Remove previous selection
    petCards.forEach(c => c.classList.remove('selected'));

    // Select new pet type
    card.classList.add('selected');
    selectedPetType = card.dataset.type;

    // Show options section with animation
    showOptionsSection();

    // Update button states and show relevant fact
    updateButtonStates();
    showPetFact(selectedPetType);

    // Add selection animation
    card.style.transform = 'translateY(-10px) scale(1.05)';
    setTimeout(() => {
        card.style.transform = '';
    }, 300);
}

// Count Adjustment
function adjustCount(btn) {
    const action = btn.dataset.action;
    let currentCount = parseInt(nameCountInput.value);

    if (action === 'increase' && currentCount < 10) {
        nameCountInput.value = currentCount + 1;
    } else if (action === 'decrease' && currentCount > 1) {
        nameCountInput.value = currentCount - 1;
    }

    // Add button click animation
    btn.style.transform = 'scale(0.9)';
    setTimeout(() => {
        btn.style.transform = '';
    }, 150);
}

// Count Validation
function validateCount() {
    let count = parseInt(nameCountInput.value);
    if (count < 1) nameCountInput.value = 1;
    if (count > 10) nameCountInput.value = 10;
}

// Button State Management
function updateButtonStates() {
    const hasSelection = selectedPetType !== null;
    generateBtn.disabled = !hasSelection;
    randomBtn.disabled = !hasSelection;

    if (hasSelection) {
        generateBtn.style.opacity = '1';
        randomBtn.style.opacity = '1';
    } else {
        generateBtn.style.opacity = '0.6';
        randomBtn.style.opacity = '0.6';
    }
}

// Show Options Section
function showOptionsSection() {
    optionsSection.classList.remove('hidden');
    optionsSection.classList.add('show');

    // Smooth scroll to options after animation starts
    setTimeout(() => {
        optionsSection.scrollIntoView({
            behavior: 'smooth',
            block: 'start',
            inline: 'nearest'
        });
    }, 200);
}

// API Calls
async function makeApiCall(endpoint, options = {}) {
    try {
        showLoading();
        const response = await fetch(`${API_BASE}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
            },
            ...options
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.status} - ${response.statusText}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('API Error:', error);
        showError(error.message || 'Failed to connect to the API. Please try again.');
        throw error;
    } finally {
        hideLoading();
    }
}

// Generate Multiple Names
async function generateNames() {
    if (!selectedPetType) return;

    try {
        const count = parseInt(nameCountInput.value);
        const data = await makeApiCall(`/pets/${selectedPetType}/names?count=${count}&random_selection=true`);

        currentNames = data.names;
        displayNames(currentNames);
        showPetFact(selectedPetType);

        // Analytics-like tracking (optional)
        trackEvent('generate_names', selectedPetType, count);

    } catch (error) {
        console.error('Error generating names:', error);
    }
}

// Get Single Random Name
async function getRandomName() {
    if (!selectedPetType) return;

    try {
        const data = await makeApiCall(`/pets/${selectedPetType}/random`);

        currentNames = [data.name];
        displaySingleName(data.name);
        showPetFact(selectedPetType);

        // Analytics-like tracking (optional)
        trackEvent('random_name', selectedPetType, 1);

    } catch (error) {
        console.error('Error getting random name:', error);
    }
}

// Display Results
function displayNames(names) {
    namesContainer.innerHTML = '';

    if (names.length === 1) {
        displaySingleName(names[0]);
        return;
    }

    names.forEach((name, index) => {
        const nameTag = document.createElement('div');
        nameTag.className = 'name-tag';
        nameTag.textContent = name;
        nameTag.style.animationDelay = `${index * 0.1}s`;

        // Add click to copy individual name
        nameTag.addEventListener('click', () => {
            copyToClipboard(name);
            showSuccessMessage(`Copied "${name}" to clipboard!`);
        });

        namesContainer.appendChild(nameTag);
    });

    showResults();
}

function displaySingleName(name) {
    namesContainer.innerHTML = `<div class="single-name">${name}</div>`;
    showResults();
}

function showResults() {
    resultsSection.classList.add('show');
    copyBtn.style.display = 'flex';

    // Smooth scroll to results
    setTimeout(() => {
        resultsSection.scrollIntoView({
            behavior: 'smooth',
            block: 'center'
        });
    }, 300);
}

// Copy Functionality
async function copyNamesToClipboard() {
    if (currentNames.length === 0) return;

    const text = currentNames.join(', ');
    await copyToClipboard(text);
    showSuccessMessage('Names copied to clipboard! 🎉');
}

async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
    } catch (error) {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
    }
}

// UI State Management
function showLoading() {
    loadingSpinner.classList.add('show');
    generateBtn.disabled = true;
    randomBtn.disabled = true;
}

function hideLoading() {
    loadingSpinner.classList.remove('show');
    updateButtonStates();
}

function showError(message) {
    errorText.textContent = message;
    errorMessage.classList.add('show');

    // Auto-hide after 5 seconds
    setTimeout(() => {
        hideError();
    }, 5000);
}

function hideError() {
    errorMessage.classList.remove('show');
}

function showSuccessMessage(message) {
    // Create temporary success message
    const successMsg = document.createElement('div');
    successMsg.className = 'error-message show';
    successMsg.style.background = 'linear-gradient(135deg, #00b894, #00a085)';
    successMsg.innerHTML = `
        <i class="fas fa-check-circle"></i>
        <span>${message}</span>
    `;

    document.body.appendChild(successMsg);

    setTimeout(() => {
        successMsg.remove();
    }, 3000);
}

// Fun Facts
async function showPetFact(petType) {
    try {
        const data = await makeApiCall(`/pets/${petType}/facts/random`);
        displayFact(data.fact);
    } catch (error) {
        console.error('Error loading pet fact:', error);
        // Fallback to generic message
        displayFact("Learning about pets is fun! 🐾");
    }
}

async function loadRandomFact() {
    try {
        const data = await makeApiCall(`/facts/random`);
        displayFact(data.fact);
    } catch (error) {
        console.error('Error loading random fact:', error);
        // Fallback message
        displayFact("Click 'Generate Names' to get started and discover fun pet facts!");
    }
}

function displayFact(factText) {
    const factElement = funFact.querySelector('p');

    // Add animation
    funFact.style.transform = 'scale(0.95)';
    funFact.style.opacity = '0.7';

    setTimeout(
        () => {
            factElement.textContent = factText;
            funFact.style.transform = 'scale(1)';
            funFact.style.opacity = '1';
        },
        200
    );
}

// Analytics-like Event Tracking (optional)
function trackEvent(action, petType, count) {
    // This could be connected to Google Analytics or other tracking services
    console.log(`Event: ${action}, Pet: ${petType}, Count: ${count}`);

    // Example: Google Analytics 4
    // if (typeof gtag !== 'undefined') {
    //     gtag('event', action, {
    //         'pet_type': petType,
    //         'name_count': count
    //     });
    // }
}

// Keyboard Shortcuts
document.addEventListener('keydown', function(event) {
    // Space bar to generate names
    if (event.code === 'Space' && selectedPetType) {
        event.preventDefault();
        generateNames();
    }

    // R key for random name
    if (event.key.toLowerCase() === 'r' && selectedPetType) {
        event.preventDefault();
        getRandomName();
    }

    // Escape to close error
    if (event.key === 'Escape') {
        hideError();
    }

    // C key to copy (when names are visible)
    if (event.key.toLowerCase() === 'c' && currentNames.length > 0 && !event.ctrlKey && !event.metaKey) {
        event.preventDefault();
        copyNamesToClipboard();
    }
});

// Easter Eggs
let clickCount = 0;
document.querySelector('.title').addEventListener('click', function() {
    clickCount++;
    if (clickCount === 5) {
        showSuccessMessage('🐾 You found an easter egg! You really love pets! 🐾');
        clickCount = 0;
    }
});

// Service Worker Registration (for PWA capabilities)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/static/service-worker.js')
            .then((registration) => {
                console.log('ServiceWorker registration successful');
            })
            .catch((error) => {
                console.log('ServiceWorker registration failed: ', error);
            });
    });
}

// Handle online/offline status
window.addEventListener('online', function() {
    hideError();
    showSuccessMessage('Back online! 🌐');
});

window.addEventListener('offline', function() {
    showError('You are offline. Some features may not work.');
});

// Prevent right-click context menu on name tags (optional)
document.addEventListener('contextmenu', function(event) {
    if (event.target.classList.contains('name-tag')) {
        event.preventDefault();
    }
});

// Add some visual feedback for interactions
document.addEventListener('click', function(event) {
    // Add ripple effect to buttons
    if (event.target.classList.contains('generate-btn') ||
        event.target.classList.contains('random-btn') ||
        event.target.classList.contains('copy-btn')) {

        const button = event.target;
        const rect = button.getBoundingClientRect();
        const ripple = document.createElement('span');
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;

        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            background: rgba(255, 255, 255, 0.5);
            border-radius: 50%;
            transform: scale(0);
            animation: ripple 0.6s linear;
            pointer-events: none;
        `;

        button.style.position = 'relative';
        button.style.overflow = 'hidden';
        button.appendChild(ripple);

        setTimeout(() => {
            ripple.remove();
        }, 600);
    }
});

// Add ripple animation keyframes
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;

document.head.appendChild(style);
