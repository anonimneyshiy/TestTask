####
Необходимое окружение:
- docker
- docker-compose

##### 
Подготовить проект к запуску:
```bash
   1. склонировать проект
   2. заменить файл .env.example в корне проекта на файл .env 
```
Для запуска сервиса в терминале из корневой папки проекта выполнить команду: 
##### 
```bash
   make up
```
Сервис будет доступен по адресу: http://127.0.0.1:8000

Для тестирования реализации решения: http://127.0.0.1:8000/docs#/default/get_tasks_tasks_post

Для остановки сервиса в терминале выполнить команду:
##### 
```bash
   make down
```
