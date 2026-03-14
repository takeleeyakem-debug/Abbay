// ============================================
// MAIN JAVASCRIPT FOR ABBAYTV
// ============================================

// Run this FIRST before anything else to ensure buttons are visible
(function() {
    // Force buttons to be visible immediately
    const style = document.createElement('style');
    style.textContent = `
        .nav-right .btn, 
        .nav-right a, 
        .btn-primary, 
        .btn-secondary {
            display: inline-flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
        }
    `;
    document.head.appendChild(style);
})();

document.addEventListener('DOMContentLoaded', function() {
    
    // ============================================
    // FIX BUTTON VISIBILITY
    // ============================================
    fixButtonVisibility();
    
    // ============================================
    // HAMBURGER MENU FUNCTIONALITY
    // ============================================
    initHamburgerMenu();
    
    // ============================================
    // SPLASH SCREEN
    // ============================================
    if (!sessionStorage.getItem('splashShown')) {
        showSplashScreen();
    }
    
    // ============================================
    // YOUTUBE THUMBNAIL LOADING
    // ============================================
    loadYouTubeThumbnails();
    
    // ============================================
    // AUTO-HIDE ALERTS
    // ============================================
    initAlerts();
    
    // ============================================
    // ADMIN PANEL TABS
    // ============================================
    initAdminTabs();
    
    // ============================================
    // EDIT BUTTONS FUNCTIONALITY
    // ============================================
    initEditButtons();
    
    // ============================================
    // DELETE CONFIRMATION
    // ============================================
    initDeleteConfirmation();
    
    // ============================================
    // PASSWORD STRENGTH INDICATOR
    // ============================================
    initPasswordStrength();
    
    // ============================================
    // YOUTUBE URL PREVIEW
    // ============================================
    initYouTubePreview();
    
    // ============================================
    // FORM VALIDATION
    // ============================================
    initFormValidation();
    
    // ============================================
    // REMEMBER ME FUNCTIONALITY
    // ============================================
    initRememberMe();
    
    // ============================================
    // SCROLL TO TOP BUTTON
    // ============================================
    initScrollToTop();
    
    // ============================================
    // ADMIN SEARCH FUNCTIONALITY
    // ============================================
    initAdminSearch();
    
    // ============================================
    // REAL-TIME CLOCK FOR ADMIN
    // ============================================
    initRealtimeClock();
    
    // ============================================
    // SPARKLE EFFECT ON CARDS
    // ============================================
    initSparkleEffect();
    
    // ============================================
    // LIVE CHAT FUNCTIONALITY
    // ============================================
    initLiveChat();
    
    // ============================================
    // CHECK LIVE STATUS
    // ============================================
    checkLiveStatus();
    
    // ============================================
    // RANDOM LOGIN PROMPTS
    // ============================================
    initRandomLoginPrompts();
});

// ============================================
// FIX BUTTON VISIBILITY
// ============================================
function fixButtonVisibility() {
    // Force all buttons to be visible
    const buttons = document.querySelectorAll('.btn, .nav-right a, .btn-primary, .btn-secondary');
    buttons.forEach(btn => {
        btn.style.display = 'inline-flex';
        btn.style.visibility = 'visible';
        btn.style.opacity = '1';
        btn.style.pointerEvents = 'auto';
    });
    
    // Check every second for 5 seconds to ensure they stay visible
    let count = 0;
    const interval = setInterval(() => {
        const btns = document.querySelectorAll('.btn, .nav-right a');
        btns.forEach(btn => {
            btn.style.display = 'inline-flex';
            btn.style.visibility = 'visible';
            btn.style.opacity = '1';
            btn.style.pointerEvents = 'auto';
        });
        count++;
        if (count >= 5) clearInterval(interval);
    }, 1000);
}

// ============================================
// HAMBURGER MENU FUNCTION
// ============================================
function initHamburgerMenu() {
    const hamburger = document.getElementById('hamburger-btn');
    const navLinks = document.getElementById('navLinks');
    
    if (!hamburger || !navLinks) return;
    
    hamburger.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        this.classList.toggle('active');
        navLinks.classList.toggle('active');
        
        if (navLinks.classList.contains('active')) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }
    });
    
    // Close on link click
    navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            hamburger.classList.remove('active');
            navLinks.classList.remove('active');
            document.body.style.overflow = '';
        });
    });
    
    // Close on outside click
    document.addEventListener('click', (e) => {
        if (!navLinks.contains(e.target) && !hamburger.contains(e.target)) {
            hamburger.classList.remove('active');
            navLinks.classList.remove('active');
            document.body.style.overflow = '';
        }
    });
}

