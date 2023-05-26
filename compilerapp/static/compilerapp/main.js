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


function deleteCatalog(catalogId) {
    fetch(`/delete_catalog/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}',
        },
        body: JSON.stringify({ catalog_to_delete: catalogId }),
    })
}

function deleteFile(fileId) {
    fetch(`/delete_file/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}',
        },
        body: JSON.stringify({ file_to_delete: fileId }),
    })
}