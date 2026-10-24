import itertools
import sympy as sp
import pandas as pd
import streamlit as st

# =========================================================
# 1. Page Config & Pastel Pink CSS Styling
# =========================================================
st.set_page_config(
    page_title="Math Logic Learning & Solver",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Main Background & Fonts */
    .stApp {
        background-color: #FFF5F7;
        color: #4A3E3D;
        font-family: 'Sarabun', sans-serif;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FDE8ED !important;
        border-right: 1px solid #F8C8D4;
    }

    /* Header Cards */
    .main-title-box {
        background: linear-gradient(135deg, #F8BBD0 0%, #F48FB1 100%);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        color: #FFFFFF;
        box-shadow: 0 4px 15px rgba(244, 143, 177, 0.3);
        margin-bottom: 25px;
    }
    
    .main-title-text {
        font-size: 26px;
        font-weight: 800;
        margin: 0;
    }

    /* Content Cards */
    .content-card {
        background-color: #FFFFFF;
        border: 1px solid #F8C8D4;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    /* Challenge Box (เหมือนการ์ดสีน้ำเงินในรูปตัวอย่างแต่เปลี่ยนเป็นชมพู) */
    .challenge-card {
        background: linear-gradient(135deg, #EC407A 0%, #D81B60 100%);
        border-radius: 14px;
        padding: 22px;
        color: #FFFFFF;
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 20px;
        box-shadow: 0 6px 18px rgba(216, 27, 96, 0.25);
    }

    /* Solution Box */
    .solution-box {
        background-color: #FCE4EC;
        border-left: 4px solid #EC407A;
        padding: 15px;
        border-radius: 8px;
        color: #880E4F;
        margin-top: 10px;
    }

    /* Sidebar Radio Options Styling */
    div[data-testid="stSidebarUserContent"] .stRadio label {
        font-size: 15px;
        font-weight: 500;
        color: #5D4037;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. Sidebar Navigation (โครงสร้างตรงตามรูปภาพตัวอย่าง)
# =========================================================
st.sidebar.title("🌸 Math Logic")
st.sidebar.caption("สื่อการเรียนรู้ตรรกศาสตร์เชิงคณิตศาสตร์")

# รายการเมนูย่อยเรียงยาวตามโครงสร้างในรูปตัวอย่าง
menu_options = [
    "🏠 หน้าแรก / สรุปภาพรวม",
    
    # บทที่ 1
    "01 นิยามและบทนำตรรกศาสตร์",
    "   • ตัวอย่างที่ 1",
    "   • โจทย์ท้าทายที่ 1",
    "   • เนื้อหาบทที่ 1",
    
    # บทที่ 2
    "02 ตัวเชื่อมและตารางค่าความจริง",
    "   • ตัวอย่างที่ 2",
    "   • โจทย์ท้าทายที่ 2",
    "   • เนื้อหาบทที่ 2",
    
    # บทที่ 3
    "03 สัจนิรันดร์และข้อขัดแย้ง",
    "   • ตัวอย่างที่ 3",
    "   • โจทย์ท้าทายที่ 3",
    "   • เนื้อหาบทที่ 3",
    
    # บทที่ 4
    "04 การอ้างเหตุผล",
    "   • ตัวอย่างที่ 4",
    "   • โจทย์ท้าทายที่ 4",
    "   • เนื้อหาบทที่ 4",
    
    # บทที่ 5
    "05 ประโยคเปิดและตัวบ่งปริมาณ",
    "   • ตัวอย่างที่ 5",
    "   • โจทย์ท้าทายที่ 5",
    "   • เนื้อหาบทที่ 5",
    
    # บทที่ 6
    "06 การอุปนัยและนิรนัย",
    "   • ตัวอย่างที่ 6",
    "   • โจทย์ท้าทายที่ 6",
    "   • เนื้อหาบทที่ 6",
    
    "📖 สรุปสูตรตรรกศาสตร์รวมทุกบท",
    "⚡ เครื่องมือคำนวณตรรกศาสตร์อัตโนมัติ"
]

selected_menu = st.sidebar.radio(
    "เลือกหัวข้อบทเรียน:",
    menu_options,
    label_visibility="collapsed"
)

# =========================================================
# 3. Main Title Display
# =========================================================
st.markdown("""
<div class="main-title-box">
    <div class="main-title-text">✨ สื่อการเรียนรู้วิชาตรรกศาสตร์เชิงคณิตศาสตร์ ✨</div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 4. Content Routing Logic
# =========================================================

# --- หน้าแรก ---
if "🏠 หน้าแรก" in selected_menu:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 💖 ยินดีต้อนรับสู่แอปพลิเคชันเรียนรู้ตรรกศาสตร์")
    st.write("เลือกหัวข้อบทเรียน ตัวอย่าง หรือโจทย์ท้าทายจากเมนูด้านซ้ายเพื่อเริ่มต้นศึกษาเนื้อหาได้ทันที")
    st.markdown("""
    * **บทที่ 1:** นิยามและบทนำตรรกศาสตร์
    * **บทที่ 2:** ตัวเชื่อมและตารางค่าความจริง
    * **บทที่ 3:** สัจนิรันดร์และข้อขัดแย้ง
    * **บทที่ 4:** การอ้างเหตุผล
    * **บทที่ 5:** ประโยคเปิดและตัวบ่งปริมาณ
    * **บทที่ 6:** การอุปนัยและนิรนัย
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# --- บทที่ 1 ---
elif "01 นิยาม" in selected_menu or "เนื้อหาบทที่ 1" in selected_menu:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 📘 01 นิยามและบทนำตรรกศาสตร์")
    st.write("ประพจน์ คือ ประโยคบอกเล่าหรือปฏิเสธที่มีค่าความจริงเป็นจริง (True) หรือเท็จ (False) อย่างใดอย่างหนึ่งเท่านั้น")
    st.markdown("#### กฎการอ้างเหตุผลเบื้องต้น:")
    st.latex(r"p, p \rightarrow q \vdash q \quad \text{(Modus Ponens)}")
    st.latex(r"p \rightarrow q, \neg q \vdash \neg p \quad \text{(Modus Tollens)}")
    st.markdown('</div>', unsafe_allow_html=True)

elif "ตัวอย่างที่ 1" in selected_menu:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 💡 ตัวอย่างที่ 1: การวิเคราะห์ประพจน์เงื่อนไข")
    st.markdown("**โจทย์:** จงพิจารณาว่าประโยค 'ถ้า $x^2 < 0$ แล้ว $x$ เป็นจำนวนจริง' มีค่าความจริงเป็นอย่างไร?")
    st.markdown('<div class="solution-box"><b>วิธีทำ:</b><br>1. ให้ $p$ แทน $x^2 < 0$ (เป็นเท็จ F)<br>2. ให้ $q$ แทน $x$ เป็นจำนวนจริง (เป็นจริง T)<br>3. เชื่อมด้วยเงื่อนไข $F \rightarrow T \equiv \text{True}$<br><b>ตอบ:</b> มีค่าความจริงเป็น <b>จริง (T)</b></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif "โจทย์ท้าทายที่ 1" in selected_menu:
    st.markdown('<div class="challenge-card">โจทย์ท้าทายที่ 1</div>', unsafe_allow_html=True)
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown(r"<b>โจทย์:</b> กำหนดให้ $p \rightarrow (q \rightarrow r)$ เป็นจริง และ $\neg r \wedge q$ เป็นจริง จงหาค่าความจริงของ $p$")
    ans1 = st.text_input("พิมพ์คำตอบของคุณ (เช่น จริง หรือ เท็จ):", key="q1")
    if st.button("ตรวจสอบคำตอบ"):
        if ans1.strip() in ["เท็จ", "False", "F", "f"]:
            st.success("🎉 ถูกต้อง! p มีค่าความจริงเป็น เท็จ (False)")
        else:
            st.error("❌ ยังไม่ถูกต้อง ลองพิจารณาค่าความจริงอีกครั้งนะครับ")
    st.markdown('</div>', unsafe_allow_html=True)

# --- บทที่ 2 ---
elif "02 ตัวเชื่อม" in selected_menu or "เนื้อหาบทที่ 2" in selected_menu:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 📗 02 ตัวเชื่อมและตารางค่าความจริง")
    st.write("ตารางแสดงค่าความจริงของตัวเชื่อมหลักทางตรรกศาสตร์")
    df_basic = pd.DataFrame({
        "p": ["T", "T", "F", "F"],
        "q": ["T", "F", "T", "F"],
        "p ∧ q": ["T", "F", "F", "F"],
        "p ∨ q": ["T", "T", "T", "F"],
        "p → q": ["T", "F", "T", "T"],
        "p ↔ q": ["T", "F", "F", "T"]
    })
    st.dataframe(df_basic, use_container_width=True, hide_index=True)
    st.markdown("#### กฎเดอมอร์แกน (De Morgan's Laws):")
    st.latex(r"\neg(p \wedge q) \equiv \neg p \vee \neg q")
    st.latex(r"\neg(p \vee q) \equiv \neg p \wedge \neg q")
    st.markdown('</div>', unsafe_allow_html=True)

elif "ตัวอย่างที่ 2" in selected_menu:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 💡 ตัวอย่างที่ 2: การลดรูปประพจน์")
    st.markdown(r"**โจทย์:** จงลดรูปประพจน์ $\neg(p \rightarrow \neg q)$")
    st.markdown('<div class="solution-box"><b>วิธีทำ:</b><br>1. ใช้สมมูล $A \rightarrow B \equiv \neg A \vee B$ ได้ $\neg(\neg p \vee \neg q)$<br>2. กระจายนิเสธด้วยกฎเดอมอร์แกนได้ $p \wedge q$<br><b>ตอบ:</b> $p \wedge q$</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif "โจทย์ท้าทายที่ 2" in selected_menu:
    st.markdown('<div class="challenge-card">โจทย์ท้าทายที่ 2</div>', unsafe_allow_html=True)
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("<b>โจทย์:</b> ตารางค่าความจริงที่มี $n$ ตัวแปร จะมีจำนวนแถวทั้งหมดกี่แถว?")
    ans2 = st.text_input("พิมพ์คำตอบของคุณ (เช่น 2^n):", key="q2")
    if st.button("ตรวจสอบคำตอบ"):
        if "2^n" in ans2.lower() or "2ⁿ" in ans2:
            st.success("🎉 ถูกต้อง! จำนวนแถวคือ 2^n แถว")
        else:
            st.error("❌ ลองพิมพ์อยู่ในรูป 2^n ดูนะครับ")
    st.markdown('</div>', unsafe_allow_html=True)

# --- บทอื่นๆ ---
elif "03 สัจนิรันดร์" in selected_menu or "เนื้อหาบทที่ 3" in selected_menu:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 📙 03 สัจนิรันดร์และข้อขัดแย้ง")
    st.write("• **สัจนิรันดร์ (Tautology):** ประพจน์ที่เป็นจริงทุกกรณี")
    st.write("• **ข้อขัดแย้ง (Contradiction):** ประพจน์ที่เป็นเท็จทุกกรณี")
    st.latex(r"p \vee \neg p \equiv \text{True}")
    st.markdown('</div>', unsafe_allow_html=True)

elif "ตัวอย่างที่ 3" in selected_menu:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 💡 ตัวอย่างที่ 3: การตรวจสอบสัจนิรันดร์")
    st.markdown(r"**โจทย์:** จงตรวจสอบว่า $[(p \rightarrow q) \wedge p] \rightarrow q$ เป็นสัจนิรันดร์หรือไม่")
    st.markdown('<div class="solution-box"><b>วิธีทำ:</b> สมมติให้ประพจน์หลักเป็นเท็จ จะเกิดข้อขัดแย้ง<br><b>ตอบ:</b> เป็นสัจนิรันดร์</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif "โจทย์ท้าทายที่ 3" in selected_menu:
    st.markdown('<div class="challenge-card">โจทย์ท้าทายที่ 3</div>', unsafe_allow_html=True)
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("<b>โจทย์:</b> ประพจน์ $p \wedge \neg p$ เป็นสัจนิรันดร์ หรือ ข้อขัดแย้ง?")
    ans3 = st.text_input("พิมพ์คำตอบของคุณ:", key="q3")
    if st.button("ตรวจสอบคำตอบ"):
        if "ขัดแย้ง" in ans3 or "contradiction" in ans3.lower():
            st.success("🎉 ถูกต้อง! เป็นข้อขัดแย้ง (Contradiction)")
        else:
            st.error("❌ ยังไม่ถูกต้อง ลองพิจารณาอีกครั้งนะครับ")
    st.markdown('</div>', unsafe_allow_html=True)

# --- สรุปสูตร ---
elif "สรุปสูตรตรรกศาสตร์รวมทุกบท" in selected_menu:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 📖 สรุปสูตรตรรกศาสตร์สำคัญทุกบท")
    st.latex(r"1. \quad p \rightarrow q \equiv \neg p \vee q")
    st.latex(r"2. \quad \neg(p \rightarrow q) \equiv p \wedge \neg q")
    st.latex(r"3. \quad p \leftrightarrow q \equiv (p \rightarrow q) \wedge (q \rightarrow p)")
    st.latex(r"4. \quad \neg \forall x P(x) \equiv \exists x \neg P(x)")
    st.latex(r"5. \quad 1^3 + 2^3 + \dots + n^3 = \left[\frac{n(n+1)}{2}\right]^2")
    st.markdown('</div>', unsafe_allow_html=True)

# --- เครื่องมือคำนวณ ---
elif "เครื่องมือคำนวณ" in selected_menu:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### ⚡ เครื่องมือคำนวณและตรวจสอบสัจนิรันดร์")
    user_expr = st.text_input("ป้อนประพจน์ (เช่น (p >> q) | (q >> p)):", value="(p >> q) | (q >> p)")
    if st.button("🚀 ตรวจสอบ"):
        try:
            expr = sp.sympify(user_expr)
            syms = sorted([str(s) for s in expr.free_symbols])
            combos = list(itertools.product([True, False], repeat=len(syms)))
            is_taut = True
            for cb in combos:
                mapping = dict(zip([sp.Symbol(s) for s in syms], cb))
                if not bool(expr.subs(mapping)):
                    is_taut = False
                    break
            if is_taut:
                st.success("🎉 ผลลัพธ์: ประพจน์นี้เป็นสัจนิรันดร์ (Tautology)")
            else:
                st.warning("⚠️ ผลลัพธ์: ประพจน์นี้ไม่เป็นสัจนิรันดร์")
        except Exception as e:
            st.error(f"รูปแบบประพจน์ไม่ถูกต้อง: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 📌 กรุณาเลือกหัวข้อบทเรียนจากแถบเมนูด้านซ้าย")
    st.markdown('</div>', unsafe_allow_html=True)
