const flipcard = document.getElementById('flipCard');
const registerText = document.getElementById('Registertext');
const LoginText = document.getElementById('loginText');

registerText.addEventListener('click', () => {
    flipcard.style.transform = "rotateY(180deg)";
});

LoginText.addEventListener('click', () => {
    flipcard.style.transform = "rotateY(0deg)";
});
const boton = document.getElementById("Registertext");
const usuarioInputs = document.getElementById("inputsusuario");
const prestadorInputs = document.getElementById("inputsprestador");

boton.addEventListener("click", () => {
    // Preguntamos si es prestador o usuario
const esPrestador = confirm("¿Ofreces servicios? (Aceptar = Sí, Cancelar = No)");

    // Ocultar ambos antes de mostrar el que corresponda
usuarioInputs.classList.add("hidden");
prestadorInputs.classList.add("hidden");

if (esPrestador) {
      // Mostrar campos de prestador
  prestadorInputs.classList.remove("hidden");
} else {
  // Mostrar campos de usuario
  usuarioInputs.classList.remove("hidden");
}

    // Cambiamos el texto del botón para enviar el formulario
  });