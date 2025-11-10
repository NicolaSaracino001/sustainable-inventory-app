# 🚀 Sustainable Inventory Management MVP (S.I.M.)

**MVP for sustainable inventory management focusing on expiry date tracking and food waste reduction for the HoReCa sector.**

---

## 🎯 The Goal: Why This Project Matters

Food waste is a massive global problem, especially in the HoReCa (Hotels, Restaurants, Catering) industry. Millions of tons of food are thrown away every year simply because they are forgotten in the back of a stockroom until they expire.

This project aims to solve this problem.

**S.I.M.** is a smart inventory tool designed to give kitchens and managers **clear, immediate, and actionable insights** into their stock. By actively monitoring expiry dates, this tool helps businesses save money, reduce their environmental impact, and operate more sustainably.

## 💡 Real-World Application

This MVP serves as the foundation for a tool that can be used daily by:

* **Chefs and Kitchen Staff:** To quickly see which ingredients need to be used *today* (e.g., "Alert: 5kg of tomatoes expire in 2 days").
* **Inventory Managers:** To optimize purchasing, avoid overstocking, and track waste metrics over time.
* **Business Owners:** To get a clear report on cost savings from waste reduction.

---

## 🏁 MVP Core Features

The primary goal of this *specific* MVP is to:

1.  **Track Products:** Allow users to log items with quantity, cost, and (most importantly) **expiry date**.
2.  **Provide Visual Alerts:** Display the inventory in a clear dashboard that uses colors (Red, Yellow, Green) to highlight products nearing expiration.
3.  **Log Waste:** Allow users to mark items as "used" or "wasted" to begin tracking data.

## 🛠️ Tech Stack (MVP)

* **Backend (Logic):** Python / Flask
* **Database:** SQLite
* **Frontend (UI):** HTML / CSS rendered via Jinja2 Templates
* **Version Control:** Git & GitHub Desktop

## 📂 Project Structure

* `/src`: Main source code.
* `/src/models`: Database models (SQLAlchemy).
* `/src/routes`: Application routes/views.
* `/src/templates`: HTML templates.
* `/src/static`: CSS and JS files.