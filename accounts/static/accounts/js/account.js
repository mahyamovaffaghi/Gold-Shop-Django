function togglePasswordLogin() {
    var passwordInputLogin = document.getElementById("passwordInputLogin");
    if (passwordInputLogin.type === "password") {
      passwordInputLogin.type = "text";
    } else {
      passwordInputLogin.type = "password";
    }
  }
  function togglePasswordReg1() {
    var passwordInputReg1 = document.getElementById("passwordInputReg1");
    if (passwordInputReg1.type === "password") {
      passwordInputReg1.type = "text";
    } else {
      passwordInputReg1.type = "password";
    }
  }
  function togglePasswordReg2() {
    var passwordInputReg2 = document.getElementById("passwordInputReg2");
    if (passwordInputReg2.type === "password") {
      passwordInputReg2.type = "text";
    } else {
      passwordInputReg2.type = "password";
    }
  }
  


  document.addEventListener("DOMContentLoaded", function () {
    const container = document.querySelector('.container'); 
    const registerBtn = document.getElementById('register');
    const loginBtn = document.getElementById('login');

    registerBtn.addEventListener('click', () => {
        container.classList.add("active");
    });

    loginBtn.addEventListener('click', () => {
        container.classList.remove("active");
    });
});



