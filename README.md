# 🛠 UXIM → SalesDrive Order & Catalog Sync Worker

Этот проект — фоновый Python-воркер, который каждые 15 минут:
- Синхронизирует заказы со статусом `new` с сайта [pitaka.ux.im](https://pitaka.ux.im) в CRM SalesDrive
- Обновляет цены и наличие товаров на сайте на основе YML-фида SalesDrive (раз в час)

---

## 🚀 Возможности

- ✅ Автоматическая отправка новых заказов в CRM
- ✅ Обновление статуса заказа на `process` после успешной передачи
- ✅ Маппинг товаров и клиентов под API SalesDrive
- ✅ Раз в 1 час: сравнение каталога YML ↔ UXIM
- ✅ Обновление цены и наличия на сайте, если есть расхождения
- ✅ Обработка ошибок и логирование
- ✅ Деплой на [Render.com](https://render.com)

---

## 📦 Установка

```bash
git clone https://github.com/<твой-аккаунт>/order_sync.git
cd order_sync
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
