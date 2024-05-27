let active_win = null;
let active_z_ind = 10;

let navbar = document.querySelector(".navbar");
let windows = document.querySelectorAll(".window");

(function() {
    windows.forEach((win) => {
        window_init(win);
    });
})();

function window_init(element) {
    let has_moved = false;
    let pos_x = element.offsetLeft;
    let pos_y = element.offsetTop;

    element.style.zIndex = active_z_ind++;

    element.style.top = element.offsetTop + "px";
    element.style.left = element.offsetLeft + "px";
    element.style.margin = 0;

    let header = element.querySelector(".window-title");
    header.onmousedown = mouse_down;

    element.onmousedown = focus;

    function mouse_down(event) {
        event.preventDefault();

        has_moved = false;
        pos_x = event.clientX;
        pos_y = event.clientY;

        document.onmouseup = mouse_up;
        document.onmousemove = mouse_move;
    }

    function mouse_move(event) {
        event.preventDefault();

        let new_y = element.offsetTop - (pos_y - event.clientY);
        let new_x = element.offsetLeft - (pos_x - event.clientX);

        has_moved = true;
        element.style.top = new_y + "px";
        element.style.left = new_x + "px";

        pos_x = event.clientX;
        pos_y = event.clientY;
    }

    function mouse_up() {
        if (has_moved) {
            let max_width = window.innerWidth - element.clientWidth;
            let max_height = window.innerHeight - element.clientHeight - navbar.clientHeight;

            let top = parseInt(element.style.top);
            element.style.top = Math.min(Math.max(top, 0), max_height) + "px";

            let left = parseInt(element.style.left);
            element.style.left = Math.min(Math.max(left, 0), max_width) + "px";
        }

        document.onmouseup = null;
        document.onmousemove = null;
    }

    function focus() {
        windows.forEach((win) => {
            win.classList.remove("window-focused");

            if (win.style.zIndex > element.style.zIndex)
                win.style.zIndex--;
        });

        element.style.zIndex = active_z_ind;

        element.classList.add("window-focused");
        active_win = element;
    }
}
