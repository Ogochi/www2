function onLogin() {
    window.localStorage.setItem("username", $('#login_username').val());
    window.localStorage.setItem("password", $('#login_password').val());
}

$().ready(() => {
    $('#login_button').click(onLogin);
});