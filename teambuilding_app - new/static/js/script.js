// Scroll Animation for Navigation Links
document.querySelectorAll('.nav a').forEach(link => {
    link.addEventListener('click', (event) => {
        const href = link.getAttribute('href');

        // Проверка дали линкът е за секция на същата страница
        if (href && href.startsWith('#')) {
            event.preventDefault();
            const targetId = href.substring(1);
            const targetSection = document.getElementById(targetId);

            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        }
    });
});

// Button Action for "Explore Now"
document.getElementById('cta-button').addEventListener('click', () => {
    const categoriesSection = document.getElementById('categories');
    categoriesSection.scrollIntoView({
        behavior: 'smooth'
    });
});

// Highlight Active Navigation Link on Scroll
window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.nav a');
    let currentSection = '';

    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        if (window.scrollY >= sectionTop - 60) {
            currentSection = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href').substring(1) === currentSection) {
            link.classList.add('active');
        }
    });
});

// Dynamic Footer Year Update
const footerYear = document.querySelector('.footer p');
footerYear.innerHTML = `&copy; ${new Date().getFullYear()} Adventure Teambuilding. All Rights Reserved.`;

// Category Button Interactivity
const categoryButtons = document.querySelectorAll('.category-button');
categoryButtons.forEach(button => {
    button.addEventListener('click', () => {
        alert('Feature not implemented yet. Stay tuned!');
    });
});


