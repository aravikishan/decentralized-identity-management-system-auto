document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelectorAll('nav a');
    const currentPath = window.location.pathname;

    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    const mobileToggle = document.querySelector('.mobile-toggle');
    if (mobileToggle) {
        mobileToggle.addEventListener('click', () => {
            document.querySelector('nav').classList.toggle('open');
        });
    }

    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', event => {
            const inputs = form.querySelectorAll('input[required]');
            let valid = true;
            inputs.forEach(input => {
                if (!input.value) {
                    valid = false;
                    input.classList.add('is-invalid');
                } else {
                    input.classList.remove('is-invalid');
                }
            });
            if (!valid) {
                event.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });

    const smoothScrollLinks = document.querySelectorAll('a[href^="#"]');
    smoothScrollLinks.forEach(link => {
        link.addEventListener('click', event => {
            event.preventDefault();
            document.querySelector(link.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});