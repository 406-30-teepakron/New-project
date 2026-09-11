import streamlit as st

st.set_page_config(page_title="Top cafe - POS", page_icon="☕", layout="wide")

st.title("☕ Top cafe - POS System")
st.caption("ระบบบริหารจัดการ POS คิดเงินและส่วนลด")

coffee_menu = {
    "☕ เอสเปรสโซร้อน (Hot Espresso)": 50,
    "🧊 อเมริกาโนเย็น (Iced Americano)": 60,
    "🥛 ลาเต้เย็น (Iced Latte)": 70,
    "☕ คาปูชิโนเย็น (Iced Cappuccino)": 70,
    "🍫 มอคค่าเย็น (Iced Mocha)": 75,
    "🍯 คาราเมลมัคคิอาโต (Caramel Macchiato)": 85,
    "🍊 กาแฟส้มสด (Orange Espresso)": 85,
    "🥥 กาแฟมะพร้าวน้ำหอม (Coconut Latte)": 85,
    "🍋 เอสเปรสโซยูซุโซดา (Yuzu Espresso Soda)": 90,
    "🥛 เดอร์ตี้คอฟฟี่ (Dirty Coffee)": 95,
    "🧊 คอลด์บรูว์สกัดเย็น (Cold Brew)": 80,
    "🧂 ซอลท์เทดคาราเมลโคลด์บรูว์ (Salted Caramel Cold Brew)": 95,
}

tea_milk_menu = {
    "🧋 ชาไทยต้นตำรับ (Traditional Thai Milk Tea)": 55,
    "🍵 ชาเขียวมัจฉะลาเต้ (Matcha Latte)": 75,
    "🧋 ชานมไต้หวันบราวน์ซูการ์ (Taiwan Brown Sugar Milk Tea)": 70,
    "🍵 โฮจิฉะคั่วลาเต้ (Hojicha Latte)": 80,
    "🍎 ชาผลไม้สกัดสด (Mixed Fruit Tea)": 65,
    "🍋 ชาไทยเลมอนฮันนี่ (Honey Lemon Thai Tea)": 60,
    "🍑 ชามัสกัตพีช (Muscat Peach Tea)": 70,
    "🌸 ชานมนมชมพูซากุระ (Sakura Milk Tea)": 65,
    "🍫 โกโก้พรีเมียมเข้มข้น (Dutch Dark Cocoa)": 70,
    "🥛 นมสดฮอกไกโดคาราเมล (Hokkaido Caramel Milk)": 65,
    "🍵 ชามะลิใสเย็น (Jasmine Green Tea)": 50,
    "🧋 ชานมชีสโฟม (Cheese Foam Milk Tea)": 85,
}

frappe_soda_menu = {
    "☕ กาแฟปั่นพรีเมียม (Coffee Frappe)": 85,
    "🍫 ช็อกโกแลตปั่นวิปครีม (Chocolate Cream Frappe)": 85,
    "🍵 มัจฉะปั่นถั่วแดง (Matcha Red Bean Frappe)": 95,
    "🍓 สตรอว์เบอร์รีโยเกิร์ตปั่น (Strawberry Yogurt Smoothie)": 85,
    "🥭 มะม่วงเสาวรสปั่น (Mango Passionfruit Smoothie)": 85,
    "🫐 บลูเบอร์รีโยเกิร์ตปั่น (Blueberry Yogurt Smoothie)": 85,
    "🥑 อะโวคาโดปั่นฮันนี่ (Avocado Honey Milkshake)": 95,
    "🍓 สตรอว์เบอร์รีสปาร์กลิ้งโซดา (Strawberry Soda)": 60,
    "🍊 ยูซุฮันนี่โซดา (Yuzu Honey Soda)": 65,
    "🍑 พีชเจลลีโซดา (Peach Jelly Soda)": 65,
    "🌊 บลูฮาวายไลม์โซดา (Blue Hawaii Soda)": 60,
}

cake_menu = {
    "🍫 เค้กช็อกโกแลตฟัดจ์ (Chocolate Fudge Cake)": 95,
    "🧀 ชีสเค้กหน้าไหม้สไตล์บาสก์ (Basque Burnt Cheesecake)": 115,
    "🍓 สตรอว์เบอร์รีชอร์ตเค้ก (Strawberry Shortcake)": 120,
    "🍌 บานอฟฟี่พายครีมสด (Banoffee Pie)": 95,
    "🫐 บลูเบอร์รีชีสพาย (Blueberry Cheese Pie)": 95,
    "🥕 เค้กแครอทวอลนัท (Carrot Walnut Cake)": 105,
    "🍰 เค้กเรดเวลเวท (Red Velvet Cake)": 95,
    "🍊 เค้กส้มลาวา (Orange Lava Cake)": 85,
    "🥥 เค้กมะพร้าวอ่อนนุ่ม (Young Coconut Cake)": 95,
    "🍰 เครปเค้กเวรี่เบอร์รี (Mille Crepe Berry)": 105,
}