// ============================================
// SPLASH SCREEN
// ============================================
function showSplashScreen() {
    const splash = document.createElement('div');
    splash.id = 'splash-screen';
    splash.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #000000 0%, #0A0A0A 100%);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 999999;
        animation: fadeOut 0.5s ease 2.5s forwards;
    `;
    
    splash.innerHTML = `
        <div style="text-align: center; animation: zoomIn 1.5s ease;">
            <img src="/static/images/logo.png" alt="AbbayTV" style="max-width: 300px; height: auto; margin-bottom: 2rem;" onerror="this.src='https://via.placeholder.com/300x100?text=AbbayTV'">
            <div style="width: 200px; height: 3px; background: rgba(255,215,0,0.2); margin: 0 auto; border-radius: 3px; overflow: hidden;">
                <div style="width: 0%; height: 100%; background: linear-gradient(90deg, #FFD700, #B8860B); animation: loadBar 2.5s linear;"></div>
            </div>
            <p style="color: #FFD700; margin-top: 1rem; font-size: 1.2rem;">Loading...</p>
        </div>
    `;
    
    document.body.appendChild(splash);
    
    // Add animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes zoomIn {
            from { opacity: 0; transform: scale(0.3); }
            to { opacity: 1; transform: scale(1); }
        }
        @keyframes loadBar {
            from { width: 0%; }
            to { width: 100%; }
        }
        @keyframes fadeOut {
            from { opacity: 1; visibility: visible; }
            to { opacity: 0; visibility: hidden; }
        }
    `;
    document.head.appendChild(style);
    
    setTimeout(() => {
        splash.remove();
        sessionStorage.setItem('splashShown', 'true');
    }, 3000);
}

// ============================================
// RANDOM LOGIN PROMPTS
// ============================================
function initRandomLoginPrompts() {
    // Check if user is logged in
    const isLoggedIn = document.querySelector('.nav-right .btn-primary')?.textContent === 'Logout';
    if (isLoggedIn) return;
    
    let lastScrollTime = Date.now();
    let promptCount = 0;
    const MAX_PROMPTS = 2;
    
    window.addEventListener('scroll', function() {
        const now = Date.now();
        if (now - lastScrollTime < 15000) return;
        if (promptCount >= MAX_PROMPTS) return;
        
        if (Math.random() < 0.05) {
            lastScrollTime = now;
            promptCount++;
            showLoginPrompt();
        }
    });
}

function showLoginPrompt() {
    const overlay = document.createElement('div');
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(5px);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 100000;
        animation: fadeIn 0.3s ease;
    `;
    
    overlay.innerHTML = `
        <div style="
            background: linear-gradient(145deg, #1A1A1A 0%, #0D0D0D 100%);
            padding: 2rem;
            border-radius: 12px;
            border: 2px solid #FFD700;
            max-width: 400px;
            text-align: center;
            animation: slideUp 0.3s ease;
        ">
            <h3 style="color: #FFD700; margin-bottom: 1rem;">Join AbbayTV!</h3>
            <p style="color: #CCC; margin-bottom: 2rem;">Login to like, comment, and get updates.</p>
            <div style="display: flex; gap: 1rem; justify-content: center;">
                <a href="/login" class="btn btn-primary" style="padding: 0.8rem 2rem;">Login</a>
                <a href="/signup" class="btn btn-secondary" style="padding: 0.8rem 2rem;">Sign Up</a>
            </div>
            <button onclick="this.closest('div[style*=\\'fixed\\']').remove()" style="
                background: none;
                border: none;
                color: #666;
                margin-top: 1rem;
                cursor: pointer;
            ">Maybe later</button>
        </div>
    `;
    
    document.body.appendChild(overlay);
    
    setTimeout(() => {
        if (overlay.parentNode) overlay.remove();
    }, 20000);
}

// ============================================
// YOUTUBE THUMBNAIL LOADING - FIXED VERSION
// ============================================
function loadYouTubeThumbnails() {
    console.log("Loading YouTube thumbnails..."); // Debug log
    
    // Select all images with the youtube-thumb class
    const thumbnails = document.querySelectorAll('.youtube-thumb');
    console.log("Found", thumbnails.length, "thumbnails"); // Debug log
    
    thumbnails.forEach(img => {
        const url = img.getAttribute('data-youtube-url');
        if (!url) {
            console.log("No URL found for thumbnail");
            return;
        }
        
        console.log("Loading thumbnail for URL:", url); // Debug log
        
        const videoId = extractVideoId(url);
        if (videoId) {
            // Try to load maxresdefault first (HD)
            const maxresUrl = `https://img.youtube.com/vi/${videoId}/maxresdefault.jpg`;
            const hqUrl = `https://img.youtube.com/vi/${videoId}/hqdefault.jpg`;
            const mqUrl = `https://img.youtube.com/vi/${videoId}/mqdefault.jpg`;
            const defaultUrl = `https://img.youtube.com/vi/${videoId}/default.jpg`;
            
            // Try HD first, then fall back to lower qualities
            tryLoadImage(img, maxresUrl, function() {
                // If HD fails, try HQ
                tryLoadImage(img, hqUrl, function() {
                    // If HQ fails, try MQ
                    tryLoadImage(img, mqUrl, function() {
                        // If all fail, use default
                        img.src = defaultUrl;
                        img.style.opacity = '1';
                    });
                });
            });
        } else {
            console.log("Could not extract video ID from URL:", url);
            // Set a placeholder
            img.src = 'https://via.placeholder.com/320x180?text=No+Video';
            img.style.opacity = '1';
        }
    });
}

