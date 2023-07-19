# Asic-Scanner

Asic-Scanner - это автоматизированный скрипт Python, который сканирует сеть с майнерами криптовалюты, сравнивает количество и названия майнеров и сверяет их с сервисом Foreman. Все, что отсутствует в Foreman, скрипт отправляет отчет через Telegram.

## Установка и Запуск

### Предварительные условия

* Python 3.7+
* pip
* Linux с установленным cron

### Запуск скрипта

1. Клонируйте репозиторий на ваш локальный компьютер или сервер:

```
git clone https://github.com/yourusername/crypto-miners-scanner.git
```

2. Перейдите в директорию проекта:

```
cd crypto-miners-scanner
```

3. Установите необходимые зависимости:

```
pip install -r requirements.txt
```

4. Создайте файл `.env` в директории проекта и добавьте следующие переменные окружения:

```
FOREMAN_TOKEN=<ваш foreman token>
TELEGRAM_TOKEN=<ваш telegram token>
```

5. Создайте файл `config.ini` в директории проекта и настройте параметры сканируемых сетей в соответствии со следующим форматом:

```ini
[Название_места_1]
chat_id = <ID вашего чата в Telegram>
client_id = <Ваш ID клиента в Foreman>
network_ranges = <Диапазон IP-адресов для сканирования>
    192.168.0.1-192.168.0.254
    ...

[Название_места_2]
chat_id = <ID вашего чата в Telegram>
client_id = <Ваш ID клиента в Foreman>
network_ranges = <Диапазон IP-адресов для сканирования>
    <Дополнительный диапазон IP-адресов для сканирования>
    ...

```

6. Запустите скрипт:

```
python main.py
```

### Настройка Cron

В системах Linux вы можете настроить cron для автоматического запуска скрипта каждый день. Для этого:

1. Откройте crontab файл:

```
crontab -e
```

2. Добавьте следующую строку (замените `<путь к скрипту>` на реальный путь к `main.py`):

```
0 0 * * * /usr/bin/python3 <путь к скрипту>/main.py >> <путь к скрипту>/cron.log 2>&1
```

Эта строка означает, что скрипт будет запускаться каждый день в полночь. Результат выполнения скрипта будет записываться в файл `cron.log`.

## Поддержка

Если у вас возникли вопросы или проблемы, создайте `issue` в этом репозитории.

## Контрибуция

Пул-реквесты приветствуются. Для крупных изменений, пожалуйста, откройте `issue` сначала, чтобы обсудить, что вы хотели бы изменить.

## Лицензия

[MIT](https://choosealicense.com/licenses/mit/)