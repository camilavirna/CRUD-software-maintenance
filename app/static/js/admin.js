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

$(document).ready(function() {
    $('#userTable').DataTable({
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.10.24/i18n/Portuguese-Brasil.json"
        }
    });
    
    $('.editUser').on('click', function() {
        const row = $(this).closest('tr');
    
        // Tornar as células editáveis clicáveis
        row.find('.editable').attr('contenteditable', true);
    
        // Adicionar classe de destaque às células editáveis
        row.find('.editable').addClass('editing');
    
        // Alterar o texto do link para 'Salvar'
        $(this).text('Salvar');
    
        // Armazenar a referência à linha
        const currentRow = row;
    
        // Remover o link de edição após clicar
        $(this).off('click').on('click', function() {
            // Tornar as células não editáveis
            currentRow.find('.editable').attr('contenteditable', false);
    
            // Remover classe de destaque
            currentRow.find('.editable').removeClass('editing');
    
            // Restaurar o texto original do link
            $(this).text('Editar');
    
            // Criar um objeto para armazenar os dados editados
           const editedData = {};
    
            // Obter o ID do usuário (substitua 'userId' pelo nome do atributo de dados que contém o ID)
            const userId = currentRow.find('td:eq(3)').text();

            // Percorrer cada célula editável na linha
            currentRow.find('.editable').each(function() {
                const columnName = $(this).data('field');  // Corrigido para 'data-field'
                const cellValue = $(this).text();
                editedData[columnName] = cellValue;
            });
    
            // Enviar os dados editados para o servidor usando AJAX (exemplo)

            $.ajax({
                type: 'PUT',
                url: 'http://127.0.0.1:5001/user/' + userId,  // Inclua o ID do usuário na URL
                data: JSON.stringify(editedData),
                contentType: 'application/json',
                success: function(response) {
                    // Lidar com a resposta do servidor, se necessário
                    console.log('Dados atualizados com sucesso:', response);
                },
                error: function(error) {
                    // Lidar com erros, se houver
                    console.error('Erro ao atualizar dados:', error);
                }
            });
        });
    });
});
