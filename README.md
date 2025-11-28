# 🌱 Sustainable Inventory Management (S.I.M.)

**A smart, eco-friendly inventory management system designed for the HoReCa sector to reduce food waste and optimize costs.**

---

## 🎯 The Goal

Food waste is a massive financial and environmental problem. **S.I.M.** empowers chefs and managers to track their stock intelligently. By monitoring expiry dates, calculating the exact **cost of waste**, and gamifying the process, this tool turns inventory management into a sustainability strategy.

---

## 💡 Key Features

### 🔐 Security & Access
* **Secure Authentication:** Complete Login/Registration system.
* **Role-Based Access:** Only authorized staff can view or modify sensitive data.

### 📦 Smart Inventory (CRUD +)
* **Barcode Memory:** "Scan-to-fill" feature that remembers products you've scanned before, auto-filling details to save time.
* **Visual Alerts:** Dashboard rows change color based on expiry urgency (🔴 High Risk, 🟡 Warning, ⚪ Safe).
* **Search & Scan:** Instant search bar compatible with USB/Bluetooth barcode scanners.

### 📉 Sustainability & Intelligence
* **Smart Tips 💡:** Clicking on expiring items provides category-specific advice on how to save them (e.g., "Meat expiring? Freeze or cook ragù").
* **Smart Restock 📧:** Automatically detects low stock (< 5 units) and generates a pre-filled email to order from suppliers.
* **Academy Section 🎓:** A dedicated learning hub with video tutorials on zero-waste cooking and storage techniques.

### 📊 Reports & Gamification
* **Financial Reports:** Visual charts (Pie & Bar) showing "Used vs. Wasted" costs in real-time.
* **Excel Export:** Download the full inventory or logs as `.xlsx` files for accounting.
* **Gamification 🏆:** Weekly Waste Budget tracker. Stay under budget to earn the **"Eco-Hero"** badge!

---

## 🛣️ Project Roadmap

We are rapidly evolving. Here is our progress:

- [x] **Core MVP:** Database, Dashboard, Basic Alerts.
- [x] **Security:** Flask-Login implementation.
- [x] **Efficiency:** Barcode integration & Product Memory.
- [x] **Business Logic:** Excel Export & Smart Restock emails.
- [x] **Education:** Academy Video Section.
- [x] **Engagement:** Gamification & Badges.
- [ ] **Phase 13:** User Profile & Custom Settings (Set your own waste budget).
- [ ] **Phase 14:** PWA (Progressive Web App) - Installable on mobile devices.
- [ ] **Phase 15:** Cloud Deployment (Online access).

---

## 🛠️ Tech Stack

* **Backend:** Python 3, Flask, SQLAlchemy
* **Database:** SQLite
* **Data Analysis:** Pandas, OpenPyXL
* **Frontend:** HTML5, CSS3 (Responsive), Jinja2, Chart.js, FontAwesome
* **Version Control:** Git & GitHub

---

### 🚀 How to Run Locally

1.  Clone the repository.
2.  Create a virtual environment: `python -m venv venv`
3.  Install dependencies: `pip install -r requirements.txt`
4.  Run the app: `python run.py`
5.  Access at: `http://127.0.0.1:5000`