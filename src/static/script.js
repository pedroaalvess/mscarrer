// Global variables
let currentSlide = 0;
let currentJobIndex = 0;
let allJobs = [];
let filteredJobs = [];
let selectedJobId = null;

// Show success animation - Simplified for mobile
function showSuccessAnimation() {
    const successAnimation = document.getElementById('successAnimation');
    if (successAnimation) {
        successAnimation.style.display = 'flex';
        document.body.style.overflow = 'hidden';
        
        // Simple close button event
        const successButton = successAnimation.querySelector('.success-button');
        if (successButton) {
            successButton.onclick = closeSuccessAnimation;
        }
        
        // Close on background click
        successAnimation.onclick = function(e) {
            if (e.target === successAnimation) {
                closeSuccessAnimation();
            }
        };
        
        // Auto close after 5 seconds
        setTimeout(closeSuccessAnimation, 5000);
    }
}

// Close success animation - Simplified
function closeSuccessAnimation() {
    const successAnimation = document.getElementById('successAnimation');
    if (successAnimation) {
        successAnimation.style.display = 'none';
        document.body.style.overflow = 'auto';
        
        // Reset form
        const form = document.getElementById('applicationForm');
        if (form) {
            form.reset();
            
            // Reset phone
            const phoneInput = document.getElementById('phone');
            if (phoneInput) phoneInput.value = '+33 ';
            
            // Reset job select
            const jobSelect = document.getElementById('jobSelect');
            if (jobSelect) jobSelect.value = '';
        }
    }
}

// Format birth date input - Enhanced version
function formatBirthDate(input) {
    let value = input.value.replace(/\D/g, ''); // Remove non-digits
    let formattedValue = '';
    
    // Limit to 8 digits (DDMMYYYY)
    value = value.substring(0, 8);
    
    // Add formatting as user types
    if (value.length > 0) {
        formattedValue = value.substring(0, 2); // DD
        if (value.length >= 3) {
            formattedValue += '/' + value.substring(2, 4); // DD/MM
            if (value.length >= 5) {
                formattedValue += '/' + value.substring(4, 8); // DD/MM/YYYY
            }
        }
    }
    
    input.value = formattedValue;
}

// Validate birth date
function validateBirthDate(dateString) {
    const regex = /^(\d{2})\/(\d{2})\/(\d{4})$/;
    const match = dateString.match(regex);
    
    if (!match) return false;
    
    const day = parseInt(match[1], 10);
    const month = parseInt(match[2], 10);
    const year = parseInt(match[3], 10);
    
    // Basic validation
    if (month < 1 || month > 12) return false;
    if (day < 1 || day > 31) return false;
    if (year < 1900 || year > new Date().getFullYear() - 16) return false;
    
    // Check if date is valid
    const date = new Date(year, month - 1, day);
    return date.getFullYear() === year && 
           date.getMonth() === month - 1 && 
           date.getDate() === day;
}

// Setup birth date input - Enhanced version
function setupBirthDateInput() {
    const birthDateInput = document.getElementById('birthDate');
    if (birthDateInput) {
        // Set placeholder
        birthDateInput.placeholder = '00/00/0000';
        
        // Format on input
        birthDateInput.addEventListener('input', function(e) {
            formatBirthDate(e.target);
        });
        
        // Prevent non-numeric input except backspace/delete
        birthDateInput.addEventListener('keydown', function(e) {
            // Allow: backspace, delete, tab, escape, enter
            if ([8, 9, 27, 13, 46].indexOf(e.keyCode) !== -1 ||
                // Allow: Ctrl+A, Ctrl+C, Ctrl+V, Ctrl+X
                (e.keyCode === 65 && e.ctrlKey === true) ||
                (e.keyCode === 67 && e.ctrlKey === true) ||
                (e.keyCode === 86 && e.ctrlKey === true) ||
                (e.keyCode === 88 && e.ctrlKey === true)) {
                return;
            }
            // Ensure that it is a number and stop the keypress
            if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
                e.preventDefault();
            }
        });
        
        // Validate on blur
        birthDateInput.addEventListener('blur', function(e) {
            const value = e.target.value;
            if (value && !validateBirthDate(value)) {
                e.target.setCustomValidity('Veuillez entrer une date de naissance valide (JJ/MM/AAAA)');
            } else {
                e.target.setCustomValidity('');
            }
        });
        
        // Better mobile styling
        birthDateInput.style.fontSize = '16px'; // Prevents zoom on iOS
        birthDateInput.style.padding = '12px 15px';
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeCarousel();
    loadJobs();
    setupPhoneFormatting();
    setupBirthDateInput();
    setupFormSubmission();
});

