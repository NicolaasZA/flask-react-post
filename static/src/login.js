function setLoginMessage(text) {
    if (text) {
        document.getElementById('loginMessage').innerText = text;
    } else {
        document.getElementById('loginMessage').innerHTML = '&nbsp;';
    }
}

function setSignupMessage(text) {
    if (text) {
        document.getElementById('signupMessage').innerText = text;
    } else {
        document.getElementById('signupMessage').innerHTML = '&nbsp;';
    }
}

function getSignupType() {
    if (document.getElementById('typeString1').checked) { return 0; }
    else if (document.getElementById('typeString2').checked) { return 1; }
    return 0;
}

function onSignupSubmit(event) {
    const email = document.getElementById('signupEmail').value;
    const signupType = getSignupType();
    const password = document.getElementById('signupPass').value || '';

    axios.post('http://192.168.221.62:80/signup', {
        username: email,
        password: password,
        type: signupType
    })
        .then(function (response) {
            // handle success
            console.log(response.data);

            if (!response.data.success) {
                document.getElementById('loginPass').value = '';
            } else {
                sessionStorage.setItem('userToken', response.data.data.user.id + '|' + response.data.data.user.token);
                window.location.href = 'dashboard.html';
            }

            setSignupMessage(response.data.message);
            setLoginMessage('');
        })
        .catch(function (error) {
            // handle error
            console.error(error);
            setSignupMessage(error);
            setLoginMessage('');
        });
}


function onLoginSubmit(event) {
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPass').value || '';

    axios.post('http://192.168.221.62:80/login', {
        username: email,
        password: password
    })
        .then(function (response) {
            // handle success
            console.log(response.data);

            if (!response.data.success) {
                document.getElementById('loginPass').value = '';
            } else {
                sessionStorage.setItem('userToken', response.data.data.user.id + '|' + response.data.data.user.token);
                window.location.href = 'dashboard.html';
            }

            setLoginMessage(response.data.message);
            setSignupMessage('');
        })
        .catch(function (error) {
            // handle error
            console.error(error);
            setLoginMessage(error);
            setSignupMessage('');
        });
}