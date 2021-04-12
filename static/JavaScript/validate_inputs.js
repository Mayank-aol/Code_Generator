$('document').ready(function () {
    var x = document.forms["SignIn"]["username"].value;
    if (x == "") {
        alert("UserName Cant be Blank");
        return false;
    }
});