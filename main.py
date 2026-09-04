import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="jkop cafe POS", page_icon="☕", layout="wide")

st.title("☕ jkop cafe - Smart POS & Discount System")
st.caption("ระบบคิดเงินและคำนวณส่วนลดร้านกาแฟ (แอปพลิเคชันสำหรับ Smart Shop)")

# ----------------------------------------------------
# 1. รายการสินค้า (หมวดเครื่องดื่ม และ เบเกอรี)
# ----------------------------------------------------
drinks_menu = {
    "☕ เอสเปรสโซร้อน (Hot Espresso)": 45,
    "🧊 อเมริกาโนเย็น (Iced Americano)": 50,
    "🧋 ชานมไต้หวัน (Taiwan Milk Tea)": 55,
    "🧋 ชาไทยเย็น (Iced Thai Tea)": 50,
    "🍵 ชาเขียวมัจฉะ (Matcha Green Tea)": 65,
    "🍎 ชาผลไม้รวม (Mixed Fruit Tea)": 60,
}

bakery_menu = {
    "🍰 เค้กช็อกโกแลต (Chocolate Cake)": 75,
    "🍫 บราวนี่ (Brownie)": 45,
    "🍪 คุกกี้ช็อกโกแลตชิพ (Cookie)": 35,
    "🥐 ครัวซองต์เนยสด (Croissant)": 55,
}

st.header("📋 1. เลือกเมนูสินค้า")

col1, col2 = st.columns(2)

total_drinks = 0
total_bakery = 0
base_total = 0

# คอลัมน์ที่ 1: เครื่องดื่ม
with col1:
    st.subheader("🥤 หมวดเครื่องดื่ม")
    for name, price in drinks_menu.items():
        qty = st.number_input(f"{name} ({price} บาท)", min_value=0, step=1, key=name)
        total_drinks += qty
        base_total += qty * price

# คอลัมน์ที่ 2: ขนม / เบเกอรี
with col2:
    st.subheader("🥐 หมวดขนม / เบเกอรี")
    for name, price in bakery_menu.items():
        qty = st.number_input(f"{name} ({price} บาท)", min_value=0, step=1, key=name)
        total_bakery += qty
        base_total += qty * price

st.markdown("---")
st.subheader(
    f"📊 สรุปรายการ: เครื่องดื่ม **{total_drinks}** แก้ว | ขนม **{total_bakery}** ชิ้น | ราคารวมเบื้องต้น: **{base_total:.2f}** บาท"
)

# ----------------------------------------------------
# 2. เงื่อนไขส่วนลด (If-Else)
# ----------------------------------------------------
st.header("🏷️ 2. ส่วนลดและโปรโมชั่น")

col_opt1, col_opt2 = st.columns(2)

with col_opt1:
    bring_own_cup = st.checkbox("🌱 ลูกค้านำแก้วมาเอง (ลด 5 บาท / แก้วเครื่องดื่ม)")

with col_opt2:
    is_member = st.checkbox("💳 บัตรสมาชิก jkop Club (ลด 10% จากยอดรวม)")

# คำนวณส่วนลดตามเงื่อนไข If-Else
discount = 0.0
discount_details = []

# เงื่อนไขที่ 1: ถ้าเอาแก้วมาเอง ลด 5 บาทต่อแก้วเครื่องดื่ม
if bring_own_cup and total_drinks > 0:
    cup_discount = total_drinks * 5
    discount += cup_discount
    discount_details.append(f"🌱 ส่วนลดนำแก้วมาเอง ({total_drinks} แก้ว x 5 บาท = -{cup_discount} บาท)")

# เงื่อนไขที่ 2: ถ้าเป็นสมาชิก ลด 10% จากยอดรวม
if is_member and base_total > 0:
    member_discount = base_total * 0.10
    discount += member_discount
    discount_details.append(f"💳 ส่วนลดสมาชิก 10% (-{member_discount:.2f} บาท)")

# เงื่อนไขที่ 3: โปรโมชั่นซื้อครบ 250 บาท ลดเพิ่ม 30 บาท
if base_total >= 250:
    promo_discount = 30.0
    discount += promo_discount
    discount_details.append("🎉 โปรโมชั่นซื้อครบ 250 บาทขึ้นไป (-30 บาท)")

# แสดงรายละเอียดส่วนลดที่ได้รับ
if discount_details:
    st.success("### รายการส่วนลดที่ได้รับ:")
    for detail in discount_details:
        st.write(f"- {detail}")
else:
    st.info("ไม่มีส่วนลดที่นำมาใช้")

# คำนวณยอดเงินสุทธิที่ต้องจ่ายจริง
final_price = base_total - discount
if final_price < 0:
    final_price = 0.0

st.markdown("---")
st.metric(
    label="💰 ยอดเงินที่ต้องจ่ายสุทธิ", 
    value=f"{final_price:.2f} บาท", 
    delta=f"-{discount:.2f} บาท (ส่วนลดรวม)" if discount > 0 else None
)

# ----------------------------------------------------
# 3. รับเงินและคำนวณเงินทอน
# ----------------------------------------------------
st.header("💵 3. รับเงินและคิดเงินทอน")

received_money = st.number_input("กรอกจำนวนเงินที่รับจากลูกค้า (บาท)", min_value=0.0, step=10.0, value=0.0)

total_items = total_drinks + total_bakery

if st.button("🧮 คำนวณเงินทอน"):
    if total_items == 0:
        st.warning("⚠️ กรุณาเลือกสั่งสินค้าอย่างน้อย 1 รายการ")
    elif received_money < final_price:
        st.error(f"❌ เงินไม่พอ! ขาดอีก {final_price - received_money:.2f} บาท")
    else:
        change = received_money - final_price
        st.balloons()
        st.success(f"✅ ชำระเงินสำเร็จ! รับเงินมา {received_money:.2f} บาท")
        st.subheader(f"🪙 เงินทอน: **{change:.2f}** บาท")
