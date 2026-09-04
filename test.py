from datetime import datetime
import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="jkop cafe - Smart POS", page_icon="☕", layout="wide"
)

# ----------------------------------------------------
# Session State สำหรับบันทึกยอดขายสะสมหน้าร้าน
# ----------------------------------------------------
if "total_sales" not in st.session_state:
    st.session_state.total_sales = 0.0
if "total_orders" not in st.session_state:
    st.session_state.total_orders = 0

# ----------------------------------------------------
# Sidebar: Dashboard สำหรับเจ้าของร้าน
# ----------------------------------------------------
with st.sidebar:
    st.header("📊 jkop Dashboard (เจ้าของร้าน)")
    st.metric("ยอดขายสะสมวันนี้", f"{st.session_state.total_sales:.2f} บาท")
    st.metric("จำนวนออเดอร์ทั้งหมด", f"{st.session_state.total_orders} ออเดอร์")
    st.markdown("---")
    if st.button("🔄 รีเซ็ตยอดขายสะสม"):
        st.session_state.total_sales = 0.0
        st.session_state.total_orders = 0
        st.rerun()

# ----------------------------------------------------
# Main Content
# ----------------------------------------------------
st.title("☕ jkop cafe - Smart POS & Discount System")
st.caption("ระบบคิดเงินหน้าร้านและคำนวณส่วนลดอัจฉริยะ")

# 1. รายการสินค้า
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

total_drinks, total_bakery, base_total = 0, 0, 0
order_summary = []

with col1:
    st.subheader("🥤 หมวดเครื่องดื่ม")
    for name, price in drinks_menu.items():
        qty = st.number_input(
            f"{name} ({price} บาท)", min_value=0, step=1, key=name
        )
        if qty > 0:
            total_drinks += qty
            item_total = qty * price
            base_total += item_total
            order_summary.append(f"{name} x {qty} = {item_total} บาท")

with col2:
    st.subheader("🥐 หมวดขนม / เบเกอรี")
    for name, price in bakery_menu.items():
        qty = st.number_input(
            f"{name} ({price} บาท)", min_value=0, step=1, key=name
        )
        if qty > 0:
            total_bakery += qty
            item_total = qty * price
            base_total += item_total
            order_summary.append(f"{name} x {qty} = {item_total} บาท")

st.markdown("---")

# ----------------------------------------------------
# 🔥 ไอเดียเจ๋งๆ: Smart Upsell Notification (ใช้ If-Else เช็กพฤติกรรม)
# ----------------------------------------------------
if total_drinks > 0 and total_bakery == 0:
    st.info(
        "💡 **Smart Suggestion:** ลูกค้าสั่งเครื่องดื่มแล้ว รับบราวนี่หรือครัวซองต์ไปทานคู่กันเพิ่มไหมครับ?"
    )

if 200 <= base_total < 250:
    shortage = 250 - base_total
    st.warning(
        f"🎉 **Smart Suggestion:** ซื้อสินค้าเพิ่มอีกเพียง **{shortage:.2f}** บาท จะได้รับส่วนลดพิเศษทันที 30 บาท!"
    )

st.subheader(
    f"📊 ยอดรวมเบื้องต้น: **{base_total:.2f}** บาท (เครื่องดื่ม {total_drinks} แก้ว / ขนม {total_bakery} ชิ้น)"
)

# ----------------------------------------------------
# 2. ส่วนลดและโปรโมชั่น (If-Else)
# ----------------------------------------------------
st.header("🏷️ 2. ส่วนลดและโปรโมชั่น")
col_opt1, col_opt2 = st.columns(2)

with col_opt1:
    bring_own_cup = st.checkbox(
        "🌱 ลูกค้านำแก้วมาเอง (ลด 5 บาท / แก้วเครื่องดื่ม)"
    )
with col_opt2:
    is_member = st.checkbox("💳 บัตรสมาชิก jkop Club (ลด 10% จากยอดรวม)")

discount = 0.0
discount_details = []

if bring_own_cup and total_drinks > 0:
    cup_discount = total_drinks * 5
    discount += cup_discount
    discount_details.append(
        f"🌱 ส่วนลดนำแก้วมาเอง ({total_drinks} แก้ว x 5 บาท = -{cup_discount} บาท)"
    )

if is_member and base_total > 0:
    member_discount = base_total * 0.10
    discount += member_discount
    discount_details.append(f"💳 ส่วนลดสมาชิก 10% (-{member_discount:.2f} บาท)")

if base_total >= 250:
    promo_discount = 30.0
    discount += promo_discount
    discount_details.append("🎉 โปรโมชั่นซื้อครบ 250 บาทขึ้นไป (-30 บาท)")

if discount_details:
    st.success("### รายการส่วนลดที่ได้รับ:")
    for detail in discount_details:
        st.write(f"- {detail}")

final_price = max(0.0, base_total - discount)

st.metric(
    label="💰 ยอดเงินที่ต้องจ่ายสุทธิ",
    value=f"{final_price:.2f} บาท",
    delta=f"-{discount:.2f} บาท (ส่วนลดรวม)" if discount > 0 else None,
)

# ----------------------------------------------------
# 3. รับเงินและออกใบเสร็จ (e-Receipt)
# ----------------------------------------------------
st.header("💵 3. รับเงินและคิดเงินทอน")
received_money = st.number_input(
    "กรอกจำนวนเงินที่รับจากลูกค้า (บาท)", min_value=0.0, step=10.0, value=0.0
)

total_items = total_drinks + total_bakery

if st.button("🧮 คิดเงินและพิมพ์ใบเสร็จ"):
    if total_items == 0:
        st.warning("⚠️ กรุณาเลือกสั่งสินค้าอย่างน้อย 1 รายการ")
    elif received_money < final_price:
        st.error(f"❌ เงินไม่พอ! ขาดอีก {final_price - received_money:.2f} บาท")
    else:
        change = received_money - final_price

        # บันทึกยอดขายเข้า Dashboard
        st.session_state.total_sales += final_price
        st.session_state.total_orders += 1

        st.balloons()
        st.success(
            f"✅ ชำระเงินสำเร็จ! รับเงินมา {received_money:.2f} บาท | เงินทอน {change:.2f} บาท"
        )

        # ----------------------------------------------------
        # 🔥 ไอเดียเจ๋งๆ: สร้างใบเสร็จดิจิทัล (e-Receipt)
        # ----------------------------------------------------
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        receipt_text = f"""===================================
             jkop cafe
      RECEIPT / ใบเสร็จรับเงิน
===================================
วันที่: {now}
-----------------------------------
รายการสินค้า:
"""
        for item in order_summary:
            receipt_text += f"- {item}\n"

        receipt_text += f"""-----------------------------------
ราคารวมเบื้องต้น: {base_total:.2f} บาท
ส่วนลดรวม: -{discount:.2f} บาท
ยอดเงินสุทธิ: {final_price:.2f} บาท
รับเงินมา: {received_money:.2f} บาท
เงินทอน: {change:.2f} บาท
===================================
     ขอบคุณที่ใช้บริการ jkop cafe!
===================================
"""

        # แสดงใบเสร็จในหน้าเว็บ
        st.subheader("🧾 ใบเสร็จรับเงิน (e-Receipt)")
        st.code(receipt_text, language="text")

        # ปุ่มดาวน์โหลดใบเสร็จเป็นไฟล์ .txt
        st.download_button(
            label="📥 ดาวน์โหลดใบเสร็จ (.txt)",
            data=receipt_text,
            file_name=f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
        )
