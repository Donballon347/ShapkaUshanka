const socket = io();
const chat = document.getElementById('chat');
const inputContainer = document.getElementById('input-container');

const filterOrder = ['categories', 'gender', 'season', 'ears', 'material', 'composition', 'ties', 'size'];
let currentFilterIndex = 0;

// Функция для отображения сообщений в чате
function appendMessage(sender, text) {
    const div = document.createElement('div');
    div.className = 'message ' + sender;
    div.textContent = (sender === 'user' ? 'Вы: ' : 'Бот: ') + text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

// Обработка сообщений от бота
// В обработке 'bot-message', если есть идентификаторы товаров, они будут добавляться в сообщения:
socket.on('bot-message', (message) => {
    const div = document.createElement('div');
    div.className = 'message bot';
    div.innerHTML = message; // Уже содержит кнопку
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;  // Прокрутка вниз
});

// Обработка кнопок с опциями фильтров
socket.on('filter-options', (options) => {
    const buttons = options.map(option => `<button onclick="selectFilter('${option}')">${option}</button>`).join(' ');
    const div = document.createElement('div');
    div.className = 'message bot';
    div.innerHTML = buttons;
    chat.appendChild(div);
});

function selectFilter(selection) {
    appendMessage('user', selection);

    if (selection === "Подобрать по фильтрам") {
        inputContainer.classList.add('hidden');  // Скрыть строку ввода
        currentFilterIndex = 0;  // Сбрасываем индекс фильтра
        user_filters = {};  // Очищаем предыдущие фильтры
        socket.emit('filter-selection', { filter_type: 'start_filters', selection: selection });
    } else if (selection === "Найти товар по поиску") {
        inputContainer.classList.remove('hidden');  // Показать строку ввода
        socket.emit('filter-selection', { filter_type: 'start_search', selection: selection });
    } else {
        const currentFilter = filterOrder[currentFilterIndex];
        socket.emit('filter-selection', { filter_type: currentFilter, selection: selection });
        currentFilterIndex++;
    }
}

// Функция для отправки сообщения (будет использоваться для формы ввода)
function sendMessage() {
    const input = document.getElementById('input');
    const message = input.value.trim();

    if (message) {
        appendMessage('user', message);

        if (currentFilterIndex === filterOrder.length) {
            socket.emit('search', { query: message });
        } else {
            socket.emit('user-message', message);
        }

        input.value = '';
    }
}

// Функция для отображения сообщений в чате
function appendMessage(sender, text) {
    const div = document.createElement('div');
    div.className = 'message ' + sender;
    div.textContent = (sender === 'user' ? 'Вы: ' : 'Бот: ') + text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

// Функция для обработки нажатия на кнопку "Показать еще"
function showMore() {
    socket.emit('show-more');
}

function showMoreSearch() {
    socket.emit('show-more-search');
}

// Функция для отправки сообщения (будет использоваться для формы ввода)
function sendMessage() {
    const input = document.getElementById('input');
    const message = input.value.trim();

    if (message) {
        appendMessage('user', message);

        if (currentFilterIndex === filterOrder.length) {
            socket.emit('search', { query: message });
        } else {
            socket.emit('user-message', message);
        }

        input.value = '';
    }
}

// Функция для добавления товара в корзину
function addToCart(id_hat) {
    socket.emit('add-to-cart', { id_hat });
}

// Функция для просмотра корзины
function viewCart() {
    socket.emit('view-cart');
}

// Функция для оформления заказа
// Шаг 1: Отправка события checkout
function checkout() {
    socket.emit('checkout');
}

// Шаг 2: Отправка номера телефона
function sendPhoneNumber() {
    const phone = document.getElementById("phone-input").value;
    socket.emit('submit-phone', { phone });
    document.getElementById("phone-input").value = ""; // Очистка поля ввода после отправки
    document.getElementById("phone-input-container").classList.add("hidden"); // Скрытие поля ввода
}

// Прослушивание события от сервера для отображения поля ввода
socket.on('show-phone-input', () => {
    document.getElementById("phone-input-container").classList.remove("hidden");
});

function formatPhoneNumber(input) {
    // Удаляем все символы, кроме цифр
    let value = input.value.replace(/\D/g, '');

    // Форматируем номер
    if (value.length <= 1) {
        input.value = value;
    } else if (value.length <= 4) {
        input.value = value.slice(0, 1) + ' ' + value.slice(1);
    } else if (value.length <= 7) {
        input.value = value.slice(0, 1) + ' ' + value.slice(1, 4) + ' ' + value.slice(4);
    } else if (value.length <= 9) {
        input.value = value.slice(0, 1) + ' ' + value.slice(1, 4) + ' ' + value.slice(4, 7) + ' ' + value.slice(7);
    } else {
        input.value = value.slice(0, 1) + ' ' + value.slice(1, 4) + ' ' + value.slice(4, 7) + ' ' + value.slice(7, 9) + ' ' + value.slice(9);
    }
}

// Начинаем диалог при загрузке страницы
socket.emit('start');


