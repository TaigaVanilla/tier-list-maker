/**
 * Fix header on scroll
 */
window.onscroll = function () {
    const scroll_position = window.pageYOffset;
    const header = document.getElementById('header');
    if (scroll_position === 0) {
        header.style.borderBottom = 'none';
    } else {
        header.style.borderBottom = '1px solid whitesmoke';
    }
};