bakery_toast_menu = {
    "🍞 ชิบุยาฮันนี่โทสต์ (Shibuya Honey Toast)": 189,
    "🧇 ครัฟเฟิลเนยสดออริจินัล (Original Croffle)": 75,
    "🧇 ครัฟเฟิลนูเทลล่ากล้วย (Nutella Banana Croffle)": 95,
    "🥐 ครัวซองต์เนยสดฝรั่งเศส (French Butter Croissant)": 70,
    "🥐 ครัวซองต์อัลมอนด์ (Almond Croissant)": 90,
    "🥐 ครัวซองต์ช็อกโกแลตลาวา (Choco Lava Croissant)": 95,
    "🧄 ขนมปังโชกุปังกระเทียมชีส (Garlic Cheese Shokupan)": 85,
    "🥐 ชินนามอนม้วนลูกเกด (Cinnamon Raisin Roll)": 75,
    "🧁 สคอนเนยสดพร้อมแยมสตรอว์เบอร์รี (Scone w/ Jam)": 65,
    "🍪 ซอฟต์คุกกี้ช็อกโกแลตชิพ (Soft Chocolate Chip Cookie)": 50,
}

snack_menu = {
    "🥪 แซนด์วิชแฮมชีสโอบเบคอน (Ham Cheese Bacon Sandwich)": 85,
    "🥐 ครัวซองต์แซนด์วิชทูน่า (Tuna Croissant Sandwich)": 95,
    "🥐 ครัวซองต์ผักโขมอบชีส (Spinach Cheese Croissant)": 95,
    "🍟 เฟรนช์ฟรายส์ดิปชีส (French Fries w/ Cheese Dip)": 79,
    "🍗 นักเก็ตไก่ซอสบาร์บีคิว (Chicken Nuggets)": 79,
    "🍗 ปีกไก่ทอดสไตล์นิวออร์ลีนส์ (New Orleans Wings)": 99,
    "🧀 ชีสสติ๊กทอดกรอบ (Mozzarella Cheese Sticks)": 89,
}

def process_drink_category(menu_dict):
    c_drinks, c_base, c_topping = 0, 0, 0
    for name, price in menu_dict.items():
        qty = st.number_input(f"{name} ({price} บาท)", min_value=0, step=1, key=name)
        if qty > 0:
            c_drinks += qty
            c_base += qty * price
            
            with st.expander(f"⚙️ ปรับแต่ง {name} (สั่ง {qty} แก้ว)"):
                st.select_slider("ระดับความหวาน", options=["0%", "25%", "50%", "100%", "120%"], value="100%", key="sweet_" + name)
                boba = st.number_input("🧋 เพิ่มไข่มุกบราวน์ซูการ์ (+10 บ.)", min_value=0, max_value=qty, key="boba_" + name)
                whip = st.number_input("🍦 เพิ่มวิปครีมเนื้อนุ่ม (+15 บ.)", min_value=0, max_value=qty, key="whip_" + name)
                shot = st.number_input("☕ เพิ่มช็อตเอสเปรสโซ (+20 บ.)", min_value=0, max_value=qty, key="shot_" + name)
                cheese = st.number_input("🧀 เพิ่มครีมชีสโฟม (+15 บ.)", min_value=0, max_value=qty, key="cheese_" + name)
                
                c_topping += (boba * 10) + (whip * 15) + (shot * 20) + (cheese * 15)
    return c_drinks, c_base, c_topping

def process_food_category(menu_dict):
    c_food, c_base = 0, 0
    for name, price in menu_dict.items():
        qty = st.number_input(f"{name} ({price} บาท)", min_value=0, step=1, key=name)
        if qty > 0:
            c_food += qty
            c_base += qty * price
    return c_food, c_base

st.header("📋 1. เลือกเมนูสินค้า")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "☕ กาแฟ", 
    "🍵 ชา & นมสด", 
    "🥤 ปั่น & โซดา", 
    "🍰 เค้ก & พาย", 
    "🍞 เบเกอรี & โทสต์", 
    "🥪 อาหารว่าง & ของทอด"
])

total_drinks, total_food, base_total, topping_total = 0, 0, 0, 0

