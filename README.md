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

| Команда             | Опис                                                 |
| ------------------- | ---------------------------------------------------- |
| `hello`             | Вітання                                              |
| `help`              | Показати список доступних команд                     |
| `add`               | Створює та додає                                     |
| `remove`            | Видаляє дані з контакту                              |
| `edit`              | Редагувати існуючі дані                              |
| `delete`            | Видалити контакт                                     |
| `all`               | Показати всі контакти                                |
| `birthdays <днів>`  | Показати, у кого ДН протягом вказаної кількості днів |
| `search <параметр>` | Пошук контакту за вказаним параметром                |
| `add-note <текст>`  | Додати нотатку                                       |
| `show-all-notes`    | Показати всі нотатки                                 |
| `delete-note <id>`  | Видалити нотатку                                     |
| `add-tag <тег>`     | Додати тег                                           |
| `find-tag <тег>`    | Знайти нотатки за тегом                              |
| `exit` або `close`  | Вийти з бота, зберегти дані                          |
