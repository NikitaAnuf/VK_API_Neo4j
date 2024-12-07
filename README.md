**Развёртывание приложения** <br />
Сначала нужно создать в корневой директории проекта файл .env, в котором нужно задать несколько переменных:
- ACCESS_TOKEN - токен доступа к VK API
- NEO4J_HOST - IP-адрес, на котором развёрнут Neo4j
- NEO4J_PORT - порт, по которому можно получить доступ к Neo4j
- NEO4J_USER - пользователь / название DBMS
- NEO4J_PASSWORD - пароль для доступа к DBMS
- NEO4J_NAME - название базы данных внутри DBMS

При разработке использовался python 3.13.

Приложение можно запустить, просто написав ```python main.py``` в рабочей директории проекта,
тогда будет запущен скрипт для получения количества узлов типа User из базы данных

**Параметры запуска** <br />
У приложения есть 3 режима работы, которые указываются в командной строке через параметр ```--mode```:
- ```api``` - получение данных из VK API и их запись в JSON-файл. Параметры:
    - ```--userid``` - ID пользователя VK, по которому будут проходить запросы, по умолчанию указан ID моего аккаунта
    - ```--filepath``` - путь и название файла (опционально), по которому нужно положить итоговый файл, по умолчанию
  название файла формируется как текущая дата и время в формате ```yyyy-mm-dd-HH-MM-SS.json``` и складывается в папку
  ```results``` в корне приложения
- ```import``` - импорт JSON-файла в базу данных Neo4j. Параметры:
  - ```--filepath``` - путь и название файла, из которого нужно импортировать данные, по умолчанию берёт последний
  по названию JSON-файл из папки ```results```
- ```query``` - выполнение запроса к базе данных Neo4j. Я поделил запросы на 3 типа, они указываются в параметре
```--type```:
  - ```count``` - запрос на получение количества узлов с типом ```User``` или ```Group```.
  Конкретный тип узла задаётся параметром ```--nodetype```, его значения могут быть ```user``` или ```group```
  - ```top``` - запрос на получение узлов с наибольшим количеством связей. У него тоже есть параметр ```--nodetype```:
    - ```user``` - получение пользователей с наибольшим количеством фолловеров
    - ```group``` - получение групп с наибольшим количеством подписчиков 
    
    Также у этого типа запросов есть параметр ```--topn```, который задаёт количество выводимых узлов, по умолчанию
    указано значение ```5```
  - ```mutual``` - возвращает пары пользователей, которые являются фолловерами друг для друга,
  дополнительных параметров нет


**Примеры строк запуска** <br />
Для получения количества узлов типа ```User```: <br />
```python main.py --mode query --type count --nodetype user```<br />

Для получения 10 групп с наибольшим количеством подписчиков: <br />
```python main.py --mode query --type top --nodetype group --topn 10```<br />

Для получения пользователей, которые являются фолловерами друг друга:<br />
```python main.py --mode query --type mutual```

**Обработка ошибок** <br />
Большинство возможных ошибок пользователя точечно обработаны в коде, ошибки в инкапсулированых скриптах завёрнуты в
try-except

**Логирование** <br />
Есть 4 вида логов: ```general``` записывает общие данные о работе приложения, ```api```, ```import``` и ```query```
записывают логи по своим режимам работы приложения, записываются логи типов ```info```, ```warn``` и ```error``` <br />
Логи складываются в отдельные файлы в папке ```logs```

**Дамп базы данных** <br />
Дамп записан в папку ```dump``` в формате ```record-aligned-1.1```