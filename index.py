import redis
import sys

# Параметры подключения к Redis
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

def connect_redis():
    """Устанавливает соединение с Redis и возвращает объект соединения."""
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=False)
        # Проверка соединения
        r.ping()
        print(f"Успешное подключение к Redis: {REDIS_HOST}:{REDIS_PORT}")
        return r
    except redis.exceptions.ConnectionError as e:
        print(f"Ошибка подключения к Redis: {e}")
        print("Убедитесь, что сервер Redis запущен.")
        sys.exit(1)

def set_value(r):
    """Добавляет или обновляет значение по ключу."""
    key = input("Введите ключ (Key): ").strip()
    value = input("Введите значение (Value): ").strip()
    
    if not key or not value:
        print("Ключ и значение не могут быть пустыми.")
        return

    # Redis хранит данные в виде байтов, поэтому мы явно кодируем значение
    r.set(key, value.encode('utf-8'))
    print(f"\n[УСПЕХ] Установлено: '{key}' = '{value}'")

def get_value(r):
    """Получает значение по ключу."""
    key = input("Введите ключ для получения (Key): ").strip()
    
    if not key:
        print("Ключ не может быть пустым.")
        return

    # Получаем данные (они приходят в виде байтов)
    value_bytes = r.get(key)
    
    if value_bytes is not None:
        # Декодируем байты в строку для отображения
        value = value_bytes.decode('utf-8')
        print(f"\n[РЕЗУЛЬТАТ] Значение для '{key}': {value}")
    else:
        print(f"\n[ОШИБКА] Ключ '{key}' не найден.")

def display_menu():
    """Отображает главное меню."""
    print("\n" + "="*30)
    print("Консольный Redis Клиент")
    print("="*30)
    print("1. Добавить/Обновить данные (SET)")
    print("2. Получить данные (GET)")
    print("3. Выйти")
    print("="*30)

def main():
    """Основная функция приложения."""
    r = connect_redis()

    while True:
        display_menu()
        choice = input("Выберите опцию (1-3): ").strip()

        if choice == '1':
            set_value(r)
        elif choice == '2':
            get_value(r)
        elif choice == '3':
            print("Выход из приложения. До свидания!")
            break
        else:
            print("Неверный выбор. Пожалуйста, введите число от 1 до 3.")

if __name__ == "__main__":
    main()
