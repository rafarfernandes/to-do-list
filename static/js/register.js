async function handleRegister(event) {
    event.preventDefault();  

    const username = document.getElementById('username').value;
    const password1 = document.getElementById('password1').value;
    const password2 = document.getElementById('password2').value;

    if (password1 !== password2) {
        alert("As senhas não coincidem. Tente novamente.");
        return;
    }

    const response = await fetch('/register/', {  
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password: password1 }),
    });

    if (response.ok) {
        const data = await response.json();
        alert("Cadastro realizado com sucesso!");
        window.location.href = '/login/';  
    } else {
        const errorData = await response.json();
        alert('Erro ao cadastrar: ' + errorData.detail);
    }
}

