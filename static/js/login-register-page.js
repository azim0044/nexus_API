window.onload = function() {
    var loginUsername = document.getElementById('input-login-username');
    var loginPassword = document.getElementById('input-login-password');
    var companyCode = document.getElementById('input-login-company-code');
    var signInButton = document.querySelector('#pills-login button[type="submit"]');

    var fullname = document.getElementById('input-fullname');
    var username = document.getElementById('input-username');
    var password = document.getElementById('input-password');
    var cpassword = document.getElementById('input-cpassword');
    var signUpButton = document.querySelector('#pills-register button[type="submit"]');
    var companyName = document.getElementById('input-register-company-name');
    var companyCode = document.getElementById('input-register-company-code');
    var companyCodeHidden = document.getElementById('input-register-company-code-hidden');

    var errorMessage = document.getElementById('errorMessage');


    function validateRegisterForm() {
        if (fullname.value && username.value && password.value && cpassword.value && companyName.value && companyCode.value && companyCodeHidden.value) {
            if (password.value === cpassword.value) {
                signUpButton.disabled = false;
                errorMessage.textContent = '';
            } else {
                signUpButton.disabled = true;
                errorMessage.textContent = 'Passwords do not match';
            }
        } else {
            signUpButton.disabled = true;
        }
    }

    loginUsername.addEventListener('input', validateLoginForm);
    loginPassword.addEventListener('input', validateLoginForm);

    fullname.addEventListener('input', validateRegisterForm);
    username.addEventListener('input', validateRegisterForm);
    password.addEventListener('input', validateRegisterForm);
    cpassword.addEventListener('input', validateRegisterForm);

    // Initial validation
    validateLoginForm();
    validateRegisterForm();
}