# 🚀 Sustainable Inventory Management (S.I.M.)

MVP for sustainable inventory management focusing on expiry date tracking and food waste reduction for the HoReCa sector.

---

## 🎯 The Goal: Why This Project Matters

Food waste is a massive global problem, especially in the HoReCa (Hotels, Restaurants, Catering) industry. This project aims to solve this by giving kitchens and managers **clear, immediate, and actionable insights** into their stock.

By actively monitoring expiry dates and, crucially, **tracking the *cost* of waste**, this tool helps businesses save money, reduce their environmental impact, and operate more sustainably.

## 💡 Real-World Application

This tool is designed for daily use by:

* **Chefs and Kitchen Staff:** To see which ingredients need to be used *today* (via color-coded alerts).
* **Inventory Managers:** To log "Used" vs. "Wasted" items, optimizing purchasing.
* **Business Owners:** To get a clear **financial report** on the total cost of food waste vs. food used.

---

## 🚀 Current Features (Beyond MVP)

* **Full CRUD Operations:** Full capability to **C**reate, **R**ead, **U**pdate (Use/Waste), and **D**elete products.
* **Expiry Date Alerts:** The dashboard automatically highlights products nearing expiration (Red, Yellow) or expired (Grey).
* **Cost Tracking:** The app logs the *cost-per-unit* for every "Use" or "Waste" transaction.
* **Financial Reporting:** A dedicated report page that calculates and displays:
    * Total **Quantity** Used vs. Wasted.
    * Total **Cost (€)** Used vs. Wasted.
* **Feedback System:** User-friendly flash messages (success, danger, info) confirm every action.

## 🛣️ Future Roadmap

* **Fase 5: User Authentication:** Implement a full login/logout system (using Flask-Login) so only authorized users can access the data.
* **Fase 6: Barcode/Scanner Integration:** Add the ability to use a barcode scanner (or the phone camera) to quickly add, find, or manage inventory items.
* **Fase 7: Advanced Reporting:** Add visual charts and graphs (e.g., using Chart.js) to the report page to better visualize the cost of waste over time.

---

## 🛠️ Tech Stack

* **Backend (Logic):** Python, Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF
* **Database:** SQLite
* **Frontend (UI):** Jinja2 Templates, HTML, CSS
* **Version Control:** Git & GitHub Desktop