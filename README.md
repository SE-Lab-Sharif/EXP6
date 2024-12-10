# آزمایش ۶
در این آزمایش به طراحی یک سیستم ساده‌ با امکان انجام CRUD با معماری micro-service می‌پردازیم و برای این منظور از docker استفاده خواهیم کرد.

## Backend Component
در ابتدا یک component برای backend تعریف و پیاده‌سازی می‌کنیم. این کار را با استفاده از Flask انجام می‌دهیم و یک سرور ساده با قابلیت اضافه کردن / حذف کردن / دریافت اطلاعات و آپدیت اطلاعات درمورد تعدادی item (مثلا کالاها یا هر آیتم دیگری) پیاده‌سازی می‌کنیم. هر آیتم دارای یک `name` و یک `description` است.

```bash
each item = {"name": "item_name", "description": "item_description"}
```

کد موجود برای پیاده‌سازی این component از کل سرویس مدنظرمان را در پوشه‌ی `backend/` می‌توانید مشاهده کنید. ضمنا یک dockerfile برای آن می‌نویسیم تا بتوانیم آنرا در قالب یک image بیلد کنیم و سپس در کنار سایر component ها توسط docker-compose بالا بیاوریم و اجرا کنیم.

```Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV PYTHONUNBUFFERED=1
ENV DB_HOST=postgres
ENV DB_NAME=postgres
ENV DB_USER=postgres
ENV DB_PASSWORD=postgres

EXPOSE 8000

CMD ["python3", "app.py"]
```
توضیحات مربوط به بخش docker-compose را در بخش مربوط به خودش می نویسیم و توضیح می‌دهیم. در ابتدا یک docker-compose ساده می‌نویسیم و آنرا اجرا می کنیم تا از صحت عملکرد component بک‌اند خود مطمین شویم:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: postgres
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5433:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DB_HOST=postgres
      - DB_NAME=postgres
      - DB_USER=postgres
      - DB_PASSWORD=postgres
    depends_on:
      postgres:
        condition: service_healthy
```
با اجرای دستور `docker-compose up` می‌توانیم این سرویس را اجرا کنیم و از صحت عملکرد آن اطمینان حاصل کنیم.

```bash
sudo docker-compose up -d
```
و نتیجه بصورت زیر خواهد بود:
![1](static/1.png)
حالا با دستور زیر می‌بینیم که container های ما درحال اجرا هستند:
```bash
docker-compose ps
```

![2](static/2.png)

و حالا برای تست کردن، ابتدا یک table خالی برای item ها می‌سازیم:

```bash
docker-compose exec postgres psql -U postgres -c "CREATE TABLE IF NOT EXISTS items (id SERIAL PRIMARY KEY, name VARCHAR(100), description TEXT);"
```
و سپس به تست CRUD می‌پردازیم:

```bash
curl -X POST http://localhost:8000/items \
-H "Content-Type: application/json" \
-d '{"name":"test item","description":"test description"}'

curl -X POST http://localhost:8000/items \                                              
-H "Content-Type: application/json" \
-d '{"name":"second test item","description":"second test description"}'

curl http://localhost:8000/items        

curl http://localhost:8000/items/1           

curl -X PUT http://localhost:8000/items/1 \                                  
-H "Content-Type: application/json" \
-d '{"name":"updated item","description":"updated description"}'

curl http://localhost:8000/items        

curl -X DELETE http://localhost:8000/items/1  

curl http://localhost:8000/items
```

به ترتیب خروجی‌ها بصورت زیر اند:
![3](static/3.png)

![4](static/4.png)

![5](static/5.png)

![6](static/6.png)

![7](static/7.png)

![8](static/8.png)

![9](static/9.png)

![10](static/10.png)

## Load Balancer (LB) Component
...

## Docker Compose
...

## Results of running complete system
...
