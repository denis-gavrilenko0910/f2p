# Асистент-Бот

## 📌 Опис

Цей проєкт — консольний асистент-бот на Python, який допомагає керувати особистими **контактами** та **нотатками**. Бот дозволяє зберігати інформацію про контакти (імена, телефони, дні народження), а також створювати нотатки з тегами.

Уся інформація зберігається між сесіями завдяки використанню файлів `.pkl`.

---

## ⚙️ Функціонал

### 📇 Контакти

- Додавання нового контакту
- Додавання кількох номерів телефону до контакту
- Видалення телефону
- Редагування телефону
- Збереження дати народження
- Виведення кількості днів до наступного дня народження
- Пошук контактів за іменем або номером
- Перегляд усіх контактів

### 🗒️ Нотатки

- Створення нотаток
- Додавання тегів до нотатки
- Пошук нотаток за тегом
- Видалення нотатки
- Перегляд усіх нотаток у вигляді таблиці

### 💾 Збереження даних

- Автоматичне збереження контактів у файл `addressbook.pkl`
- Автоматичне збереження нотаток у файл `notebook.pkl`

---

## 🧑‍💻 Використання

Після запуску скрипта бот готовий приймати команди у консольному режимі.

### 🔑 Основні команди

| Команда                                | Опис                                   |
| -------------------------------------- | -------------------------------------- |
| `hello`                                | Вітання                                |
| `add contact <ім'я> <телефон>`         | Додати новий контакт                   |
| `add phone <ім'я> <телефон>`           | Додати телефон до наявного контакту    |
| `delete phone <ім'я> <телефон>`        | Видалити телефон                       |
| `change phone <ім'я> <старий> <новий>` | Змінити номер телефону                 |
| `add birthday <ім'я> <ДД.ММ.РРРР>`     | Додати дату народження                 |
| `days to birthday <ім'я>`              | Скільки днів до дня народження         |
| `find <текст>`                         | Пошук контактів за іменем або номером  |
| `show all`                             | Показати всі контакти                  |
| `add note <текст>`                     | Додати нотатку                         |
| `add tag <id> <тег1> <тег2>...`        | Додати теги до нотатки                 |
| `find tag <тег>`                       | Пошук нотаток за тегом                 |
| `delete note <id>`                     | Видалити нотатку                       |
| `show notes`                           | Показати всі нотатки                   |
| `exit` або `close`                     | Завершити роботу бота та зберегти дані |

---
