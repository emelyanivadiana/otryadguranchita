function openModal(card) {
    console.log('Открываем модальное окно'); // Для отладки

    // Получаем данные из карточки
    const imgSrc = card.querySelector('img').src;
    const title = card.querySelector('h3').textContent;
    const fullText = card.querySelector('.full-text').innerHTML;

    // Заполняем модальное окно
    document.getElementById('modal-img').src = imgSrc;
    document.getElementById('modal-title').textContent = title;
    document.getElementById('modal-text').innerHTML = fullText;

    // Показываем модальное окно
    document.getElementById('modal').style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

// Закрыть модальное окно
function closeModal() {
    document.getElementById('modal').style.display = 'none';
    document.body.style.overflow = 'auto';
}

// Закрыть при клике вне окна
document.getElementById('modal').addEventListener('click', function(e) {
    if (e.target === this) {
        closeModal();
    }
});

// Закрыть по ESC
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeModal();
    }
});