// Carousel functionality
function initializeCarousel() {
    const slides = document.querySelectorAll('.carousel-slide');
    const indicators = document.querySelectorAll('.indicator');
    
    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.classList.toggle('active', i === index);
        });
        indicators.forEach((indicator, i) => {
            indicator.classList.toggle('active', i === index);
        });
        currentSlide = index;
    }
    
    function nextSlide() {
        const nextIndex = (currentSlide + 1) % slides.length;
        showSlide(nextIndex);
    }
    
    // Auto-advance carousel
    setInterval(nextSlide, 5000);
    
    // Manual navigation
    window.currentSlide = showSlide;
}

// Phone formatting for French format - Simplified
function setupPhoneFormatting() {
    const phoneInput = document.getElementById('phone');
    if (phoneInput) {
        // Set initial value
        phoneInput.value = '+33 ';
        
        phoneInput.addEventListener('input', function(e) {
            let value = e.target.value;
            
            // Always start with +33
            if (!value.startsWith('+33 ')) {
                value = '+33 ';
            }
            
            // Remove everything except numbers after +33
            let numbers = value.substring(4).replace(/\D/g, '');
            
            // Limit to 10 digits
            numbers = numbers.substring(0, 10);
            
            // Format as +33 X XX XX XX XX
            let formatted = '+33 ';
            if (numbers.length > 0) {
                formatted += numbers.substring(0, 1);
                if (numbers.length > 1) formatted += ' ' + numbers.substring(1, 3);
                if (numbers.length > 3) formatted += ' ' + numbers.substring(3, 5);
                if (numbers.length > 5) formatted += ' ' + numbers.substring(5, 7);
                if (numbers.length > 7) formatted += ' ' + numbers.substring(7, 9);
                if (numbers.length > 9) formatted += ' ' + numbers.substring(9, 10);
            }
            
            e.target.value = formatted;
        });
        
        phoneInput.addEventListener('keydown', function(e) {
            // Prevent deleting +33 prefix
            if ((e.key === 'Backspace' || e.key === 'Delete') && 
                e.target.selectionStart <= 4) {
                e.preventDefault();
            }
        });
        
        phoneInput.addEventListener('focus', function(e) {
            // Set cursor after +33 
            if (e.target.value === '+33 ') {
                setTimeout(() => {
                    e.target.setSelectionRange(4, 4);
                }, 0);
            }
        });
    }
}

// Load jobs from API
async function loadJobs() {
    try {
        const response = await fetch('/api/jobs');
        const data = await response.json();
        
        if (data.success) {
            allJobs = data.jobs;
            filteredJobs = [...allJobs];
            displayJobs();
            populateJobSelect();
        } else {
            console.error('Error loading jobs:', data.error);
        }
    } catch (error) {
        console.error('Error loading jobs:', error);
    }
}

// Display jobs in carousel
function displayJobs() {
    const container = document.getElementById('jobsContainer');
    if (!container) return;
    
    // Job images mapping
    const jobImages = {
        1: 'images/job-xbox-marketing-final.jpg',
        2: 'images/job-data-scientist-final.webp', 
        3: 'images/job-frontend-teams-final.png',
        4: 'images/job-cybersecurity-final.jpg',
        5: 'images/job-product-manager-final.jpg',
        6: 'images/job-azure-engineer-final.jpg'
    };
    
    container.innerHTML = filteredJobs.map(job => `
        <div class="job-card" data-job-id="${job.id}">
            <div class="job-image">
                <img src="${jobImages[job.id] || 'images/default-job.jpg'}" alt="${job.title}" loading="lazy">
            </div>
            <div class="job-content">
                <h3>${job.title}</h3>
                <div class="job-meta">
                    <span class="job-location">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M21 10C21 17 12 23 12 23S3 17 3 10C3 5.02944 7.02944 1 12 1C16.9706 1 21 5.02944 21 10Z" stroke="#0078D4" stroke-width="2"/>
                            <circle cx="12" cy="10" r="3" stroke="#0078D4" stroke-width="2"/>
                        </svg>
                        ${job.location}
                    </span>
                    <span class="job-department">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M20 7H4C2.9 7 2 7.9 2 9V18C2 19.1 2.9 20 4 20H20C21.1 20 22 19.1 22 18V9C22 7.9 21.1 7 20 7Z" stroke="#0078D4" stroke-width="2"/>
                            <path d="M16 21V5C16 3.9 15.1 3 14 3H10C8.9 3 8 3.9 8 5V21" stroke="#0078D4" stroke-width="2"/>
                        </svg>
                        ${job.department}
                    </span>
                    <span class="job-type">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <circle cx="12" cy="12" r="10" stroke="#0078D4" stroke-width="2"/>
                            <polyline points="12,6 12,12 16,14" stroke="#0078D4" stroke-width="2"/>
                        </svg>
                        ${job.employment_type}
                    </span>
                </div>
                <p class="job-description">${job.description}</p>
                <button class="btn-primary" onclick="applyForJob(${job.id}, '${job.title}')">Postuler</button>
            </div>
        </div>
    `).join('');
}

