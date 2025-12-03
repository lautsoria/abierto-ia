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

    // validamos que los datos tengan sentido
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
    });