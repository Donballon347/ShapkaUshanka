from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit
import psycopg2
from psycopg2.extras import RealDictCursor


def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",  # Хост вашей базы данных
        database="shopdb",  # Название вашей базы данных
        user="postgres",  # Имя пользователя базы данных
        password="1337",  # Пароль пользователя базы данных
    )
    return conn


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)

# Словарь фильтров
filters = {
    "categories": [
        "Шапка",
        "Панама",
        "Снуд",
        "Берет+снуд",
        "Бандана",
        "Бейсболка",
        "Шапка+Снуд",
        "Берет",
        "Шарф",
    ],
    "gender": ["Мальчик", "Девочка", "Микс"],
    "season": ["Весна", "Зима", "Лето", "Осень"],
    "ears": ["С полуушками", "Без ушек", "С ушками"],
    "material": ["Болонь", "Светоотражающий элемент"],
    "composition": [
        "Акрил",
        "Хлопок",
        "Хлопок+Акрил",
        "Шерсть+Акрил",
        "Вискоза+Эластан",
        "Бамбук+Акрил",
        "Вискоза+Нейлон",
        "Шерсть",
        "Шерсть мериноса",
    ],
    "ties": ["Да", "Нет"],
    "size": [
        "50-52",
        "46-50",
        "54-56",
        "44-46",
        "52-54",
        "52-56",
        "50-54",
        "40-42",
        "46-48",
        "48-50",
        "42-44",
        "38-40",
    ],
}

user_filters = {}
page_number = 0
page_size = 5


def offer_return_to_selection():
    emit("bot-message", "Хотите вернуться к выбору?")
    emit("filter-options", ["Подобрать по фильтрам", "Найти товар по поиску"])


# Делаем корзину частью сессии пользователя
def get_cart():
    if "cart" not in session:
        session["cart"] = []
    return session["cart"]


def clear_cart():
    session["cart"] = []


@app.route("/")
def index():
    return render_template("index.html")


# Добавление товаров в корзину
@socketio.on("add-to-cart")
def add_to_cart(data):
    cart = get_cart()
    if "title" in data:
        cart.append(data["title"])  # Добавление товара в корзину
        session.modified = True
        emit("bot-message", f"{data['title']} добавлен в корзину.")
    else:
        emit("bot-message", "Ошибка: Товар не указан.")


# Просмотр содержимого корзины
@socketio.on("view-cart")
def view_cart():
    cart = get_cart()
    if cart:
        emit("bot-message", "Ваши товары в корзине:")
        for item in cart:
            emit("bot-message", f"- {item}")
    else:
        emit("bot-message", "Ваша корзина пуста.")


# Оформление заказа
@socketio.on("checkout")
def checkout():
    cart = get_cart()
    if cart:
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            for item in cart:
                cursor.execute("INSERT INTO orders (product_name) VALUES (%s)", (item,))
            conn.commit()
            clear_cart()
            emit("bot-message", "Ваш заказ оформлен!")
        except Exception as e:
            conn.rollback()
            emit("bot-message", "Ошибка при оформлении заказа. Попробуйте снова.")
            print(f"Ошибка: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        emit("bot-message", "Ваша корзина пуста. Невозможно оформить заказ.")


def get_filtered_hats(filters, offset=0, limit=5):
    query = """
    SELECT id_hat, title
    FROM hats
    WHERE category ILIKE %s
    AND sex ILIKE %s
    AND season ILIKE %s
    AND ears ILIKE %s
    AND material ILIKE %s
    AND composition ILIKE %s
    AND ties ILIKE %s
    AND size ILIKE %s
    LIMIT %s OFFSET %s
    """
    filter_values = (
        filters.get("categories", "%"),
        filters.get("gender", "%"),
        filters.get("season", "%"),
        filters.get("ears", "%"),
        filters.get("material", "%"),
        filters.get("composition", "%"),
        filters.get("ties", "%"),
        filters.get("size", "%"),
        limit,
        offset,
    )

    print("Выполняется запрос с фильтрами:", filter_values)  # Отладочное сообщение

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query, filter_values)
    hats = cursor.fetchall()
    cursor.close()
    conn.close()

    print("Результаты запроса:", hats)  # Отладочное сообщение

    return hats


@socketio.on("start")
def start_conversation():
    user_filters.clear()
    emit("bot-message", "Привет! Как вы хотите продолжить?")
    emit("filter-options", ["Подобрать по фильтрам", "Найти товар по поиску"])