with tab1:
    d, b, t = process_drink_category(coffee_menu)
    total_drinks += d; base_total += b; topping_total += t

with tab2:
    d, b, t = process_drink_category(tea_milk_menu)
    total_drinks += d; base_total += b; topping_total += t

with tab3:
    d, b, t = process_drink_category(frappe_soda_menu)
    total_drinks += d; base_total += b; topping_total += t

with tab4:
    f, b = process_food_category(cake_menu)
    total_food += f; base_total += b

with tab5:
    f, b = process_food_category(bakery_toast_menu)
    total_food += f; base_total += b

with tab6:
    f, b = process_food_category(snack_menu)
    total_food += f; base_total += b

base_total += topping_total
st.markdown("---")

if total_drinks > 0 and total_food == 0:
    st.info("💡 **Smart Suggestion:** รับของทานเล่นคู่กันไหมครับ? แนะนำ **ชิบุยาฮันนี่โทสต์**, **ชีสเค้กหน้าไหม้** หรือ **ครึ่งวงครัวซองต์เนยสด** อบร้อนๆ ทานคู่กับเครื่องดื่มเข้ากันมากครับ!")
elif total_food > 0 and total_drinks == 0:
    st.info("💡 **Smart Suggestion:** รับเครื่องดื่มตัดเลี่ยนสักแก้วไหมครับ? แนะนำ **เอสเปรสโซส้มสด**, **ชาไทยต้นตำรับ** หรือ **ยูซุฮันนี่โซดา** เพิ่มความสดชื่นครับ!")
elif total_drinks >= 3 and total_food < 2:
    st.info("💡 **Smart Suggestion:** สั่งเครื่องดื่มหลายแก้ว รับชุด **ของทานเล่น (เฟรนช์ฟรายส์ดิปชีส / นักเก็ตไก่)** ไปทานร่วมกันไหมครับ?")

if 200 <= base_total < 300:
    shortage = 300 - base_total
    st.warning(f"🎉 **Smart Suggestion:** ยอดซื้อขณะนี้ {base_total:.2f} บาท สั่งเพิ่มอีกเพียง **{shortage:.2f}** บาท จะได้รับส่วนลดพิเศษทันที 40 บาท (เมื่อครบ 300 บาท)!")

st.subheader(f"📊 ยอดรวมเบื้องต้น: **{base_total:.2f}** บาท (รวมค่าท็อปปิ้ง {topping_total} บาท)")

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

if bring_own_cup == True and total_drinks > 0:
    cup_discount = total_drinks * 5
    discount += cup_discount
    discount_details.append(f"🌱 ส่วนลดนำแก้วมาเอง ({total_drinks} แก้ว = -{cup_discount} บาท)")

if member_tier == "Silver Member (ลด 5%)":
    mem_disc = base_total * 0.05
    discount += mem_disc
    discount_details.append(f"💳 ส่วนลด Silver Member 5% (-{mem_disc:.2f} บาท)")
elif member_tier == "Gold Member (ลด 10%)":
    mem_disc = base_total * 0.10
    discount += mem_disc
    discount_details.append(f"💳 ส่วนลด Gold Member 10% (-{mem_disc:.2f} บาท)")
elif member_tier == "Platinum Member (ลด 15%)":
    mem_disc = base_total * 0.15
    discount += mem_disc
    discount_details.append(f"💳 ส่วนลด Platinum Member 15% (-{mem_disc:.2f} บาท)")

if base_total >= 300:
    promo_discount = 40.0
    discount += promo_discount
    discount_details.append("🎉 โปรโมชั่นซื้อครบ 300 บาทขึ้นไป (-40 บาท)")

if len(discount_details) > 0:
    st.success("### รายการส่วนลดที่ได้รับ:")
    for detail in discount_details:
        st.write("- " + detail)

price_after_discount = base_total - discount
if price_after_discount < 0:
    price_after_discount = 0.0

vat = price_after_discount * 0.07
final_price = price_after_discount + vat

st.write(f"**ส่วนลดรวมทั้งหมด:** -{discount:.2f} บาท")
st.write(f"**ภาษีมูลค่าเพิ่ม (VAT 7%):** +{vat:.2f} บาท")
st.subheader(f"💰 ยอดเงินที่ต้องจ่ายสุทธิ: {final_price:.2f} บาท")

st.header("💵 3. รับเงินและคิดเงินทอน")
received_money = st.number_input("กรอกจำนวนเงินที่รับจากลูกค้า (บาท)", min_value=0.0, step=20.0, value=0.0)

total_items = total_drinks + total_food

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
