// cuando ver mas es clickeado, se agrega la clase open y se saca al clickear de nuevo
// pues por defecto el panel tiene altura 0
function toggleDetails(id) {
    const panel = document.getElementById(`details-${id}`);
    panel.classList.toggle('open');
}
