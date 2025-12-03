let today = new Date();
let min = new Date(today);
let max = new Date(today);
// podra reservar para el dia siguiente
min.setDate(today.getDate() + 1);
// y hasta 15 dias despues del dia siguiente
max.setDate(today.getDate() + 16);

const minStr = min.toISOString().split('T')[0];
const maxStr = max.toISOString().split('T')[0];
document.getElementById('fecha').setAttribute('min', minStr);
document.getElementById('fecha').setAttribute('max', maxStr);

const bookings = JSON.parse('{{ reservas | tojson | safe }}');

/* 
cuando el usuario selecciona una fecha en el calendario, esta variable cambia
a esa fecha para poder verificar si tiene reservas
*/
const options = document.getElementById('hora').options;
const validOptions = Array.from(options).filter((op) => op.value.length > 0);

function pickedTimes(date) {
    // devuelve los horarios no disponibles segun el dia
    return bookings
        .filter(b => b.fecha_servicio.split('T')[0] === date)
        .map(b => b.hora_servicio);
}

function isDateFull(date) {
    // vemos si todos los horarios del dia estan ocupados
    const bookedHours = pickedTimes(date);
    return validOptions.every(op => bookedHours.includes(op.value));
}

function nextAvailableDate(fromDate) {
    const maxDate = new Date(document.getElementById('fecha').getAttribute('max'));
    let checkDate = new Date(fromDate);
    checkDate.setDate(checkDate.getDate() + 1);

    while (checkDate <= maxDate) {
        const dateStr = checkDate.toISOString().split('T')[0];
        if (!isDateFull(dateStr)) {
            return dateStr;
        }
        checkDate.setDate(checkDate.getDate() + 1);
    }
    return null;
}

function display(dateStr) {
    const date = new Date(dateStr + 'T00:00:00');
    const opts = { weekday: 'long', day: 'numeric', month: 'long' };
    return date.toLocaleDateString('es-AR', opts);
}

document.getElementById('fecha').addEventListener('change', () => {
    /* 
    reseteamos las opciones para que todas esten disponibles antes 
    de invalidar las no disponibles
    */
    validOptions.forEach(op => {
        op.disabled = false;
        if (op.value) op.textContent = op.value;
    });

    const selectedDate = document.getElementById('fecha').value;
    bookings.forEach(booking => {
        if (booking.fecha_servicio.split('T')[0] === selectedDate) {
            validOptions.forEach((op) => {
                if (op.value === booking.hora_servicio) {
                    op.disabled = true;
                }
            });
        }
    });

    const allDisabled = validOptions.every((op) => op.disabled);
    if (allDisabled) {
        const nextAvailable = nextAvailableDate(selectedDate);
        if (nextAvailable) {
            const formattedDate = display(nextAvailable);
            alert(`El día seleccionado no tiene horarios disponibles.\n\nPróxima fecha disponible: ${formattedDate}`);
        } else {
            alert('El día seleccionado no tiene horarios disponibles.\n\nNo hay fechas disponibles en los próximos 15 días.');
        }
        document.getElementById('fecha').value = '';
        document.getElementById('hora').value = '';
    }
});

// manejamos el input de la direccion
document.getElementById('bookingForm').addEventListener('submit', function(e) {
    const addressInput = document.getElementById('direccion');
    const addressError = document.getElementById('addressError');
    
    if (addressInput.value.length < 5) {
        e.preventDefault();
        addressInput.style.borderColor = '#d32f2f';
        addressError.style.display = 'block';
        addressError.textContent = 'La dirección es muy corta.';
        return;
    }

    addressInput.style.borderColor = '#ccc';
    addressError.style.display = 'none';
});