async function handleLogin(event) {
    event.preventDefault(); 

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('error-message');

    const response = await fetch('/api/token/', {  // Certifique-se de que o endpoint está correto
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    });

    if (response.ok) {
        const data = await response.json();
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);
        window.location.href = '/tasks';  // Ajuste o redirecionamento para a página desejada
    } else {
        const errorData = await response.json();
        errorMessage.classList.remove('d-none');
        errorMessage.innerText = errorData.detail || 'Erro ao fazer login. Tente novamente.';
    }
}