// Populate job select dropdown
function populateJobSelect() {
    const select = document.getElementById('jobSelect');
    if (!select) return;
    
    select.innerHTML = '<option value="">Sélectionnez un poste</option>' +
        allJobs.map(job => `<option value="${job.id}">${job.title}</option>`).join('');
}

// Apply for job - scroll to form and pre-select job
function applyForJob(jobId, jobTitle) {
    selectedJobId = jobId;
    
    // Scroll to application form
    const formSection = document.getElementById('candidature');
    if (formSection) {
        formSection.scrollIntoView({ behavior: 'smooth' });
        
        // Pre-select the job in the dropdown
        setTimeout(() => {
            const jobSelect = document.getElementById('jobSelect');
            if (jobSelect) {
                jobSelect.value = jobId;
            }
        }, 500);
    }
}

// Job filtering
function filterJobs() {
    const departmentFilter = document.getElementById('departmentFilter').value;
    const levelFilter = document.getElementById('levelFilter').value;
    const typeFilter = document.getElementById('typeFilter').value;
    
    filteredJobs = allJobs.filter(job => {
        return (!departmentFilter || job.department === departmentFilter) &&
               (!levelFilter || job.experience_level === levelFilter) &&
               (!typeFilter || job.employment_type === typeFilter);
    });
    
    currentJobIndex = 0;
    displayJobs();
}

// Job carousel navigation
function nextJob() {
    if (currentJobIndex < filteredJobs.length - 3) {
        currentJobIndex++;
        updateJobCarousel();
    }
}

function previousJob() {
    if (currentJobIndex > 0) {
        currentJobIndex--;
        updateJobCarousel();
    }
}

function updateJobCarousel() {
    const container = document.getElementById('jobsContainer');
    if (container) {
        const cardWidth = 350; // Width of each job card + margin
        container.style.transform = `translateX(-${currentJobIndex * cardWidth}px)`;
    }
}

// Form submission - Simplified for mobile compatibility
function setupFormSubmission() {
    const form = document.getElementById('applicationForm');
    const submitButton = form.querySelector('button[type="submit"]');
    
    if (form && submitButton) {
        // Remove any existing listeners
        form.removeEventListener('submit', handleFormSubmit);
        submitButton.removeEventListener('click', handleFormSubmit);
        
        // Add simple event listeners
        form.addEventListener('submit', handleFormSubmit);
        submitButton.addEventListener('click', handleFormSubmit);
        
        // Force mobile compatibility
        submitButton.style.webkitTapHighlightColor = 'transparent';
        submitButton.style.touchAction = 'manipulation';
    }
}

// Simplified form submission handler
async function handleFormSubmit(e) {
    e.preventDefault();
    e.stopPropagation();
    
    const form = document.getElementById('applicationForm');
    const submitButton = form.querySelector('button[type="submit"]');
    
    // Prevent double submission
    if (submitButton.disabled) return;
    
    // Show loading
    submitButton.textContent = 'Envoi...';
    submitButton.disabled = true;
    submitButton.style.opacity = '0.7';
    
    try {
        const formData = new FormData(form);
        const jobId = formData.get('job_id');
        
        if (!jobId) {
            alert('Veuillez sélectionner un poste');
            resetButton();
            return;
        }
        
        // Simple fetch without complex headers
        const response = await fetch(`/api/jobs/${jobId}/apply`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Show success
            showSuccessAnimation();
        } else {
            alert('Erreur: ' + (data.error || 'Erreur inconnue'));
        }
        
    } catch (error) {
        console.error('Error:', error);
        alert('Erreur de connexion. Veuillez réessayer.');
    } finally {
        resetButton();
    }
    
    function resetButton() {
        submitButton.textContent = 'Envoyer ma candidature';
        submitButton.disabled = false;
        submitButton.style.opacity = '1';
    }
}

// Utility functions
function scrollToJobs() {
    const jobsSection = document.getElementById('emplois');
    if (jobsSection) {
        jobsSection.scrollIntoView({ behavior: 'smooth' });
    }
}

function scrollToApplication() {
    const applicationSection = document.getElementById('candidature');
    if (applicationSection) {
        applicationSection.scrollIntoView({ behavior: 'smooth' });
    }
}

function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    if (notification) {
        notification.textContent = message;
        notification.className = `notification ${type} show`;
        
        setTimeout(() => {
            notification.classList.remove('show');
        }, 5000);
    }
}

