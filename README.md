# AuthorizationApp

Учебное настольное приложение авторизации на Python, PySide6 и SQLite.

## Возможности

- Регистрация и вход.
- SQLite-база `users.db`, создаётся автоматически.
- Хеширование паролей PBKDF2-HMAC-SHA256 с индивидуальной солью.
- Личный кабинет.
- Смена пароля.
- Администрирование пользователей: просмотр, изменение роли, удаление.
- Светлая и тёмная тема (на время текущего запуска приложения).

Первый зарегистрированный пользователь получает роль администратора. Следующие получают роль обычного пользователя.

## Запуск на Linux / NixOS

### Вариант A: через nix-shell

Из каталога проекта попробуйте:

```bash
nix-shell -p python313Packages.pyside6
python3 main.py
```

Если атрибут пакета не найден в вашей версии nixpkgs, используйте вариант B.

### Вариант B: через Python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

На NixOS pip-колёсам Qt иногда не хватает системных библиотек. Если приложение не запускается с ошибкой Qt platform plugin, предпочтите Qt/PySide6 из nixpkgs и сообщите точный текст ошибки.

## Запуск в Windows

```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python main.py
```

## Структура

```text
AuthorizationApp/
├── main.py
├── database/
│   ├── __init__.py
│   └── database.py
├── services/
│   ├── __init__.py
│   └── auth_service.py
├── ui/
│   ├── __init__.py
│   ├── theme.py
│   ├── login_window.py
│   ├── register_window.py
│   ├── dashboard_window.py
│   ├── users_dialog.py
│   └── change_password_dialog.py
├── requirements.txt
└── README.md
```

## Примечание

Это учебный проект, не готовая система для публичного сервиса. Для реального продукта потребуются дополнительные меры защиты, тесты, резервное копирование и более строгая модель управления сессиями.
