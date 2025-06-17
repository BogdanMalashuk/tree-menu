# Django tree-menu

**tree-menu** — это Django-приложение для управления и отображения многоуровневого меню, хранящегося в базе данных.  
Меню можно создавать и редактировать через стандартную админку Django. Для вывода меню на страницах используется кастомный template tag.  

---

# 📋 Основные возможности

- 🗄️ Хранение меню и пунктов меню в базе данных (PostgreSQL, SQLite и др.)
- 🌳 Поддержка неограниченной вложенности пунктов меню
- 🛠️ Редактирование меню через стандартную Django Admin
- 🔗 Выбор URL пункта меню — явный URL или named URL (Django reverse)
- 🎯 Автоматическое определение активного пункта меню по текущему URL
- 🔓 Развёртывание ветвей меню: все пункты выше активного и первая вложенность под ним открыты
- 📑 На одной странице можно вывести несколько меню по их названию
- ⚡ Оптимальный запрос к базе данных — 1 вложенность = 1 запрос
- 🐍 Совместимость с Django 5.x и Python 3.12+

---

# 🧭 Структура проекта

```
project/
├── app/
│   ├── management/
│   │   └── commands/
│   │       └── seed_data.py   
│   ├── migrations/
│   ├── templatetags/
│   │   └── menu_tags.py            
│   ├── admin.py
│   ├── models.py                   
│   ├── tests.py                                      
│   ├── urls.py                  
│   └── views.py       
├── project/
│   ├── asgi.py
│   ├── wsgi.py
│   ├── settings.py
│   └── urls.py
├── templates/
│   ├── base/
│   │   └── base.html           
│   ├── main/
│   │   └── home.html            
│   └── menus/
│       ├── page.html
│       └── menu.html   
├── manage.py
├── requirements.txt
└── README.md
```

---

# 🛠️ Установка

## 📥 Клонирование проекта

```bash
git clone https://github.com/BogdanMalashuk/tree-menu.git
```


## 🧪 Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate       # Windows
# OR
source .venv/bin/activate     # Alt if .venv used
```


## 📦 Установка зависимостей

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## ⚙️ .env конфигурация

Create a `.env` file and add the following variables:

```ini
DEBUG=True
SECRET_KEY=super-secret-key-1234567890
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

POSTGRES_DB=dbname
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

---

# 🧪 Тестовое наполнение БД

```bash
cd project
python manage.py seed_data
```
