// Exchange rate constants
const EXCHANGE_RATE = 6.68031791 / 1000;
const ERROR_RATE = 0.0119695182 / 1000;

// DOM elements
const amountInput = document.getElementById('amount');
const resultAmountEl = document.querySelector('.result-amount');
const resultErrorEl = document.getElementById('result-error');
const rateDisplayEl = document.getElementById('rate-display');
const converterCard = document.querySelector('.converter-card');

// Format number with proper decimals and thousands separators
function formatNumber(number, decimals = 2) {
    return new Intl.NumberFormat('en-US', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    }).format(number);
}

// Animate number changes
function animateValue(element, start, end, duration = 500) {
    const startTime = performance.now();
    const range = end - start;
    
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function for smooth animation
        const easeOutQuad = 1 - (1 - progress) * (1 - progress);
        const current = start + (range * easeOutQuad);
        
        element.textContent = formatNumber(current);
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    
    requestAnimationFrame(update);
}

// Update conversion result
function updateConversion() {
    const amount = parseFloat(amountInput.value) || 0;
    
    if (amount < 0) {
        amountInput.value = '';
        return;
    }
    
    // Calculate conversion
    const convertedAmount = amount * EXCHANGE_RATE;
    const errorAmount = amount * ERROR_RATE;
    
    // Get previous value for animation
    const prevValue = parseFloat(resultAmountEl.textContent.replace(/,/g, '')) || 0;
    
    // Animate the result change
    if (Math.abs(convertedAmount - prevValue) > 0.01) {
        animateValue(resultAmountEl, prevValue, convertedAmount);
    } else {
        resultAmountEl.textContent = formatNumber(convertedAmount);
    }
    
    // Update error margin
    if (amount > 0) {
        resultErrorEl.textContent = `± ${formatNumber(errorAmount)} BYN uncertainty`;
        resultErrorEl.style.opacity = '1';
    } else {
        resultErrorEl.textContent = '';
        resultErrorEl.style.opacity = '0';
    }
    
    // Add visual feedback for successful conversion
    if (amount > 0) {
        converterCard.style.transform = 'scale(1.01)';
        setTimeout(() => {
            converterCard.style.transform = '';
        }, 150);
    }
}

// Debounce function to limit API calls
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Debounced update function
const debouncedUpdate = debounce(updateConversion, 100);

// Input validation
function validateInput(event) {
    const value = event.target.value;
    
    // Remove any non-numeric characters except decimal point
    const cleanValue = value.replace(/[^\d.]/g, '');
    
    // Ensure only one decimal point
    const parts = cleanValue.split('.');
    if (parts.length > 2) {
        event.target.value = parts[0] + '.' + parts.slice(1).join('');
        return;
    }
    
    // Limit decimal places to 2
    if (parts[1] && parts[1].length > 2) {
        event.target.value = parts[0] + '.' + parts[1].substring(0, 2);
        return;
    }
    
    // Prevent starting with multiple zeros
    if (cleanValue.length > 1 && cleanValue[0] === '0' && cleanValue[1] !== '.') {
        event.target.value = cleanValue.substring(1);
        return;
    }
    
    event.target.value = cleanValue;
}

// Initialize the app
function initializeApp() {
    // Set up rate display
    rateDisplayEl.textContent = `1 KZT = ${formatNumber(EXCHANGE_RATE, 5)} BYN`;
    
    // Initial conversion
    updateConversion();
    
    // Add event listeners
    amountInput.addEventListener('input', (event) => {
        validateInput(event);
        debouncedUpdate();
    });
    
    amountInput.addEventListener('keydown', (event) => {
        // Allow special keys
        const allowedKeys = [
            'Backspace', 'Delete', 'Tab', 'Escape', 'Enter',
            'ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown',
            'Home', 'End'
        ];
        
        if (allowedKeys.includes(event.key)) {
            return;
        }
        
        // Allow Ctrl+A, Ctrl+C, Ctrl+V, Ctrl+X
        if (event.ctrlKey && ['a', 'c', 'v', 'x'].includes(event.key.toLowerCase())) {
            return;
        }
        
        // Allow numbers and decimal point
        if (!/[\d.]/.test(event.key)) {
            event.preventDefault();
        }
    });
    
    // Add paste event listener
    amountInput.addEventListener('paste', (event) => {
        setTimeout(() => {
            validateInput(event);
            debouncedUpdate();
        }, 0);
    });
    
    // Focus the input on load
    amountInput.focus();
    
    // Add subtle entrance animation
    setTimeout(() => {
        converterCard.style.opacity = '1';
        converterCard.style.transform = 'translateY(0)';
    }, 100);
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeApp);
} else {
    initializeApp();
}
