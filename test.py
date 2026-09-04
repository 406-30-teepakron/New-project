import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="jkop cafe - Smart POS", page_icon="☕", layout="wide")

st.title("☕ jkop cafe - Smart POS System")
st.caption("ระบบบริหารจัดการคิดเงินและคำนวณส่วนลดอัตโนมัติ")

# 1. กำหนดรายการสินค้าและราคา
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
topping_total = 0

# คอลัมน์ที่ 1: เครื่องดื่ม
with col1:
    st.subheader("🥤 หมวดเครื่องดื่ม")
    for name, price in drinks_menu.items():
        qty = st.number_input(f"{name} ({price} บาท)", min_value=0, step=1, key=name)
        
        if qty > 0:
            total_drinks = total_drinks + qty
            base_total = base_total + (qty * price)
            
            # ปรับแต่งท็อปปิ้งเฉพาะเมนูที่เลือก
            with st.expander(f"⚙️ ปรับแต่ง {name} (สั่ง {qty} แก้ว)"):
                sweetness = st.select_slider(
                    "ระดับความหวาน", 
                    options=["0%", "25%", "50%", "100%", "120%"], 
                    value="100%", 
                    key="sweet_" + name
                )
                
                boba_qty = st.number_input(
                    "🧋 เพิ่มไข่มุก (+10 บ.) [จำนวนแก้ว]", 
                    min_value=0, max_value=qty, key="boba_" + name
                )
                whip_qty = st.number_input(
                    "🍦 เพิ่มวิปครีม (+15 บ.) [จำนวนแก้ว]", 
                    min_value=0, max_value=qty, key="whip_" + name
                )
                shot_qty = st.number_input(
                    "☕ เพิ่มช็อตกาแฟ (+20 บ.) [จำนวนแก้ว]", 
                    min_value=0, max_value=qty, key="shot_" + name
                )
                
                topping_total = topping_total + (boba_qty * 10) + (whip_qty * 15) + (shot_qty * 20)

# คอลัมน์ที่ 2: ขนม / เบเกอรี
with col2:
    st.subheader("🥐 หมวดขนม / เบเกอรี")
    for name, price in bakery_menu.items():
        qty = st.number_input(f"{name} ({price} บาท)", min_value=0, step=1, key=name)
        if qty > 0:
            total_bakery = total_bakery + qty
            base_total = base_total + (qty * price)

# รวมค่าท็อปปิ้งเข้ากับราคารวมเบื้องต้น
base_total = base_total + topping_total
st.markdown("---")

# ระบบแนะนำสินค้า (Smart Suggestion)
if total_drinks > 0 and total_bakery == 0:
    st.info("💡 **Smart Suggestion:** รับบราวนี่หรือครัวซองต์อบร้อนๆ ไปทานคู่กับเครื่องดื่มเพิ่มไหมครับ?")

if base_total >= 200 and base_total < 250:
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
if bring_own_cup == True and total_drinks > 0:
    cup_discount = total_drinks * 5
    discount = discount + cup_discount
    discount_details.append(f"🌱 ส่วนลดนำแก้วมาเอง ({total_drinks} แก้ว = -{cup_discount} บาท)")

# เงื่อนไขที่ 2: สมาชิก (เช็กด้วย If-Elif-Else ชัดเจน)
if member_tier == "Silver Member (ลด 5%)":
    mem_disc = base_total * 0.05
    discount = discount + mem_disc
    discount_details.append(f"💳 ส่วนลด Silver Member 5% (-{mem_disc:.2f} บาท)")
elif member_tier == "Gold Member (ลด 10%)":
    mem_disc = base_total * 0.10
    discount = discount + mem_disc
    discount_details.append(f"💳 ส่วนลด Gold Member 10% (-{mem_disc:.2f} บาท)")
elif member_tier == "Platinum Member (ลด 15%)":
    mem_disc = base_total * 0.15
    discount = discount + mem_disc
    discount_details.append(f"💳 ส่วนลด Platinum Member 15% (-{mem_disc:.2f} บาท)")

# เงื่อนไขที่ 3: ซื้อครบ 250 บาท
if base_total >= 250:
    promo_discount = 30.0
    discount = discount + promo_discount
    discount_details.append("🎉 โปรโมชั่นซื้อครบ 250 บาทขึ้นไป (-30 บาท)")

# แสดงรายการส่วนลดที่ได้รับ
if len(discount_details) > 0:
    st.success("### รายการส่วนลดที่ได้รับ:")
    for detail in discount_details:
        st.write("- " + detail)

# คำนวณราคาหลังหักส่วนลด (ไม่ให้ติดลบ)
price_after_discount = base_total - discount
if price_after_discount < 0:
    price_after_discount = 0.0

# คำนวณภาษี VAT 7%
vat = price_after_discount * 0.07
final_price = price_after_discount + vat

st.write(f"**ส่วนลดรวมทั้งหมด:** -{discount:.2f} บาท")
st.write(f"**ภาษีมูลค่าเพิ่ม (VAT 7%):** +{vat:.2f} บาท")
st.subheader(f"💰 ยอดเงินที่ต้องจ่ายสุทธิ: {final_price:.2f} บาท")

# 3. รับเงินและคิดเงินทอน
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