// Helper function to try loading an image with fallback
function tryLoadImage(imgElement, src, fallbackCallback) {
    const tempImg = new Image();
    tempImg.onload = function() {
        imgElement.src = src;
        imgElement.style.opacity = '1';
        console.log("Successfully loaded:", src);
    };
    tempImg.onerror = function() {
        console.log("Failed to load:", src);
        if (fallbackCallback) fallbackCallback();
    };
    tempImg.src = src;
}

// Improved YouTube ID extractor
function extractVideoId(url) {
    if (!url) return null;
    
    // Handle different YouTube URL formats
    const patterns = [
        /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/v\/|youtube\.com\/live\/)([^&\?\/]+)/,
        /youtube\.com\/shorts\/([^&\?\/]+)/,
        /^([a-zA-Z0-9_-]{11})$/
    ];
    
    for (const pattern of patterns) {
        const match = url.match(pattern);
        if (match) {
            console.log("Extracted video ID:", match[1]); // Debug log
            return match[1];
        }
    }
    
    // If the URL itself might be just the ID (11 characters)
    if (url.length === 11 && /^[a-zA-Z0-9_-]{11}$/.test(url)) {
        return url;
    }
    
    return null;
}

// Make sure to call the function after DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Small delay to ensure DOM is fully ready
    setTimeout(loadYouTubeThumbnails, 100);
});

// Also call it when page is fully loaded (for any late-loading content)
window.addEventListener('load', function() {
    loadYouTubeThumbnails();
});

// ============================================
// ALERTS
// ============================================
function initAlerts() {
    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            if (alert.parentNode) alert.remove();
        }, 5000);
    });
}

// ============================================
// ADMIN TABS
// ============================================
function initAdminTabs() {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const tabId = this.dataset.tab;
            
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            
            this.classList.add('active');
            document.getElementById(tabId)?.classList.add('active');
        });
    });
}

// ============================================
// EDIT BUTTONS
// ============================================
function initEditButtons() {
    // News edit
    document.querySelectorAll('.edit-news-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const form = document.getElementById('edit-news-form');
            if (form) {
                document.getElementById('edit-news-id').value = this.dataset.id;
                document.getElementById('edit-news-title').value = this.dataset.title;
                document.getElementById('edit-news-url').value = this.dataset.url;
                document.getElementById('edit-news-description').value = this.dataset.description;
                form.style.display = 'block';
                form.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
}

// ============================================
// DELETE CONFIRMATION
// ============================================
function initDeleteConfirmation() {
    document.querySelectorAll('.delete-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!confirm('Are you sure you want to delete this item?')) {
                e.preventDefault();
            }
        });
    });
}

// ============================================
// PASSWORD STRENGTH
// ============================================
function initPasswordStrength() {
    const password = document.getElementById('password');
    const confirm = document.getElementById('confirm_password');
    
    if (password) {
        password.addEventListener('input', function() {
            const strength = this.value.length;
            let message = '';
            let color = '#FF4444';
            
            if (strength === 0) message = '';
            else if (strength < 6) message = 'Too short';
            else if (strength < 8) message = 'Weak';
            else if (strength < 10) message = 'Good';
            else message = 'Strong';
            
            const div = document.getElementById('password-strength') || document.createElement('div');
            div.id = 'password-strength';
            div.textContent = message;
            div.style.color = strength < 8 ? '#FF4444' : '#44FF44';
            this.parentNode.appendChild(div);
        });
    }
    
    if (confirm) {
        confirm.addEventListener('input', function() {
            if (this.value && this.value !== password.value) {
                this.style.borderColor = '#FF4444';
            } else {
                this.style.borderColor = 'rgba(255,215,0,0.3)';
            }
        });
    }
}

