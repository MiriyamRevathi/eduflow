// EduFlow Theme Switcher Module
document.addEventListener('DOMContentLoaded', () => {
    const themeBtn = document.getElementById('theme-toggle-btn');
    const htmlElem = document.documentElement;

    const savedTheme = localStorage.getItem('eduflow_theme') || 'light';
    htmlElem.setAttribute('data-theme', savedTheme);

    if (themeBtn) {
        themeBtn.addEventListener('click', () => {
            const currentTheme = htmlElem.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            htmlElem.setAttribute('data-theme', newTheme);
            localStorage.setItem('eduflow_theme', newTheme);
        });
    }
});
