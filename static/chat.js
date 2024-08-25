// const socket = io();
// const chat = document.getElementById('chat');

// const filterOrder = ['categories', 'gender', 'season', 'ears', 'material', 'composition', 'ties', 'size'];
// let currentFilterIndex = 0;

// // Функция для отображения сообщений в чате
// function appendMessage(sender, text) {
//     const div = document.createElement('div');
//     div.className = 'message ' + sender;
//     div.textContent = (sender === 'user' ? 'Вы: ' : 'Бот: ') + text;
//     chat.appendChild(div);
//     chat.scrollTop = chat.scrollHeight;
// }

// // Обработка сообщений от бота
// socket.on('bot-message', (message) => {
//     const div = document.createElement('div');
//     div.className = 'message bot';
//     div.innerHTML = message;
//     chat.appendChild(div);
// });

// // Обработка кнопок с опциями фильтров
// socket.on('filter-options', (options) => {
//     const buttons = options.map(option => `<button onclick="selectFilter('${option}')">${option}</button>`).join(' ');
//     const div = document.createElement('div');
//     div.className = 'message bot';
//     div.innerHTML = buttons;
//     chat.appendChild(div);
// });

// // Функция для отправки выбранного фильтра на сервер
// function selectFilter(selection) {
//     appendMessage('user', selection);

//     const currentFilter = filterOrder[currentFilterIndex];
//     socket.emit('filter-selection', { filter_type: currentFilter, selection: selection });

//     // Увеличиваем индекс текущего фильтра для следующего этапа
//     currentFilterIndex++;
// }

// // Функция для обработки нажатия на кнопку "Показать еще"
// function showMore() {
//     socket.emit('filter-selection', { filter_type: 'show_more', selection: '' });
// }

// // Функция для отправки сообщения (будет использоваться для формы ввода)
// function sendMessage() {
//     const input = document.getElementById('input');
//     const message = input.value.trim();
//     if (message) {
//         appendMessage('user', message);
//         socket.emit('user-message', message); // Пример события для отправки сообщения
//         input.value = '';
//     }
// }

// // Начинаем диалог при загрузке страницы
// socket.emit('start');





const socket = io();
const chat = document.getElementById('chat');

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

// Функция для отправки выбранного фильтра на сервер
function selectFilter(selection) {
    appendMessage('user', selection);

    const currentFilter = filterOrder[currentFilterIndex];
    socket.emit('filter-selection', { filter_type: currentFilter, selection: selection });

    // Увеличиваем индекс текущего фильтра для следующего этапа
    currentFilterIndex++;
}

// Функция для обработки нажатия на кнопку "Показать еще"
function showMore() {
    socket.emit('show-more');
}

// Функция для отправки сообщения (будет использоваться для формы ввода)
function sendMessage() {
    const input = document.getElementById('input');
    const message = input.value.trim();
    if (message) {
        appendMessage('user', message);
        socket.emit('user-message', message); // Пример события для отправки сообщения
        input.value = '';
    }
}

// Начинаем диалог при загрузке страницы
socket.emit('start');
