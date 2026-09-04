import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="jkop cafe - Ultimate POS", page_icon="☕", layout="wide")

# ----------------------------------------------------
# Session State สำหรับระบบคิว ยอดขาย และสต็อกสินค้า
# ----------------------------------------------------
if "total_sales" not in st.session_state:
    st.session_state.total_sales = 0.0
if "total_orders" not in st.session_state:
    st.session_state.total_orders = 0
if "queue_no" not in st.session_state:
    st.session_state.queue_no = 1

# จำกัดสต็อกสินค้าประจำวัน
if "stock" not in st.session_state:
    st.session_state.stock = {
        "🍰 เค้กช็อกโกแลต (Chocolate Cake)": 8,
        "🍫 บราวนี่ (Brownie)": 5,
        "🍪 คุกกี้ช็อกโกแลตชิพ (Cookie)": 10,
        "🥐 ครัวซองต์เนยสด (Croissant)": 5,
    }

# ----------------------------------------------------
# Sidebar: Dashboard สำหรับเจ้าของร้าน & สต็อก
# ----------------------------------------------------
with st.sidebar:
    st.header("📊 jkop Dashboard (เจ้าของร้าน)")
    st.metric("ยอดขายสะสมวันนี้", f"{st.session_state.total_sales:.2f} บาท")
    st.metric("จำนวนออเดอร์ทั้งหมด", f"{st.session_state.total_orders} ออเดอร์")
    st.metric("คิวปัจจุบัน", f"Q-{st.session_state.queue_no:03d}")
    
    st.markdown("---")
    st.subheader("📦 สต็อกขนมคงเหลือ")
    for item, qty in st.session_state.stock.items():
        st.write(f"- {item.split(' (')[0]}: **{qty}** ชิ้น")
        
    st.markdown("---")
    if st.button("🔄 รีเซ็ตระบบทั้งหมด"):
        st.session_state.total_sales = 0.0
        st.session_state.total_orders = 0
        st.session_state.queue_no = 1
        st.session_state.stock = {
            "🍰 เค้กช็อกโกแลต (Chocolate Cake)": 8,
            "🍫 บราวนี่ (Brownie)": 5,
            "🍪 คุกกี้ช็อกโกแลตชิพ (Cookie)": 10,
            "🥐 ครัวซองต์เนยสด (Croissant)": 5,
        }
        st.rerun()

# ----------------------------------------------------
# Main Content
# ----------------------------------------------------
st.title("☕ jkop cafe - Smart POS & Management System")
st.caption("ระบบบริหารจัดการคิดเงิน คำนวณภาษี และรันคิวอัตโนมัติ")

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
topping_total = 0
stock_error = False

with col1:
    st.subheader("🥤 หมวดเครื่องดื่ม")
    for name, price in drinks_menu.items():
        qty = st.number_input(f"{name} ({price} บาท)", min_value=0, step=1, key=name)
        if qty > 0:
            total_drinks += qty
            base_total += qty * price

    if total_drinks > 0:
        with st.expander("🛠️ ปรับแต่งเครื่องดื่ม (Sweetness & Toppings)"):
            st.select_slider("ระดับความหวาน", options=["0%", "25%", "50%", "100%", "120%"], value="100%")
            st.write("ท็อปปิ้งเพิ่มเติม:")
            if st.checkbox("🧋 เพิ่มไข่มุก (+10 บาท/แก้ว)"):
                topping_total += total_drinks * 10
            if st.checkbox("🍦 เพิ่มวิปครีม (+15 บาท/แก้ว)"):
                topping_total += total_drinks * 15
            if st.checkbox("☕ เพิ่มช็อตกาแฟ (+20 บาท/แก้ว)"):
                topping_total += total_drinks * 20

with col2:
    st.subheader("🥐 หมวดขนม / เบเกอรี")
    for name, price in bakery_menu.items():
        max_limit = st.session_state.stock[name]
        qty = st.number_input(
            f"{name} ({price} บาท) [เหลือ {max_limit}]", 
            min_value=0, 
            max_value=max_limit, 
            step=1, 
            key=name
        )
        if qty > max_limit:
            st.error(f"❌ {name} สินค้าไม่พอ!")
            stock_error = True
        if qty > 0:
            total_bakery += qty
            base_total += qty * price

base_total += topping_total
st.markdown("---")

# Smart Suggestion (Upsell)
if total_drinks > 0 and total_bakery == 0:
    st.info("💡 **Smart Suggestion:** รับบราวนี่หรือครัวซองต์อบร้อนๆ ไปทานคู่กับเครื่องดื่มเพิ่มไหมครับ?")

if 200 <= base_total < 250:
    shortage = 250 - base_total
    st.warning(f"🎉 **Smart Suggestion:** สั่งเพิ่มอีกเพียง **{shortage:.2f}** บาท จะได้รับส่วนลดพิเศษทันที 30 บาท!")

