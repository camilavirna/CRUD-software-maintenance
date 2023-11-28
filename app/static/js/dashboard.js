document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('userForm');
    const cancelButton = document.getElementById('cancelButton');
    const updateButton = document.getElementById('updateButton');
    const backButton = document.getElementById('backButton');
    const visible = document.getElementById('togglePassword')
    const originalValues = {
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
        nome: document.getElementById('nome').value,
        telefone: document.getElementById('telefone').value
    };
    
    form.addEventListener('input', function() {
        const emailInput = document.getElementById('email');
        const passwordInput = document.getElementById('password');
        const nomeInput = document.getElementById('nome');
        const telefoneInput = document.getElementById('telefone');
        if (
            emailInput.value !== originalValues.email ||
            passwordInput.value !== originalValues.password ||
            nomeInput.value !== originalValues.nome ||
            telefoneInput.value !== originalValues.telefone
        ) {
            updateButton.removeAttribute('disabled');
            cancelButton.removeAttribute('disabled');
        } else {
            updateButton.setAttribute('disabled', 'true'); 
            cancelButton.setAttribute('disabled', 'true'); 
        }
    });

    cancelButton.addEventListener('click',function(){
        form.elements.email.value = originalValues.email;
        form.elements.password.value = originalValues.password;
        form.elements.nome.value = originalValues.nome;
        form.elements.telefone.value = originalValues.telefone;
        updateButton.setAttribute('disabled', 'true'); 
        cancelButton.setAttribute('disabled', 'true');  
    });

    backButton.addEventListener('click', function() {
        history.back();
    });

    visible.addEventListener('click',function(){
        const passwordInput = document.getElementById("password");
        const togglePasswordIcon = document.getElementById("togglePassword");
        
        passwordInput.type = passwordInput.type === "password" ? "text" : "password";
        
        togglePasswordIcon.innerHTML = passwordInput.type === "password" ? '<i class="fas fa-eye-slash"></i>' : '<i class="far fa-eye"></i>';
    });
});
