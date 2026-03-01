# 🃏 GUY TCG Marketplace Project (Final Commit 60)

โปรเจกต์ระบบจำลองตลาดซื้อขายการ์ดเกม (Trading Card Game) ที่พัฒนาด้วย **Python Flask** และ **SQLAlchemy** พร้อมระบบจัดการฐานข้อมูลสมาชิก คลังสินค้า และประวัติการเงิน

## 🌟 ฟีเจอร์ที่โดดเด่น (Key Features)

* **🛒 Market Page:** แสดงรายการการ์ดที่มีวางขายในร้าน พร้อมรูปภาพและราคา
* **🔐 Authentication:** ระบบล็อกอินสมาชิก เพื่อเข้าถึงคลังส่วนตัว (User: `guy` / Pass: `123`)
* **💳 Digital Wallet:** ระบบกระเป๋าเงินจำลอง หักเงินจริงเมื่อมีการซื้อขาย
* **✅ Purchase Confirmation:** ระบบยืนยันการสั่งซื้อก่อนหักเงิน พร้อมระบบแจ้งเตือน (Alert) เมื่อยอดเงินไม่เพียงพอ
* **📦 Personal Inventory:** คลังเก็บการ์ดส่วนตัว การ์ดที่ซื้อแล้วจะย้ายจากหน้าร้านมาอยู่ที่นี่ทันที
* **📜 Transaction History:** บันทึกประวัติการใช้จ่ายย้อนหลัง แบ่งประเภทรายการ (ซื้อ/เติมเงิน) ชัดเจน
* **❤️ Wishlist:** ระบบเลือกเก็บการ์ดที่ชอบไว้ในรายการโปรด

## 🛠️ เทคโนโลยีที่ใช้ (Tech Stack)

* **Backend:** Python 3.10+, Flask Framework
* **Database:** SQLite (SQLAlchemy ORM)
* **Frontend:** HTML5, CSS3 (Custom Design), Bootstrap 5, Font Awesome Icons
* **Fonts:** Google Fonts (Kanit)

## 📂 โครงสร้างโปรเจกต์ (Project Structure)

```text
My-web/
├── app.py              # ไฟล์หลักควบคุม Logic และ Routes ทั้งหมด
├── data.sqlite         # ไฟล์ฐานข้อมูล (สร้างอัตโนมัติ)
├── README.md           # รายละเอียดโปรเจกต์
├── static/
│   └── css/
│       └── style.css   # ไฟล์ตกแต่งหน้าตาเว็บเพิ่มเติม
└── templates/          # โฟลเดอร์เก็บไฟล์ HTML (Jinja2)
    ├── base.html       # โครงสร้างหลักของหน้าเว็บ (Navbar/Footer)
    ├── index.html      # หน้าตลาดการ์ด
    ├── login.html      # หน้าเข้าสู่ระบบ
    ├── confirm_buy.html # หน้ากดยืนยันการชำระเงิน
    ├── inventory.html  # หน้าคลังการ์ดที่ซื้อแล้ว
    ├── history.html    # หน้าประวัติการทำรายการ
    ├── wishlist.html   # หน้าสรุปรายการที่ชอบ
    └── profile.html    # หน้าข้อมูลส่วนตัวและยอดคงเหลือ

##วิธีการรันโปรเจกต์ (How to run)
##ติดตั้ง Library:


##pip install flask flask-sqlalchemy flask-login
##จัดการพอร์ตค้าง (ถ้ามี):fuser -k 5001/tcp

##รันแอปพลิเคชัน:python app.py

##เข้าใช้งาน:
##เปิด Browser ไปที่ http://127.0.0.1:5001