st.subheader(f"📊 ยอดรวมเบื้องต้น: **{base_total:.2f}** บาท (รวมค่าท็อปปิ้ง {topping_total} บาท)")

# 2. ส่วนลดและโปรโมชั่น (If-Elif-Else)
st.header("🏷️ 2. ส่วนลดและระดับสมาชิก")
col_opt1, col_opt2 = st.columns(2)

with col_opt1:
    bring_own_cup = st.checkbox("🌱 ลูกค้านำแก้วมาเอง (ลด 5 บาท / แก้วเครื่องดื่ม)")

with col_opt2:
    member_tier = st.selectbox(
        "💳 ระดับบัตรสมาชิก jkop Club",
        ["บุคคลทั่วไป (ไม่มีส่วนลด)", "Silver Member (ลด 5%)", "Gold Member (ลด 10%)", "Platinum Member (ลด 15%)"]
    )

discount = 0.0
discount_details = []

# เงื่อนไขที่ 1: นำแก้วมาเอง
if bring_own_cup and total_drinks > 0:
    cup_discount = total_drinks * 5
    discount += cup_discount
    discount_details.append(f"🌱 ส่วนลดนำแก้วมาเอง ({total_drinks} แก้ว = -{cup_discount} บาท)")

# เงื่อนไขที่ 2: ระดับสมาชิก (If-Elif-Else)
if "Silver" in member_tier:
    mem_disc = base_total * 0.05
    discount += mem_disc
    discount_details.append(f"💳 ส่วนลด Silver Member 5% (-{mem_disc:.2f} บาท)")
elif "Gold" in member_tier:
    mem_disc = base_total * 0.10
    discount += mem_disc
    discount_details.append(f"💳 ส่วนลด Gold Member 10% (-{mem_disc:.2f} บาท)")
elif "Platinum" in member_tier:
    mem_disc = base_total * 0.15
    discount += mem_disc
    discount_details.append(f"💳 ส่วนลด Platinum Member 15% (-{mem_disc:.2f} บาท)")

# เงื่อนไขที่ 3: ซื้อครบ 250 บาท
if base_total >= 250:
    promo_discount = 30.0
    discount += promo_discount
    discount_details.append("🎉 โปรโมชั่นซื้อครบ 250 บาทขึ้นไป (-30 บาท)")

if discount_details:
    st.success("### รายการส่วนลดที่ได้รับ:")
    for detail in discount_details:
        st.write(f"- {detail}")

price_after_discount = max(0.0, base_total - discount)

# คำนวณภาษี VAT 7%
vat = price_after_discount * 0.07
final_price = price_after_discount + vat

col_calc1, col_calc2, col_calc3 = st.columns(3)
col_calc1.metric("ส่วนลดรวม", f"-{discount:.2f} บาท")
col_calc2.metric("ภาษีมูลค่าเพิ่ม (VAT 7%)", f"+{vat:.2f} บาท")
col_calc3.metric("💰 ยอดเงินที่ต้องจ่ายสุทธิ", f"{final_price:.2f} บาท")

# 3. รับเงิน คิดเงินทอน และออกคิว
st.header("💵 3. รับเงิน คิดเงินทอน และออกคิว")
received_money = st.number_input("กรอกจำนวนเงินที่รับจากลูกค้า (บาท)", min_value=0.0, step=10.0, value=0.0)

total_items = total_drinks + total_bakery

if st.button("🧮 คิดเงินและออกคิว"):
    if stock_error:
        st.error("⚠️ ไม่สามารถทำรายการได้เนื่องจากสินค้าในสต็อกไม่พอ")
    elif total_items == 0:
        st.warning("⚠️ กรุณาเลือกสั่งสินค้าอย่างน้อย 1 รายการ")
    elif received_money < final_price:
        st.error(f"❌ เงินไม่พอ! ขาดอีก {final_price - received_money:.2f} บาท")
    else:
        change = received_money - final_price
        
        # ตัดสต็อกขนม
        for name in bakery_menu.keys():
            st.session_state.stock[name] -= st.session_state[name]
        
        # อัปเดตยอดขายและคิว
        st.session_state.total_sales += final_price
        st.session_state.total_orders += 1
        current_q = f"Q-{st.session_state.queue_no:03d}"
        st.session_state.queue_no += 1
        
        st.balloons()
        st.success(f"✅ ชำระเงินสำเร็จ! รับเงินมา {received_money:.2f} บาท | เงินทอน {change:.2f} บาท")
        
        # แสดงหมายเลขคิวขนาดใหญ่
        st.markdown(f"### 🎟️ หมายเลขคิวของคุณ: **{current_q}**")
        st.info("กรุณารอเรียกคิวสักครู่ ขอบคุณครับ!")
