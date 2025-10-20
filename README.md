# Library Management System (12th Grade Final Project)

A simple, menu-driven **Library Management System** built with **Python** and **MySQL**.  
Manage **books, members, lendings/returns, fines, staff, and spending** through a terminal interface.

**Repo contents**
- `source.py` — Python program (menu-driven CLI)
- `server.sql` — MySQL schema + sample data

---

## 🧰 Requirements
- **Python** 3.8+
- **MySQL** 8.x (or MariaDB)
- Python package: `mysql-connector-python`

Install the Python connector:
```bash
pip install mysql-connector-python

```
## 🗃️ Database Setup (MySQL)

1. Start MySQL and log in:

```bash
mysql -u root -p
```

2. Create the database **exactly** with this name (lowercase, includes spaces):

```sql
CREATE DATABASE `library management system`;
```

> **Important**
>
> * The code expects the database name **`library management system`**.
> * On Linux/macOS, names can be case-sensitive—use the exact spelling.
> * If `server.sql` has a `DROP DATABASE` line, **remove/comment it** before importing.

3. Load tables + sample data (from your OS shell, not inside the MySQL prompt):

```bash
mysql -u root -p "library management system" < server.sql
```

*(Or, inside MySQL: `USE \`library management system`;`then paste the CREATE/INSERT parts from`server.sql`.)*

---

## 🔌 Default Connection Details

The program (in `source.py`) connects using:

* **host**: `localhost`
* **user**: `root`
* **password**: `Mysql@2005`
* **database**: `library management system`

If your local MySQL password differs, update it in `source.py` or change your local root password accordingly.

---

## ▶️ Running the Program

From the folder containing `source.py`:

```bash
python source.py
```

**Login options (demo IDs)**

* Librarian (trial): `123456`
* Manager (trial): `1234567`
  *(If you’ve added staff via SQL with passwords, use their `ID No` + password.)*

---

## ✨ Features (Menu Overview)

* **Books**

  * Add / remove books
  * Search by **name / id / writer / category**
  * List all books; filter **available** vs **borrowed**

* **Members & Memberships**

  * Add members (Reg ID, Name, Mobile No., Tenure)
  * View member details
  * Renew membership (annual tenures)

* **Lendings & Returns**

  * Lend a book to a member
  * Extend “Borrowed Till” (total cap: **30 days**)
  * Return book; availability status updates automatically

* **Fines**

  * Automatic fine by days delayed:

    * 0 days → ₹0
    * 1–2 days → ₹10/day
    * 3–5 days → ₹20 + ₹25/day over 2
    * ≥6 days → ₹95 + ₹50/day over 5

* **Staff**

  * Add staff (`ID No` like `LIBXXXX`), set position & salary
  * Passwords for privileged roles (e.g., Manager)
  * View / edit staff details

* **Spending**

  * Record purchases (item, date, amount)
  * Filter by item & date range
  * Show totals over a period

---

## 🧪 Quick Demo Flow

1. `python source.py`
2. Login as **Manager (trial)**: `1234567`
3. Try: add a **Member** → lend a **Book** → extend/return → check **Fines**
4. Record a **Spending** entry and view totals

---

## 🐞 Troubleshooting

* **“Error! Not connected to MySQL”**
  Ensure MySQL is running, credentials in `source.py` are correct, and DB name is **`library management system`**.

* **Login fails**
  Use trial IDs above or add staff via SQL and use their `ID No` + password.

* **Import drops my DB**
  Remove/comment any `DROP DATABASE` in `server.sql` before importing.

* **Case sensitivity**
  On Linux/macOS, create the DB exactly as: `` `library management system` `` (lowercase, with spaces).

---

## 📄 Notes

This project is intentionally kept in its original classic terminal form as built for a 12th-grade final.
Optional future improvements: parameterized queries, `.env` for credentials, unit tests for fine logic, and a minimal web UI.

---
