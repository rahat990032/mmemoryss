# Деплой на Timeweb

## Шаги:

1. Зарегистрируйся на https://timeweb.com/
2. Купи хостинг (Виртуальный хостинг Start за 199₽/мес)
3. В панели управления найди FTP доступы
4. Скачай FileZilla: https://filezilla-project.org/
5. Подключись по FTP к Timeweb
6. Загрузи все файлы из папки `clothing-website-netlify/` в папку `public_html/` на сервере

## Файлы для загрузки:
- index.html
- images/ (вся папка)
- data/ (вся папка)
- netlify/functions/ (нужно переделать на PHP)

## Важно:
Telegram бот на Timeweb нужно переделать с Netlify Functions на PHP.
Сейчас создам PHP версию.
