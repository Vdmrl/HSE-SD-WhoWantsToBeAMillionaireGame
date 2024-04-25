document.getElementById("continueBtn").addEventListener("click", function () {
    var username = document.getElementById("username").value;
    window.location.href = "http://127.0.0.1:8000/" + username;
});
