// function to set a given theme/color-scheme
function setTheme(themeName) {
    localStorage.setItem('theme', themeName);
    document.documentElement.className = themeName;
}
// function to toggle between light and dark theme
function toggleTheme() {
   if (localStorage.getItem('theme') === 'theme-dark'){
       setTheme('theme-light');
   } else {
       setTheme('theme-dark');
   }
}
// Immediately invoked function to set the theme on initial load
(function () {
   if (localStorage.getItem('theme') === 'theme-dark') {
       setTheme('theme-dark');
   } else {
       setTheme('theme-light');
   }
})();

function displayTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tab");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}


function getCSRFToken() {
    var csrfCookie = document.cookie.match('(^|;)\\s*' + 'csrftoken' + '\\s*=\\s*([^;]+)');
    return csrfCookie ? csrfCookie.pop() : '';
}

function display_options(event, processor) {
    // Check the value of the 'processor' variable
    if (processor === 'MCS51') {
        // Display options for MCS51
        document.getElementById('options-container').innerHTML += `
            <form method="POST">
                <input type="hidden" name="csrfmiddlewaretoken" value="${getCSRFToken()}">
                <input type="checkbox" value="--model-small" name="procesor_options">--model-small<br>
                <input type="checkbox" value="--model-medium" name="procesor_options">--model-medium<br>
                <input type="checkbox" value="--model-large" name="procesor_options">--model-large<br>
                <input type="submit" value="Save">
            </form>
        `;
    } else if (processor === 'Z80') {
        // Display options for Z80
        document.getElementById('options-container').innerHTML += `
            <form method="POST">
                <input type="hidden" name="csrfmiddlewaretoken" value="${getCSRFToken()}">
                <input type="checkbox" value="--portmode=z80" name="procesor_options">--portmode=z80</option><br>
                <input type="checkbox" value="--portmode=z180" name="procesor_options">--portmode=z180</option><br>
                <input type="checkbox" value="--fno-omit-frame-pointer" name="procesor_options">--fno-omit-frame-pointer</option><br>
                <input type="submit" value="Save">
            </form>
        `;
    } else if (processor === 'STM8') {
        // Display options for STM8
        document.getElementById('options-container').innerHTML += `
            <form method="POST">
                <input type="hidden" name="csrfmiddlewaretoken" value="${getCSRFToken()}">
                <input type="checkbox" value="--model-medium" name="procesor_options">--model-medium<br>
                <input type="checkbox" value="--model-large" name="procesor_options">--model-large<br>
                <input type="submit" value="Save">
            </form>
        `;
    }
}
