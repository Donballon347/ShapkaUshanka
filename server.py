from flask import Flask, render_template
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


@app.route("/")
def index():
    return render_template("index.html")


def get_filtered_hats(filters, offset=0, limit=5):
    query = """
    SELECT title
    FROM hats
    WHERE category = %s
    AND sex = %s
    AND season = %s
    AND ears = %s
    AND material = %s
    AND composition = %s
    AND ties = %s
    AND size = %s
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

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query, filter_values)
    hats = cursor.fetchall()
    cursor.close()
    conn.close()

    return hats


@socketio.on("start")
def start_conversation():
    user_filters.clear()
    emit(
        "bot-message", "Привет! Давайте подберем шапку. Для начала выберите категорию."
    )
    emit("filter-options", filters["categories"])


# @socketio.on("filter-selection")
# def handle_filter_selection(data):
#     filter_type = data["filter_type"]
#     selection = data["selection"]

#     user_filters[filter_type] = selection

#     next_filter = None
#     if filter_type == "categories":
#         next_filter = "gender"
#         emit("bot-message", f"Вы выбрали {selection}. Теперь выберите пол.")
#     elif filter_type == "gender":
#         next_filter = "season"
#         emit("bot-message", f"Вы выбрали {selection}. Теперь выберите сезон.")
#     elif filter_type == "season":
#         next_filter = "ears"
#         emit("bot-message", f"Вы выбрали {selection}. Теперь выберите ушки.")
#     elif filter_type == "ears":
#         next_filter = "material"
#         emit("bot-message", f"Вы выбрали {selection}. Теперь выберите материал.")
#     elif filter_type == "material":
#         next_filter = "composition"
#         emit("bot-message", f"Вы выбрали {selection}. Теперь выберите состав.")
#     elif filter_type == "composition":
#         next_filter = "ties"
#         emit("bot-message", f"Вы выбрали {selection}. Теперь выберите наличые завязок.")
#     elif filter_type == "ties":
#         next_filter = "size"
#         emit("bot-message", f"Вы выбрали {selection}. Теперь выберите размер.")
#     elif filter_type == "size":
#         emit("bot-message", "Вы выбрали все фильтры. Вот ваши варианты:")
#         result = f"Модель 1. {user_filters['categories']}, {user_filters['gender']}, {user_filters['season']}, {user_filters['ears']}, {user_filters['material']}, {selection}"
#         emit("bot-message", result)
#         return

#     if next_filter:
#         emit("filter-options", filters[next_filter])


@socketio.on("filter-selection")
def handle_filter_selection(data):
    global page_number
    filter_type = data["filter_type"]
    selection = data["selection"]

    if filter_type == "show_more":
        page_number += 1
        hats = get_filtered_hats(
            user_filters, offset=page_number * page_size, limit=page_size
        )
        if hats:
            for hat in hats:
                emit("bot-message", f"Модель: {hat['title']}")
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
                emit("bot-message", f"Модель: {hat['title']}")
            emit("bot-message", '<button onclick="showMore()">Показать еще</button>')
        else:
            emit("bot-message", "К сожалению, по вашим критериям ничего не найдено.")
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
            emit("bot-message", f"Модель: {hat['title']}")
        emit("bot-message", '<button onclick="showMore()">Показать еще</button>')
    else:
        emit("bot-message", "К сожалению, по вашим критериям ничего не найдено.")


@socketio.on("search")
def handle_search(data):
    search_query = data["query"]

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # SQL запрос для поиска товаров по названию
    cursor.execute(
        """
        SELECT title
        FROM hats
        WHERE title ILIKE %s
        """,
        (f"%{search_query}%",),
    )

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    if results:
        for result in results:
            emit("bot-message", f"Найдено: {result['title']}")
    else:
        emit("bot-message", "Ничего не найдено по вашему запросу.")


if __name__ == "__main__":
    socketio.run(app, debug=True)
