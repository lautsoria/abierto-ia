function updatePreview() {
    const nombre = document.getElementById('nombre').value;
    const categoria = document.getElementById('categoria_id');
    const categoriaText = categoria.options[categoria.selectedIndex]?.text || 'Categoría';
    const descripcion = document.getElementById('descripcion').value;
    const precio = document.getElementById('precio').value;
    const duracion = document.getElementById('duracion').value;
    const horaInicio = document.getElementById('hora_inicio').value;
    const horaFin = document.getElementById('hora_fin').value;

    document.getElementById('previewTitle').textContent =
        nombre || 'Nombre del servicio';
    document.getElementById('previewCategory').textContent =
        categoriaText !== 'Seleccioná una categoría'
        ? categoriaText
        : 'Categoría';
    document.getElementById('previewDescription').textContent =
        descripcion
            ? descripcion.substring(0, 80) + (descripcion.length > 80 ? '...' : '')
            : 'Descripción del servicio...';
    document.getElementById('previewPrice').textContent =
        precio ? '$ ' + Number(precio).toLocaleString('es-AR') : '$ 0';
    document.getElementById('previewDuration').textContent =
        duracion ? duracion + 'h' : '0h';
    if (horaInicio && horaFin) {
        document.getElementById('previewSchedule').textContent =
            `${horaInicio.padStart(2, '0')}:00 - ${horaFin.padStart(2, '0')}:00`;
    }
}

function confirmarEliminacion() {
    const eliminarURL = this.getAttribute('data-url');
    if (confirm('¿Estás seguro de que querés eliminar este servicio? Esta acción no se puede deshacer.')) {
        window.location.href = eliminarURL;
    }
}

function cancelar() {
    const cancelarURL = this.getAttribute('data-url');
    window.location.href = cancelarURL;
}

// Inicializar cuando el DOM carga
document.addEventListener('DOMContentLoaded', function() {
    // Actualizar preview inicial
    updatePreview();
    
    // Event listeners para actualizar preview en tiempo real
    const formInputs = ['nombre', 'categoria_id', 'descripcion', 'precio', 'duracion', 'hora_inicio', 'hora_fin'];
    formInputs.forEach(function(id) {
        const element = document.getElementById(id);
        if (element) {
            element.addEventListener('input', updatePreview);
            element.addEventListener('change', updatePreview);
        }
    });
    
    // Event listener para el botón de eliminar
    const btnEliminar = document.getElementById('btnEliminar');
    if (btnEliminar) {
        btnEliminar.addEventListener('click', confirmarEliminacion);
    }
    
    // Event listener para el botón de cancelar
    const btnCancelar = document.getElementById('btnCancelar');
    if (btnCancelar) {
        btnCancelar.addEventListener('click', cancelar);
    }
});