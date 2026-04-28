# Веб-сайт Shop (shop.jk-lab.ru)

Тестовый проект сайта для оформления заказов через платежную систему Stripe.
Протестировать проект можно по ссылке: shop.jk-lab.ru

## Функционал

- Реализованы модели: 
  - Item (для товаров)
  - Order (для корзин с товарами, Many-to-many к Item)
  - Tax (для налогов, One-to-many к Order) 
  - Discount (для скидок, One-to-many к Order)
- Реализован Stripe PaymentIntent - в связи с этим логика эндпоинов изменена под особенности работы с 
  данным платежным методом, но общая логика осталась (кнопка Buy на странице товара и реализация 
  через нее платежа)
- Реализованы: 
  - Покупка товаров по отдельности и через корзину.
  - Скидки и налоги на товары (налог можно протестировать, добавив его в заказ через админ-панель -
    там уже созданы дефолтный налог и дефолтная скидка по промокоду STRIPE).
  - 2 разные валюты - RUB и USD.
  - Просмотр моделей через админ-панель.
  - Запуск с помощью docker-compose.
  - Загрузка переменных из .env.
- Эндпоинты: 
  - GET /item/{id} - страница товара с кнопками добавления в корзину и моментальной покупки.
  - GET /buy/{id} - эндпоинт, к которому обращается JS при нажатии на кнопку моментальной покупки 
  (Buy) на странице товара для получения ClientSecret для PaymentIntent.
  - GET /cart - отображение корзины с товарами, через которую так же можно оформить покупку.
  - GET /buy - эндпоинт, к которому обращается JS при нажатии на кнопку Buy на странице корзины 
    для получения ClientSecret для PaymentIntent.
  - POST /cart/add - добавление товара в корзину.
  - POST /cart/remove - удаление товара из корзины.
  - POST /webhook/stripe - эндпоинт, на который приходят вебхуки от Stripe со статусом платежа, 
    он так же меняет статус заказа в базе данных.
  - GET success/ - эндпоинт для перенаправления пользователя после успешного платежа.
  - POST apply_promo/ - эндпоинт для применения скидки к заказу, переход на который реализован 
    с помощью ввода промокода в корзине.
  - GET / - главная страница для удобного просмотра товаров.

## Технологии

- Python 3.13
- Django 6.0.4
- PostgreSQL
- Docker/Docker Compose
- Nginx
- Gunicorn 25.3.0
- Stripe 15.1.4

## Как получить API ключи

### API ключи Stripe
1. Зарегистрируйтесь в [Stripe](https://dashboard.stripe.com/)
2. Перейдите на Developers, API keys.
3. Скопируйте Publishable key и Secret key.
4. Перейдите на Developers, Webhooks.
5. Нажмите кнопку Add endpoint.
6. В поле «Endpoint URL» вставьте URL твоего сервера, где будет представление для вебхука.
7. В разделе «Events to send» отметьте галочками события для Payment Intent.
8. Скопируйте Signing secret.

## Данные для тестирования платежей Stripe

Номера тестовых карт:
Успешная оплата - 4242 4242 4242 4242
Требуется 3D Secure	- 4000 0025 0000 3155
Недостаточно средств - 4000 0000 0000 9995
Карта отклонена - 4000 0000 0000 0002

CVV - любые 3 цифры, дата - любая будущая дата.

## Переменные окружения

Создайте файл .env в ./shop, структура представлена в файле .env_example:

```bash
# PostgreSQL
POSTGRES_DB=postgres
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password

# Stripe
STRIPE_PUBLISHABLE_KEY=your_pub_key
STRIPE_SECRET_KEY=your_secret_key
STRIPE_WEBHOOK_SECRET=your_webhook_key

# Django
SECRET_KEY=your_secret_key
DEBUG=False
ALLOWED_HOSTS=host.com
CSRF_TRUSTED_ORIGINS=http://host.com
```

## Как запустить

```bash
# Клонировать репозиторий
git clone ...
cd Shop_with_Stripe

# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows

# Запускаем проект
docker compose up

# Создать суперпользователя (опционально)
docker exec -it django_shop python manage.py createsuperuser
```

## Статус проекта

Закончен

## Автор
Кузнецова Юлия / https://github.com/juliamayorrr