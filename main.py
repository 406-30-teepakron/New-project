import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="jkop cafe POS", page_icon="☕", layout="wide")

st.title("☕ jkop cafe - Smart POS & Discount System")
st.caption("ระบบคิดเงินและคำนวณส่วนลดร้านกาแฟ (แอปพลิเคชันสำหรับ Smart Shop)")

# ----------------------------------------------------
# 1. รายการสินค้า 10 เมนูเครื่องดื่ม
# ----------------------------------------------------
menu_items = {
    "☕ เอสเปรสโซร้อน (Hot Espresso)": 45,
    "🧊 อเมริกาโนเย็น (Iced Americano)": 50,
    "🥛 ลาเต้เย็น (Iced Latte)": 60,
    "🥤 คาปูชิโนเย็น (Iced Cappuccino)": 60,
    "🍵 มัจฉะลาเต้เย็น (Iced Matcha Latte)": 65,
    "🧋 ชาไทยเย็น (Iced Thai Tea)": 50,
    "🍃 ชาเขียวนมเย็น (Iced Green Tea)": 50,
    "🍫 โกโก้เย็น (Iced Cocoa)": 55,
    "🍮 นมสดคาราเมล (Caramel Fresh Milk)": 55,
    "🍓 สตรอว์เบอร์รีสมูทตี้ (Strawberry Smoothie)": 70
}

st.header("📋 1. เลือกเมนูเครื่องดื่ม (10 เมนู)")

# จัดวางเมนูแบ่งเป็น 2 คอลัมน์
col1, col2 = st.columns(2)

total_cups = 0
base_total = 0

items_list = list(menu_items.items())
half = len(items_list) // 2

# คอลัมน์ที่ 1 (เมนูที่ 1 - 5)
with col1:
    for name, price in items_list[:half]:
        qty = st.number_input(f"{name} ({price} บาท)", min_value=0, step=1, key=name)
        total_cups += qty
        base_total += qty * price

# คอลัมน์ที่ 2 (เมนูที่ 6 - 10)
with col2:
    for name, price in items_list[half:]:
        qty = st.number_input(f"{name} ({price} บาท)", min_value=0, step=1, key=name)
        total_cups += qty
        base_total += qty * price

st.markdown("---")
st.subheader(f"📊 สรุปรายการ: **{total_cups}** แก้ว | ราคารวมเบื้องต้น: **{base_total:.2f}** บาท")

# ----------------------------------------------------
# 2. เงื่อนไขส่วนลด (If-Else)
# ----------------------------------------------------
st.header("🏷️ 2. ส่วนลดและโปรโมชั่น")

col_opt1, col_opt2 = st.columns(2)

with col_opt1:
    bring_own_cup = st.checkbox("🌱 ลูกค้านำแก้วมาเอง (ลด 5 บาท / แก้ว)")

with col_opt2:
    is_member = st.checkbox("💳 บัตรสมาชิก jkop Club (ลด 10% จากยอดรวม)")

# คำนวณส่วนลดตามเงื่อนไข If-Else
discount = 0.0
discount_details = []

# เงื่อนไขที่ 1: ถ้าเอาแก้วมาเอง ลด 5 บาทต่อแก้ว
if bring_own_cup and total_cups > 0:
    cup_discount = total_cups * 5
    discount += cup_discount
    discount_details.append(f"🌱 ส่วนลดนำแก้วมาเอง ({total_cups} แก้ว x 5 บาท = -{cup_discount} บาท)")

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

if st.button("🧮 คำนวณเงินทอน"):
    if total_cups == 0:
        st.warning("⚠️ กรุณาเลือกสั่งเครื่องดื่มอย่างน้อย 1 แก้ว")
    elif received_money < final_price:
        st.error(f"❌ เงินไม่พอ! ขาดอีก {final_price - received_money:.2f} บาท")
    else:
        change = received_money - final_price
        st.balloons()
        st.success(f"✅ ชำระเงินสำเร็จ! รับเงินมา {received_money:.2f} บาท")
        st.subheader(f"🪙 เงินทอน: **{change:.2f}** บาท")
