const $ = id => document.getElementById(id)

const flipcard = document.getElementById('flipCard');
const registerText = document.getElementById('Registertext');
const LoginText = document.getElementById('loginText');

registerText.addEventListener('click', () => {
    flipcard.style.transform = "rotateY(180deg)";
});

LoginText.addEventListener('click', () => {
    flipcard.style.transform = "rotateY(0deg)";
});

// flow para registrar y loguear un usuario

// register
const registerForm = $("registerForm")
registerForm.addEventListener('submit', async (e) => {
    e.preventDefault()
    const user = $("newUser")
    const email = $("email")
    const password = $("newPassword")
    const repeatPassword = $("newPassword2")
    const registerMessage = $("registerMessage")
    const checkbox = $("isProveedor")
    
    if (password.value !== repeatPassword.value) {
        registerMessage.innerText = 'Passwords do not match'
        registerMessage.style.color = 'red'
        return        
    }
    
    // enviamos un POST a la api para registrar al usuario.
    // lo hacemos de esta forma porque front y back se encuentran en 2 puertos separados
    const req_body = JSON.stringify({ user: user.value, email: email.value, password: password.value, provider: checkbox.checked })
    console.log(req_body)
    
    const register = await fetch('http://localhost:5500/auth/register', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json'
        },
        credentials: 'include',
        body: req_body
    })

    if (!register.ok) {
        registerMessage.innerText = `Error al registrar el usuario`
        registerMessage.style.color = 'red'
        return           
    }

    registerMessage.innerText = 'Usuario creado, Iniciar sesión!'
    registerMessage.style.color = 'green'
    setTimeout(() => {
        flipcard.style.transform = "rotateY(0deg)";
    }, 2000)       
})

// login
const loginForm = document.getElementById("loginForm")

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault()
    const credential = document.getElementById('credential')
    const loginPassword = document.getElementById('password')
    const loginMessage = document.getElementById("loginMessage")

    // enviamos un POST a la api para registrar al usuario.
    // lo hacemos de esta forma porque front y back se encuentran en 2 puertos separados
    const login = await fetch('http://localhost:5500/auth/login', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify({ credential: credential.value, password: loginPassword.value })
    })

    if (!login.ok) {
        loginMessage.innerText = `Credenciales inválidas`
        loginMessage.style.color = 'red'
        return           
    }

    // no debemos pasar la cookie ya que el backend se encarga de meterla
    loginMessage.innerText = 'Iniciando sesión...'
    loginMessage.style.color = 'green'
    setTimeout(() => {
        window.location.href = '/'
    }, 1000)
})


