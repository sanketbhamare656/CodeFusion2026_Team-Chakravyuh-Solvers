// PhishNet Consolidated JavaScript Logic

// Toggle Navbar on Mobile
function toggleNavbar() {
    const navLinks = document.querySelector('.nav-links');
    if (navLinks) {
        navLinks.classList.toggle('show');
    }
}

// Global Preloader and Mobile Navigation events
document.addEventListener("DOMContentLoaded", function () {
    // 1. Mobile Menu Link closing behavior
    const navLinks = document.querySelector('.nav-links');
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth <= 768 && navLinks) {
                navLinks.classList.remove('show');
            }
        });
    });

    // 2. Preloader logic
    const preloader = document.getElementById("preloader");
    const contentWrap = document.querySelector(".content-wrap");
    
    if (preloader && contentWrap) {
        if (!sessionStorage.getItem("preloaderDisplayed")) {
            const strings = [
                "Initializing request...",
                "Resolving internet address 127.0.0.1",
                "Requesting access to server",
                "Entering credentials",
                "Login denied",
                "Re-entering credentials",
                "Access granted",
                "Finding PhishNet backend services",
                "Services found on port 80",
                "Starting services...",
                "Checking hardware changes...",
                "Applying security updates...",
                "Bringing up network interface...",
                "Connecting to database...",
                "Fetching data...",
                "Processing DOM...",
                "Loading images...",
                "Rendering page...",
                "WELCOME TO PhishNet - Your Cyber Guardian!"
            ];

            let count = 0;
            const delay = 350; // slightly faster animation for better UX

            function addLog() {
                const logContainer = document.getElementById("log-container");
                if (logContainer && count < strings.length) {
                    const row = document.createElement("div");
                    row.style.color = "#fff";
                    row.style.fontFamily = "monospace";
                    row.style.padding = "5px";
                    row.innerHTML = `<span style="color: #00f0ff">[OK]</span> ${strings[count]}`;
                    logContainer.appendChild(row);
                    logContainer.scrollTop = logContainer.scrollHeight;

                    count++;
                    setTimeout(addLog, delay);
                } else {
                    setTimeout(() => {
                        preloader.style.opacity = '0';
                        preloader.style.transition = 'opacity 0.5s ease';
                        setTimeout(() => {
                            preloader.style.display = "none";
                            contentWrap.style.display = "flex";
                        }, 500);
                        sessionStorage.setItem("preloaderDisplayed", "true");
                    }, 800);
                }
            }

            addLog();
        } else {
            // Hide preloader immediately if already displayed in this session
            preloader.style.display = "none";
            contentWrap.style.display = "flex";
        }
    }

    // 3. Initialize Particles.js (if particle div and library are loaded)
    if (document.getElementById("particles-js") && typeof particlesJS !== "undefined") {
        particlesJS("particles-js", {
            particles: {
                number: { value: 80, density: { enable: true, value_area: 800 } },
                color: { value: "#00f0ff" },
                shape: {
                    type: "circle",
                    stroke: { width: 0, color: "#000000" },
                    polygon: { nb_sides: 5 },
                },
                opacity: { value: 0.5, random: true, anim: { enable: true, speed: 1, opacity_min: 0.1 } },
                size: { value: 3, random: true, anim: { enable: true, speed: 40, size_min: 0.1 } },
                line_linked: {
                    enable: true,
                    distance: 150,
                    color: "#00f0ff",
                    opacity: 0.4,
                    width: 1
                },
                move: {
                    enable: true,
                    speed: 4,
                    direction: "none",
                    random: false,
                    straight: false,
                    out_mode: "out",
                    bounce: false,
                    attract: { enable: false, rotateX: 600, rotateY: 1200 }
                }
            },
            interactivity: {
                detect_on: "canvas",
                events: {
                    onhover: { enable: true, mode: "repulse" },
                    onclick: { enable: true, mode: "push" },
                },
                modes: {
                    repulse: { distance: 100, duration: 0.4 },
                    push: { particles_nb: 4 }
                }
            },
            retina_detect: true
        });
    }

    // 4. Shared Animation on Scroll behavior for cards
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.feature-card, .team-card, .testimonial-card, .manual-card, .news-card');

        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.3;

            if (elementPosition < screenPosition) {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }
        });
    };

    // Set initial state for animated elements
    document.querySelectorAll('.feature-card, .team-card, .testimonial-card, .manual-card, .news-card').forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'all 0.6s ease';
    });

    // Run once on page load
    animateOnScroll();

    // Run on scroll
    window.addEventListener('scroll', animateOnScroll);
});
