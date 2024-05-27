let clock = document.querySelector(".navbar-tray-clock");

(function() {
    set_time();
})();

function add_leading_zero(i) {
    if (i < 10) { i = "0" + i };
    return i;
}

function set_time() {
    const today = new Date();
    let h = add_leading_zero(today.getHours());
    let m = add_leading_zero(today.getMinutes());
    let s = add_leading_zero(today.getSeconds());

    clock.innerHTML = h + ":" + m + ":" + s;
    setTimeout(set_time, 1000);
}