// ============================================
// YOUTUBE PREVIEW
// ============================================
function initYouTubePreview() {
    const input = document.getElementById('youtube_url');
    if (!input) return;
    
    input.addEventListener('input', function() {
        const url = this.value;
        const videoId = extractVideoId(url);
        
        let preview = document.getElementById('youtube-preview');
        if (!preview) {
            preview = document.createElement('div');
            preview.id = 'youtube-preview';
            this.parentNode.appendChild(preview);
        }
        
        if (videoId) {
            preview.innerHTML = `<img src="https://img.youtube.com/vi/${videoId}/hqdefault.jpg" style="width:100%; margin-top:0.5rem; border-radius:4px;">`;
        } else {
            preview.innerHTML = '';
        }
    });
}

// ============================================
// FORM VALIDATION
// ============================================
function initFormValidation() {
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            let valid = true;
            this.querySelectorAll('[required]').forEach(field => {
                if (!field.value.trim()) {
                    field.style.borderColor = '#FF4444';
                    valid = false;
                }
            });
            if (!valid) e.preventDefault();
        });
    });
}

// ============================================
// REMEMBER ME
// ============================================
function initRememberMe() {
    const remember = document.getElementById('remember');
    const email = document.getElementById('email');
    
    if (remember && email) {
        const saved = localStorage.getItem('rememberEmail');
        if (saved) {
            email.value = saved;
            remember.checked = true;
        }
        
        remember.addEventListener('change', function() {
            if (this.checked) {
                localStorage.setItem('rememberEmail', email.value);
            } else {
                localStorage.removeItem('rememberEmail');
            }
        });
    }
}

// ============================================
// SCROLL TO TOP
// ============================================
function initScrollToTop() {
    const btn = document.createElement('button');
    btn.id = 'scroll-top';
    btn.innerHTML = '↑';
    btn.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: #FFD700;
        color: #000;
        border: none;
        cursor: pointer;
        display: none;
        z-index: 9999;
    `;
    document.body.appendChild(btn);
    
    window.addEventListener('scroll', () => {
        btn.style.display = window.pageYOffset > 300 ? 'block' : 'none';
    });
    
    btn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// ============================================
// ADMIN SEARCH
// ============================================
function initAdminSearch() {
    document.querySelectorAll('.admin-table').forEach(table => {
        const input = document.createElement('input');
        input.type = 'text';
        input.placeholder = 'Search...';
        input.className = 'form-input';
        input.style.marginBottom = '1rem';
        input.style.maxWidth = '300px';
        
        table.parentNode.insertBefore(input, table);
        
        input.addEventListener('input', function() {
            const search = this.value.toLowerCase();
            table.querySelectorAll('tbody tr').forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(search) ? '' : 'none';
            });
        });
    });
}

// ============================================
// ADMIN CLOCK
// ============================================
function initRealtimeClock() {
    const clock = document.getElementById('realtime-clock');
    if (!clock) return;
    
    function update() {
        clock.textContent = new Date().toLocaleString();
    }
    update();
    setInterval(update, 1000);
}

// ============================================
// SPARKLE EFFECT
// ============================================
function initSparkleEffect() {
    // Disabled for performance
}

// ============================================
// LIVE CHAT
// ============================================
function initLiveChat() {
    const input = document.getElementById('chat-input');
    const button = document.querySelector('.chat-input .btn');
    const messages = document.getElementById('chat-messages');
    
    if (!input || !messages) return;
    
    function send() {
        const text = input.value.trim();
        if (!text) return;
        
        const div = document.createElement('div');
        div.className = 'chat-message';
        div.innerHTML = `<span class="chat-user">You:</span> <span class="chat-text">${escapeHtml(text)}</span>`;
        messages.appendChild(div);
        messages.scrollTop = messages.scrollHeight;
        input.value = '';
    }
    
    input.addEventListener('keypress', e => {
        if (e.key === 'Enter') send();
    });
    
    if (button) button.addEventListener('click', send);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ============================================
// LIVE STATUS
// ============================================
function checkLiveStatus() {
    if (!window.location.pathname.includes('/live')) return;
    
    setInterval(() => {
        fetch('/api/live/status')
            .then(r => r.json())
            .then(data => {
                const indicator = document.querySelector('.live-indicator');
                if (indicator) {
                    indicator.style.display = data.is_live ? 'flex' : 'none';
                }
            })
            .catch(() => {});
    }, 30000);
}

// ============================================
// RANDOM LOGIN PROMPTS
// ============================================
function initRandomLoginPrompts() {
    // Already defined above
}

// ============================================
// INITIALIZE ALL
// ============================================
setTimeout(() => {
    fixButtonVisibility();
}, 100);