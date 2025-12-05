# 🌱 S.I.M. - Sustainable Inventory Management

**A smart, eco-friendly inventory management system (PWA) designed for the HoReCa sector to reduce food waste and optimize costs.**

![SIM Logo](src/static/logo.png)

---

## 🎯 The Goal

Food waste is a massive financial and environmental problem. **S.I.M.** empowers chefs and managers to track their stock intelligently. By monitoring expiry dates, calculating the exact **cost of waste**, and gamifying the process, this tool turns inventory management into a sustainability strategy.

---

## 💡 Key Features (Completed Phases 1-14)

### 📱 User Experience (PWA)
* **Progressive Web App:** Installable on any device (iOS, Android, Desktop) with a native app-like experience.
* **Modern UI:** Clean, responsive design with "Inter" font, custom branding, and mobile-optimized layout.

### 🔐 Security & Access
* **Secure Authentication:** Complete Login/Registration system.
* **User Profile:** Custom profile management with personalized waste budget settings.

### 📦 Smart Inventory (CRUD +)
* **Barcode Memory:** "Scan-to-fill" feature that remembers products you've scanned before, auto-filling details to save time.
* **Visual Alerts:** Dashboard rows change color based on expiry urgency (🔴 High Risk, 🟡 Warning, ⚪ Safe).
* **Search & Scan:** Instant search bar compatible with USB/Bluetooth barcode scanners.

### 📉 Sustainability & Intelligence
* **Smart Tips 💡:** Context-aware advice on how to save expiring items based on their category.
* **Smart Restock 📧:** Automatically detects low stock and generates pre-filled order emails for suppliers.
* **Academy Section 🎓:** A dedicated video learning hub for zero-waste training.

### 📊 Reports & Gamification
* **Financial Reports:** Visual charts (Pie & Bar) showing "Used vs. Wasted" costs and weekly trends.
* **Excel Export:** One-click export of the full inventory for accounting purposes.
* **Gamification 🏆:** Weekly Waste Budget tracker with **"Eco-Hero"** badges to motivate the team.

---

## 🛣️ Roadmap: Next Steps

We are moving towards Cloud Deployment and AI Integration.

- [x] **Phase 1-12:** Core MVP, Analytics, Gamification.
- [x] **Phase 13:** User Profile & Custom Settings.
- [x] **Phase 14:** PWA Conversion & UI Polish.
- [ ] **Phase 15:** Cloud Deployment (Put the app online for real usage).
- [ ] **Phase 16:** AI Integration (Recipe suggestions, visual recognition).
- [ ] **Phase 17:** Advanced Mobile Native Features (Camera scan, Push notifications).

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