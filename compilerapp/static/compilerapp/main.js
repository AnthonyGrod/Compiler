const csrftoken = Cookies.get('csrftoken');
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
  }
});

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

$(document).on('click', '#compile', function(e) {
    $.ajax({
        url: '/compilerapp/compile/',
        type: 'POST',
        data: {},
        success: function(data) {
            console.log("Success!");
            location.reload();
        }
    });});

$(document).on('click', '#blob', function(e) {
    // Get value on textarea with it="file-fragment"
    var blob = new Blob(document.getElementById('file-fragment').textContent);

    var link = document.createElement('a');
    link.download = "file.asm";
    link.href = window.URL.createObjectURL(blob);
    link.click();
    link.remove();
    window.url.revokeObjectURL(link.href);
});