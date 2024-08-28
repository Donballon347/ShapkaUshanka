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
socket.on('bot-message', (message) => {
    const div = document.createElement('div');
    div.className = 'message bot';
    div.innerHTML = message;
    chat.appendChild(div);
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

// Начинаем диалог при загрузке страницы
socket.emit('start');
