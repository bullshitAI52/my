document.addEventListener('DOMContentLoaded', () => {
    // Add smooth reveal animation to sections
    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Initial state for sections
    document.querySelectorAll('section').forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(20px)';
        section.style.transition = 'all 0.6s ease-out';
        observer.observe(section);
    });

    // Handle contact link clicks
    document.querySelectorAll('.contact-item a').forEach(link => {
        link.addEventListener('click', (e) => {
            // Log interaction or handle analytics if needed
            console.log(`Contact link clicked: ${link.getAttribute('href')}`);
        });
    });
});