@socketio.on("filter-selection")
def handle_filter_selection(data):
    global page_number
    filter_type = data["filter_type"]
    selection = data["selection"]

    if selection == "Подобрать по фильтрам":
        emit("bot-message", "Для начала выберите категорию.")
        emit("filter-options", filters["categories"])
        return

    elif selection == "Найти товар по поиску":
        emit("bot-message", "Введите название товара для поиска.")
        return

    if filter_type == "show_more":
        page_number += 1
        hats = get_filtered_hats(
            user_filters, offset=page_number * page_size, limit=page_size
        )
        if hats:
            for hat in hats:
                # emit("bot-message", f"Модель: {hat['title']}")
                emit(
                    "bot-message",
                    f"Модель: {hat['title']} <button onclick=\"addToCart({hat['id_hat']})\">Добавить в корзину</button>",
                )
            emit("bot-message", '<button onclick="showMore()">Показать еще</button>')
        else:
            emit("bot-message", "Больше нет товаров.")
        return

    user_filters[filter_type] = selection

    next_filter = None
    if filter_type == "categories":
        next_filter = "gender"
        emit("bot-message", f"Вы выбрали {selection}. Теперь выберите пол.")
    elif filter_type == "gender":
        next_filter = "season"
        emit("bot-message", f"Вы выбрали {selection}. Теперь выберите сезон.")
    elif filter_type == "season":
        next_filter = "ears"
        emit("bot-message", f"Вы выбрали {selection}. Теперь выберите ушки.")
    elif filter_type == "ears":
        next_filter = "material"
        emit("bot-message", f"Вы выбрали {selection}. Теперь выберите материал.")
    elif filter_type == "material":
        next_filter = "composition"
        emit("bot-message", f"Вы выбрали {selection}. Теперь выберите состав.")
    elif filter_type == "composition":
        next_filter = "ties"
        emit("bot-message", f"Вы выбрали {selection}. Теперь выберите наличие завязок.")
    elif filter_type == "ties":
        next_filter = "size"
        emit("bot-message", f"Вы выбрали {selection}. Теперь выберите размер.")
    elif filter_type == "size":
        emit("bot-message", "Вы выбрали все фильтры. Вот ваши варианты:")
        hats = get_filtered_hats(
            user_filters, offset=page_number * page_size, limit=page_size
        )
        if hats:
            for hat in hats:
                # emit("bot-message", f"Модель: {hat['title']}")
                emit(
                    "bot-message",
                    f"Модель: {hat['title']} <button onclick=\"addToCart({hat['id_hat']})\">Добавить в корзину</button>",
                )
            emit("bot-message", '<button onclick="showMore()">Показать еще</button>')
        else:
            emit("bot-message", "К сожалению, по вашим критериям ничего не найдено.")
        offer_return_to_selection()
        return

    if next_filter:
        emit("filter-options", filters[next_filter])


@socketio.on("show-more")
def show_more():
    global page_number
    page_number += 1
    show_hats()


def show_hats():
    global page_number
    hats = get_filtered_hats(
        user_filters, offset=page_number * page_size, limit=page_size
    )
    if hats:
        for hat in hats:
            # emit("bot-message", f"Модель: {hat['title']}")
            emit(
                "bot-message",
                f"Модель: {hat['title']} <button onclick=\"addToCart({hat['id_hat']})\">Добавить в корзину</button>",
            )
        emit("bot-message", '<button onclick="showMore()">Показать еще</button>')
    else:
        emit("bot-message", "К сожалению, по вашим критериям ничего не найдено.")
    offer_return_to_selection()


@socketio.on("search")
def handle_search(data):
    global page_number
    search_query = data["query"]
    page_number = 0  # Сбрасываем номер страницы при новом поисковом запросе

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # SQL запрос для поиска товаров по названию с лимитом и смещением для пагинации
    cursor.execute(
        """
        SELECT id_hat, title
        FROM hats
        WHERE title ILIKE %s
        LIMIT %s OFFSET %s
        """,
        (f"%{search_query}%", page_size, page_number * page_size),
    )

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    if results:
        for result in results:
            # emit("bot-message", f"Найдено: {result['title']}")
            emit(
                "bot-message",
                f"Модель: {result['title']} <button onclick=\"addToCart({result['id_hat']})\">Добавить в корзину</button>",
            )
        emit("bot-message", '<button onclick="showMoreSearch()">Показать еще</button>')
    else:
        emit("bot-message", "Ничего не найдено по вашему запросу.")
    offer_return_to_selection()


@socketio.on("show-more-search")
def show_more_search():
    global page_number
    page_number += 1

    search_query = user_filters.get("search_query", "")

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # SQL запрос для поиска товаров по названию с лимитом и смещением
    cursor.execute(
        """
        SELECT id_hat, title
        FROM hats
        WHERE title ILIKE %s
        LIMIT %s OFFSET %s
        """,
        (f"%{search_query}%", page_size, page_number * page_size),
    )

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    if results:
        for result in results:
            # emit("bot-message", f"Найдено: {result['title']}")
            emit(
                "bot-message",
                f"Модель: {result['title']} <button onclick=\"addToCart({result['id_hat']})\">Добавить в корзину</button>",
            )
        emit("bot-message", '<button onclick="showMoreSearch()">Показать еще</button>')
    else:
        emit("bot-message", "Больше нет товаров.")
    offer_return_to_selection()


if __name__ == "__main__":
    socketio.run(app, debug=True)
