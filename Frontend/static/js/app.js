document.getElementById('btnCalcular').addEventListener('click', async (e) => {
    e.preventDefault();
    const textoUsuario = document.getElementById('textoUsuario').value.trim();
    const btn = document.getElementById('btnCalcular');
    const loading = document.getElementById('loading');
    const resultados = document.getElementById('resultados');
    const listaAlimentos = document.getElementById('listaAlimentos');
    const totalCaloriasSpan = document.getElementById('totalCalorias');

    if (!textoUsuario) {
        alert('Por favor, escribe los alimentos que consumiste.');
        return;
    }

    // Interfaz en modo de carga
    btn.disabled = true;
    loading.classList.remove('hidden');
    resultados.classList.add('hidden');
    listaAlimentos.innerHTML = '';

    try {
        // Hacemos el Fetch real a nuestro Backend en FastAPI
        const response = await fetch('http://127.0.0.1:8000/calculator/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ texto_usuario: textoUsuario })
        });

        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor backend.');
        }

        

        const data = await response.json();

        // Inyectamos el total de calorías calculado matemáticamente
        totalCaloriasSpan.textContent = data.total_calorias;

        // Iteramos el desglose estructurado para pintar las tarjetas HTML
        data.desglose.forEach(item => {
            const itemCaloriasReales = Math.round((item.calorias_por_100g / 100) * item.gramos);
            
            const card = document.createElement('div');
            card.className = 'food-item-card';
            card.innerHTML = `
                <div class="food-header">
                    <strong>${item.alimento.toUpperCase()}</strong> 
                    <span>${item.gramos}g ➔ <strong>${itemCaloriasReales} kcal</strong></span>
                    
                </div>
                <p class="food-seo-text">${item.dato_educativo}</p>
                <small class="base-info">Valor base: ${item.calorias_por_100g} kcal por cada 100g.</small>
            `;
            listaAlimentos.appendChild(card);
        });

        // Mostramos la sección de resultados limpios
        resultados.classList.remove('hidden');

    } catch (error) {
        console.error('Error:', error);
        alert('Hubo un problema al conectar con el servidor de NutriIA.');
    } finally {
        // Restauramos el botón
        btn.disabled = false;
        loading.classList.add('hidden');
    }
});