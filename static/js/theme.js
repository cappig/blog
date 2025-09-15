let saved_theme = localStorage.getItem('theme');

if (saved_theme) {
    document.documentElement.setAttribute('data-theme', saved_theme);
} else {
    const prefers_dark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const default_theme = prefers_dark ? 'dark' : 'light';

    document.documentElement.setAttribute('data-theme', default_theme);
}


function toggle_theme() {
    const current_theme = document.documentElement.getAttribute('data-theme');
    const new_theme = current_theme === 'dark' ? 'light' : 'dark';

    document.documentElement.setAttribute('data-theme', new_theme);
    localStorage.setItem('theme', new_theme);
}
