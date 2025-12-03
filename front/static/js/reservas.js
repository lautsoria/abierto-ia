function openModal(modalId) {
            const modal = document.getElementById(modalId);
            modal.classList.add('active');
        }

        function closeModal(modalId) {
            const modal = document.getElementById(modalId);
            modal.classList.remove('active');
        }

        function closeModalOnOutsideClick(event, modalId) {
            if (event.target.id === modalId) {
                closeModal(modalId);
            }
        }