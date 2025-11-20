# 🚀 Sustainable Inventory Management (S.I.M.)

**A smart inventory MVP designed to reduce food waste in the HoReCa sector through expiry tracking and cost analysis.**

---

## 🎯 The Goal: Why This Project Matters

Food waste is a massive financial and environmental problem. **S.I.M.** helps chefs and managers track their stock intelligently. 

By monitoring expiry dates and calculating the exact **cost of waste**, this tool turns inventory management into a sustainability strategy.

## 💡 Key Features (Implemented)

### 🔐 Security & Access
* **User Authentication:** Secure Login and Registration system.
* **Protected Data:** Only authorized users can access the inventory dashboard and make changes.

### 📦 Inventory Management (CRUD)
* **Barcode Support:** Ability to input and view Barcodes/SKUs for every product.
* **Full Tracking:** Create, Read, Update, and Delete products.
* **Smart Dashboard:** Immediate visual alerts for products:
    * 🔴 **Expiring soon (High Risk)**
    * 🟡 **Warning (Medium Risk)**
    * ⚪ **Safe**

### 📉 Sustainability & Finance
* **Use vs. Waste Logic:** Distinct actions to log whether a product was "Used" (Sold) or "Wasted" (Thrown away).
* **Financial Reporting:** A dedicated Report page that calculates:
    * Total **Cost (€)** Used.
    * Total **Cost (€)** Wasted.
* **Action Logs:** Complete history of every transaction with timestamps.

---

## 🛣️ Roadmap & Future Goals

We are currently working on Phase 6. Here is the plan for the next steps:

- [x] **Phase 1-4: MVP Core** (Database, Dashboard, Alerts, Reports).
- [x] **Phase 5: Security** (Login/Logout implementation).
- [x] **Phase 6a: Barcode Data Entry** (Database & UI update).
- [ ] **Phase 6b: Scan-to-Search** (Use a barcode scanner to instantly find products in the dashboard).
- [ ] **Phase 7: Advanced Visualization** (Integrate charts/graphs like Chart.js to visualize waste trends over time).
- [ ] **Phase 8: UI/UX Polish** (Logo design, advanced styling, and responsive mobile layout).

---

## 🛠️ Tech Stack

* **Language:** Python 3
* **Framework:** Flask
* **Database:** SQLite (SQLAlchemy ORM)
* **Authentication:** Flask-Login, Werkzeug Security
* **Forms:** Flask-WTF
* **Frontend:** HTML5, CSS3, Jinja2 Templates
* **Version Control:** Git & GitHub