const flipcard = document.getElementById('flipCard');
const registerText = document.getElementById('Registertext');
const LoginText = document.getElementById('loginText');

registerText.addEventListener('click', () => {
    flipcard.style.transform = "rotateY(180deg)";
});

LoginText.addEventListener('click', () => {
    flipcard.style.transform = "rotateY(0deg)";
});