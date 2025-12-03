document.getElementById('nombre').addEventListener('input', function() {
        document.getElementById('nombreCount').textContent = this.value.length;
        document.getElementById('previewNombre').textContent = this.value || 'Nombre del servicio';
    });

    document.getElementById('descripcion').addEventListener('input', function() {
        document.getElementById('descripcionCount').textContent = this.value.length;
    });

    document.getElementById('precio').addEventListener('input', function() {
        const precio = parseFloat(this.value) || 0;
        document.getElementById('previewPrecio').textContent = precio.toLocaleString('es-AR');
    });


    document.getElementById('categoria').addEventListener('change', function() {
        const selected = this.options[this.selectedIndex];
        document.getElementById('previewCategoria').textContent = selected.text || 'Categoría';
    });


    function updateSchedulePreview() {
        const inicio = document.getElementById('hora_inicio').value;
        const fin = document.getElementById('hora_fin').value;
        const duracion = document.getElementById('duracion').value;
        
        if (inicio && fin) {
            document.getElementById('previewHorario').textContent = 
                `${inicio.padStart(2, '0')}:00 a ${fin.padStart(2, '0')}:00`;
        }
        
        if (duracion) {
            document.getElementById('previewDuracion').textContent = duracion;
        }
    }

    document.getElementById('hora_inicio').addEventListener('change', updateSchedulePreview);
    document.getElementById('hora_fin').addEventListener('change', updateSchedulePreview);
    document.getElementById('duracion').addEventListener('change', updateSchedulePreview);

    document.getElementById('hora_fin').addEventListener('change', function() {
        const inicio = parseInt(document.getElementById('hora_inicio').value);
        const fin = parseInt(this.value);
        
        if (inicio && fin && fin <= inicio) {
            alert('La hora de fin debe ser posterior a la hora de inicio');
            this.value = '';
        }
    });

    document.getElementById('duracion').addEventListener('change', function() {
        const inicio = parseInt(document.getElementById('hora_inicio').value);
        const fin = parseInt(document.getElementById('hora_fin').value);
        const duracion = parseInt(this.value);
        
        if (inicio && fin && duracion) {
            const rangoDisponible = fin - inicio;
            if (duracion > rangoDisponible) {
                alert(`La duración (${duracion}h) no puede ser mayor al rango horario disponible (${rangoDisponible}h)`);
                this.value = '';
            }
        }
    });

    const MAX_BARRIOS = 3;
    let selectedBarrios = [];

    const barrioSelect = document.getElementById('barrioSelect');
    const selectedBarriosContainer = document.getElementById('selectedBarrios');
    const barriosPlaceholder = document.getElementById('barriosPlaceholder');
    const barriosCount = document.getElementById('barriosCount');
    const barriosInputs = document.getElementById('barriosInputs');
    const barriosHelp = document.getElementById('barriosHelp');

    function updateBarriosUI() {
        
        barriosCount.textContent = selectedBarrios.length;
        
        // actualiza el barios seleccionados
        barriosPlaceholder.style.display = selectedBarrios.length === 0 ? 'block' : 'none';
        
        // verificamos que no se pueda agregar mas de 3 barrios
        if (selectedBarrios.length >= MAX_BARRIOS) {
            barrioSelect.disabled = true;
            barriosHelp.textContent = 'Máximo de barrios alcanzado';
            barriosHelp.style.color = '#d32f2f';
        } else {
            barrioSelect.disabled = false;
            barriosHelp.textContent = `Podés seleccionar hasta ${MAX_BARRIOS - selectedBarrios.length} barrio${MAX_BARRIOS - selectedBarrios.length !== 1 ? 's' : ''} más`;
            barriosHelp.style.color = '#666';
        }

        // actualizamos los inputs escondidos
        barriosInputs.innerHTML = '';
        selectedBarrios.forEach(barrio => {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'barrios[]';
            input.value = barrio.id;
            barriosInputs.appendChild(input);
        });
    }


    function addBarrio(id, nombre) {
        if (selectedBarrios.length >= MAX_BARRIOS) return;
        if (selectedBarrios.find(b => b.id === id)) return;

        selectedBarrios.push({ id, nombre });

        // los barrios que seleccionamos aparecen en la barra de arriba
        const tag = document.createElement('span');
        tag.className = 'barrio-tag';
        tag.dataset.id = id;
        tag.innerHTML = `
            ${nombre}
            <button type="button" class="remove-barrio" title="Quitar barrio">&times;</button>
        `;

        tag.querySelector('.remove-barrio').addEventListener('click', () => removeBarrio(id));
        selectedBarriosContainer.appendChild(tag);

        // deshabilitamos el barrio seleccionado
        const option = barrioSelect.querySelector(`option[value="${id}"]`);
        if (option) option.disabled = true;

        updateBarriosUI();
    }

    // borramos el barrio de la barra de seleccionados
    function removeBarrio(id) {
        selectedBarrios = selectedBarrios.filter(b => b.id !== id);

        const tag = selectedBarriosContainer.querySelector(`[data-id="${id}"]`);
        if (tag) tag.remove();

        const option = barrioSelect.querySelector(`option[value="${id}"]`);
        if (option) option.disabled = false;

        updateBarriosUI();
    }

    barrioSelect.addEventListener('change', function() {
        const selectedOption = this.options[this.selectedIndex];
        if (selectedOption.value) {
            addBarrio(selectedOption.value, selectedOption.dataset.nombre);
            this.value = ''; // Reset select
        }
    });

    document.getElementById('serviceForm').addEventListener('submit', function(e) {
        const inicio = parseInt(document.getElementById('hora_inicio').value);
        const fin = parseInt(document.getElementById('hora_fin').value);
        const duracion = parseInt(document.getElementById('duracion').value);
        const precio = parseFloat(document.getElementById('precio').value);

        if (fin <= inicio) {
            e.preventDefault();
            alert('La hora de fin debe ser posterior a la hora de inicio');
            return;
        }

        if (duracion > (fin - inicio)) {
            e.preventDefault();
            alert('La duración del turno no puede ser mayor al rango horario');
            return;
        }

        if (precio < 100) {
            e.preventDefault();
            alert('El precio mínimo es $100');
            return;
        }

        if (selectedBarrios.length === 0) {
            e.preventDefault();
            alert('Debés seleccionar al menos un barrio');
            return;
        }
    });