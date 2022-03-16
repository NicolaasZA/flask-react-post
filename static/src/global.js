function logout() {
    sessionStorage.clear();
    window.location.href = 'login.html';
}


function showUserFields(user) {
    document.getElementById('phUserName').innerText = user.name;
}