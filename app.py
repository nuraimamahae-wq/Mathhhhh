import streamlit as st
import sympy as sp
import itertools

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="ตรรกศาสตร์เชิงคณิตศาสตร์ | Minimal Learning App",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Minimalist Clean White Theme & Custom CSS
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Minimal Background & Font setup */
    .stApp {
        background-color: #F8FAFC;
        color: #1E293B;
        font-family: 'Sarabun', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Header Container - Minimal Slate */
    .main-title-box {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    .main-title-text {
        font-size: 26px;
        font-weight: 700;
        color: #0F172A;
        margin: 0;
    }
    
    .main-subtitle-text {
        font-size: 14px;
        color: #64748B;
        margin-top: 6px;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 18px;
        font-weight: 700;
        color: #2563EB;
        border-left: 4px solid #2563EB;
        padding-left: 10px;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    /* Content Card */
    .content-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
    }
    
    /* Challenge Card */
    .challenge-card {
        background-color: #EFF6FF;
        border: 1px solid #BFDBFE;
        border-radius: 12px;
        padding: 20px;
        color: #1E40AF;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 15px;
    }
    
    /* Solution Card */
    .solution-card {
        background-color: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-radius: 8px;
        padding: 16px;
        color: #166534;
        margin-top: 12px;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "01_theory"

# ---------------------------------------------------------
# Sidebar Navigation (Minimal Accordion Menu)
# ---------------------------------------------------------
st.sidebar.markdown("### 📚 เมนูบทเรียน")

# บทที่ 1
with st.sidebar.expander("01 บทนำและประพจน์", expanded=True):
    if st.button("• เนื้อหาบทที่ 1", key="m1_1", use_container_width=True):
        st.session_state.selected_menu = "01_theory"
    if st.button("• ตัวอย่างที่ 1", key="m1_2", use_container_width=True):
        st.session_state.selected_menu = "01_ex1"
    if st.button("• โจทย์ท้าทายที่ 1", key="m1_3", use_container_width=True):
        st.session_state.selected_menu = "01_challenge1"

# บทที่ 2
with st.sidebar.expander("02 ตัวเชื่อมและตารางค่าความจริง"):
    if st.button("• เนื้อหาบทที่ 2", key="m2_1", use_container_width=True):
        st.session_state.selected_menu = "02_theory"
    if st.button("• ตัวอย่างที่ 2", key="m2_2", use_container_width=True):
        st.session_state.selected_menu = "02_ex2"
    if st.button("• โจทย์ท้าทายที่ 2", key="m2_3", use_container_width=True):
        st.session_state.selected_menu = "02_challenge2"

# บทที่ 3
with st.sidebar.expander("03 สัจนิรันดร์และข้อขัดแย้ง"):
    if st.button("• เนื้อหาบทที่ 3", key="m3_1", use_container_width=True):
        st.session_state.selected_menu = "03_theory"
    if st.button("• ตัวอย่างที่ 3", key="m3_2", use_container_width=True):
        st.session_state.selected_menu = "03_ex3"
    if st.button("• โจทย์ท้าทายที่ 3", key="m3_3", use_container_width=True):
        st.session_state.selected_menu = "03_challenge3"

# บทที่ 4
with st.sidebar.expander("04 การอ้างเหตุผล"):
    if st.button("• เนื้อหาบทที่ 4", key="m4_1", use_container_width=True):
        st.session_state.selected_menu = "04_theory"
    if st.button("• ตัวอย่างที่ 4", key="m4_2", use_container_width=True):
        st.session_state.selected_menu = "04_ex4"
    if st.button("• โจทย์ท้าทายที่ 4", key="m4_3", use_container_width=True):
        st.session_state.selected_menu = "04_challenge4"

# บทที่ 5
with st.sidebar.expander("05 ประโยคเปิดและตัวบ่งปริมาณ"):
    if st.button("• เนื้อหาบทที่ 5", key="m5_1", use_container_width=True):
        st.session_state.selected_menu = "05_theory"
    if st.button("• ตัวอย่างที่ 5", key="m5_2", use_container_width=True):
        st.session_state.selected_menu = "05_ex5"
    if st.button("• โจทย์ท้าทายที่ 5", key="m5_3", use_container_width=True):
        st.session_state.selected_menu = "05_challenge5"

# บทที่ 6
with st.sidebar.expander("06 การอุปนัยและนิรนัย"):
    if st.button("• เนื้อหาบทที่ 6", key="m6_1", use_container_width=True):
        st.session_state.selected_menu = "06_theory"
    if st.button("• ตัวอย่างที่ 6", key="m6_2", use_container_width=True):
        st.session_state.selected_menu = "06_ex6"
    if st.button("• โจทย์ท้าทายที่ 6", key="m6_3", use_container_width=True):
        st.session_state.selected_menu = "06_challenge6"

st.sidebar.markdown("---")
if st.sidebar.button("📐 เมนูสรุปสูตรทั้งหมด", use_container_width=True):
    st.session_state.selected_menu = "all_formulas"
if st.sidebar.button("⚡ เครื่องมือคำนวณอัจฉริยะ", use_container_width=True):
    st.session_state.selected_menu = "calculator"

# ---------------------------------------------------------
# Main Display Content
# ---------------------------------------------------------

# Title Banner
st.markdown("""
<div class="main-title-box">
    <div class="main-title-text">📐 สื่อการเรียนรู้วิชาตรรกศาสตร์เชิงคณิตศาสตร์</div>
    <div class="main-subtitle-text">เรียนรู้ตรรกศาสตร์ สูตรคณิตศาสตร์ ตัวอย่าง และโจทย์ท้าทายอย่างเป็นระบบ</div>
</div>
""", unsafe_allow_html=True)

menu = st.session_state.selected_menu

# --- 01_theory ---
if menu == "01_theory":
    st.markdown('<div class="section-header">📘 บทที่ 1: ประพจน์และการให้เหตุผล - เนื้อหาหลัก</div>', unsafe_allow_html=True)
    st.markdown(r"""
    <div class="content-card">
        <h3>📖 นิยามประพจน์ (Proposition)</h3>
        <p>ประพจน์ คือ ประโยคบอกเล่าหรือประโยคปฏิเสธที่มีค่าความจริงเป็น <b>จริง ($\text{True}$)</b> หรือ <b>เท็จ ($\text{False}$)</b> อย่างใดอย่างหนึ่งเท่านั้น</p>
        <hr style="border: 0; border-top: 1px solid #E2E8F0;">
        <h4>📐 กฎการอ้างเหตุผลเบื้องต้น</h4>
        <ul>
            <li><b>Modus Ponens:</b> $$p, p \rightarrow q \vdash q$$</li>
            <li><b>Modus Tollens:</b> $$p \rightarrow q, \neg q \vdash \neg p$$</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --- 01_ex1 ---
elif menu == "01_ex1":
    st.markdown('<div class="section-header">💡 บทที่ 1: ตัวอย่างพร้อมวิธีทำอย่างละเอียด</div>', unsafe_allow_html=True)
    with st.expander("ตัวอย่างที่ 1: การวิเคราะห์ค่าความจริงของประพจน์เงื่อนไข", expanded=True):
        st.markdown(r"<b>โจทย์:</b> จงพิจารณาว่าประโยค 'ถ้า $x^2 < 0$ แล้ว $x$ เป็นจำนวนจริง' มีค่าความจริงเป็นอย่างไร?")
        st.markdown(r"""
        <div class="solution-card">
            <b>วิธีทำ:</b><br>
            1. ให้ $p$ แทน $x^2 < 0$ และ $q$ แทน $x$ เป็นจำนวนจริง<br>
            2. ประพจน์เหตุ $p$ ($x^2 < 0$) มีค่าความจริงเป็นเท็จ ($\text{False}$) ในระบบจำนวนจริง<br>
            3. ประพจน์ผล $q$ ($x$ เป็นจำนวนจริง) มีค่าความจริงเป็นจริง ($\text{True}$)<br>
            4. ตามนิยามประพจน์เงื่อนไข $F \rightarrow T \equiv \text{True}$<br>
            <b>คำตอบ:</b> ประโยคนี้มีค่าความจริงเป็น <b>จริง ($\text{True}$)</b>
        </div>
        """, unsafe_allow_html=True)

# --- 01_challenge1 ---
elif menu == "01_challenge1":
    st.markdown('<div class="challenge-card">โจทย์ท้าทายที่ 1</div>', unsafe_allow_html=True)
    st.markdown(r"""
    <div class="content-card">
        <b>โจทย์:</b> กำหนดให้ $p \rightarrow (q \rightarrow r)$ เป็นจริง และ $\neg r \wedge q$ เป็นจริง จงหาค่าความจริงของประพจน์ $p$
    </div>
    """, unsafe_allow_html=True)
    
    ans = st.text_input("พิมพ์คำตอบของคุณ (เช่น จริง หรือ เท็จ):", key="ans_c1")
    if st.button("ตรวจคำตอบ"):
        if ans.strip() in ["เท็จ", "False", "F", "f"]:
            st.success("🎉 ถูกต้อง! ค่าความจริงของ p คือ เท็จ (False)")
        else:
            st.error("❌ ยังไม่ถูกต้อง ลองพิจารณาค่าความจริงใหม่อีกครั้งนะครับ")
            
    with st.expander("👉 ดูเฉลยวิธีทำอย่างละเอียด"):
        st.markdown(r"""
        <div class="solution-card">
            <b>วิธีทำ:</b><br>
            1. จาก $\neg r \wedge q \equiv T$ จะได้ $\neg r \equiv T \implies r \equiv F$ และ $q \equiv T$<br>
            2. แทนค่าในวงเล็บหลัง $q \rightarrow r \implies T \rightarrow F \equiv F$<br>
            3. จากโจทย์ $p \rightarrow (q \rightarrow r) \equiv T$ จะได้ $p \rightarrow F \equiv T$<br>
            4. การที่ประพจน์เงื่อนไข $p \rightarrow F$ เป็นจริงได้ บังคับให้ $p$ ต้องเป็น <b>เท็จ ($\text{False}$)</b> เท่านั้น
        </div>
        """, unsafe_allow_html=True)

# --- 02_theory ---
elif menu == "02_theory":
    st.markdown('<div class="section-header">📗 บทที่ 2: ตัวเชื่อมและตารางค่าความจริง - เนื้อหา</div>', unsafe_allow_html=True)
    st.markdown(r"""
    <div class="content-card">
        <h3>📖 ตัวเชื่อมทางตรรกศาสตร์ (Logical Connectives)</h3>
        <ul>
            <li><b>นิเสธ ($\neg$):</b> $\neg T \equiv F$, $\neg F \equiv T$</li>
            <li><b>และ ($\wedge$):</b> $T \wedge T \equiv T$ (กรณีอื่นเป็นเท็จทั้งหมด)</li>
            <li><b>หรือ ($\vee$):</b> $F \vee F \equiv F$ (กรณีอื่นเป็นจริงทั้งหมด)</li>
            <li><b>ถ้า...แล้ว ($\rightarrow$):</b> $T \rightarrow F \equiv F$ (กรณีอื่นเป็นจริงทั้งหมด)</li>
            <li><b>ก็ต่อเมื่อ ($\leftrightarrow$):</b> ค่าความจริงเหมือนกันเป็นจริง ต่างกันเป็นเท็จ</li>
        </ul>
        <hr style="border: 0; border-top: 1px solid #E2E8F0;">
        <h4>📐 กฎเดอมอร์แกน (De Morgan's Laws)</h4>
        $$\neg(p \wedge q) \equiv \neg p \vee \neg q$$
        $$\neg(p \vee q) \equiv \neg p \wedge \neg q$$
    </div>
    """, unsafe_allow_html=True)

# --- 02_ex2 ---
elif menu == "02_ex2":
    st.markdown('<div class="section-header">💡 บทที่ 2: ตัวอย่างการจัดรูปประพจน์</div>', unsafe_allow_html=True)
    with st.expander("ตัวอย่างที่ 2: การแปลงประพจน์ด้วยกฎสมมูล", expanded=True):
        st.markdown(r"<b>โจทย์:</b> จงลดรูปประพจน์ $\neg(p \rightarrow \neg q)$ ให้เหลือเฉพาะตัวเชื่อมพื้นฐาน")
        st.markdown(r"""
        <div class="solution-card">
            <b>วิธีทำ:</b><br>
            1. ใช้สมมูล $A \rightarrow B \equiv \neg A \vee B$ แปลงในวงเล็บได้ $\neg p \vee \neg q$<br>
            2. ใส่เครื่องหมายนิเสธภายนอก: $\neg(\neg p \vee \neg q)$<br>
            3. กระจายนิเสธด้วยกฎเดอมอร์แกน: $(\neg\neg p \wedge \neg\neg q)$<br>
            4. ใช้กฎนิเสธซ้อนจะได้คำตอบ: $p \wedge q$<br>
            <b>คำตอบ:</b> $p \wedge q$
        </div>
        """, unsafe_allow_html=True)

# --- 02_challenge2 ---
elif menu == "02_challenge2":
    st.markdown('<div class="challenge-card">โจทย์ท้าทายที่ 2</div>', unsafe_allow_html=True)
    st.markdown(r"""
    <div class="content-card">
        <b>โจทย์:</b> ตารางค่าความจริงของประพจน์ที่มี $n$ ตัวแปรที่แตกต่างกัน จะมีจำนวนแถวทั้งหมดกี่แถว? (ตอบเป็นรูปสูตร เช่น 2^n)
    </div>
    """, unsafe_allow_html=True)
    ans2 = st.text_input("พิมพ์คำตอบของคุณ:", key="ans_c2")
    if st.button("ตรวจคำตอบ"):
        if "2^n" in ans2.lower() or "2ⁿ" in ans2:
            st.success(r"🎉 ถูกต้อง! จำนวนแถวในตารางค่าความจริงคือ $2^n$ แถว")
        else:
            st.error("❌ คำตอบยังไม่ถูกต้อง ลองพิมพ์อยู่ในรูป 2^n ดูนะครับ")

# --- 03_theory ---
elif menu == "03_theory":
    st.markdown('<div class="section-header">📙 บทที่ 3: สัจนิรันดร์และข้อขัดแย้ง - เนื้อหา</div>', unsafe_allow_html=True)
    st.markdown(r"""
    <div class="content-card">
        <h3>📖 นิยามและสมบัติ</h3>
        <ul>
            <li><b>สัจนิรันดร์ (Tautology):</b> ประพจน์ที่มีค่าความจริงเป็น <b>จริง ($\text{True}$) ทุกกรณี</b></li>
            <li><b>ข้อขัดแย้ง (Contradiction):</b> ประพจน์ที่มีค่าความจริงเป็น <b>เท็จ ($\text{False}$) ทุกกรณี</b></li>
        </ul>
        <hr style="border: 0; border-top: 1px solid #E2E8F0;">
        <h4>📐 กฎการเป็นจริงกึ่งกลาง</h4>
        $$p \vee \neg p \equiv T \quad \text{(เป็นสัจนิรันดร์)}$$
        $$p \wedge \neg p \equiv F \quad \text{(เป็นข้อขัดแย้ง)}$$
    </div>
    """, unsafe_allow_html=True)

# --- 03_ex3 ---
elif menu == "03_ex3":
    st.markdown('<div class="section-header">💡 บทที่ 3: ตัวอย่างการหาข้อขัดแย้ง</div>', unsafe_allow_html=True)
    with st.expander("ตัวอย่างที่ 3: ตรวจสอบสัจนิรันดร์โดยวิธีสมมติให้เป็นเท็จ", expanded=True):
        st.markdown(r"<b>โจทย์:</b> จงตรวจสอบว่า $[(p \rightarrow q) \wedge p] \rightarrow q$ เป็นสัจนิรันดร์หรือไม่")
        st.markdown(r"""
        <div class="solution-card">
            <b>วิธีทำ:</b><br>
            1. สมมติให้ประพจน์หลักเป็นเท็จ ($\equiv F$)<br>
            2. จะได้เหตุทางซ้ายเป็นจริง และผลทางขวา $q \equiv F$<br>
            3. จากเหตุทางซ้ายเป็นจริง บังคับให้ $p \equiv T$ และ $(p \rightarrow q) \equiv T$<br>
            4. แทน $p \equiv T, q \equiv F$ ใน $p \rightarrow q$ ได้ $T \rightarrow F \equiv F$ ซึ่งขัดแย้งกับข้อ 3<br>
            <b>คำตอบ:</b> เกิดข้อขัดแย้ง แสดงว่าประพจน์นี้ <b>เป็นสัจนิรันดร์ (Tautology)</b>
        </div>
        """, unsafe_allow_html=True)

# --- 03_challenge3 ---
elif menu == "03_challenge3":
    st.markdown('<div class="challenge-card">โจทย์ท้าทายที่ 3</div>', unsafe_allow_html=True)
    st.markdown(r"""
    <div class="content-card">
        <b>โจทย์:</b> ประพจน์ $p \wedge \neg p$ มีลักษณะทางตรรกศาสตร์เป็น สัจนิรันดร์ หรือ ข้อขัดแย้ง?
    </div>
    """, unsafe_allow_html=True)
    ans3 = st.text_input("พิมพ์คำตอบของคุณ:", key="ans_c3")
    if st.button("ตรวจคำตอบ"):
        if "ขัดแย้ง" in ans3 or "contradiction" in ans3.lower():
            st.success("🎉 ถูกต้อง! $p \wedge \neg p$ เป็นเท็จทุกกรณี จึงเป็นข้อขัดแย้ง (Contradiction)")
        else:
            st.error("❌ ยังไม่ถูกต้อง ลองทบทวนดูอีกครั้งนะครับ")

# --- all_formulas ---
elif menu == "all_formulas":
    st.markdown('<div class="section-header">📐 สรุปสูตรและกฎสำคัญทางตรรกศาสตร์รวมทุกบท</div>', unsafe_allow_html=True)
    st.markdown(r"""
    <div class="content-card">
        <h4>1. กฎการสมมูลของประพจน์ (Equivalence Rules)</h4>
        <ul>
            <li>$p \rightarrow q \equiv \neg p \vee q$</li>
            <li>$\neg(p \rightarrow q) \equiv p \wedge \neg q$</li>
            <li>$p \leftrightarrow q \equiv (p \rightarrow q) \wedge (q \rightarrow p)$</li>
            <li>$\neg(p \wedge q) \equiv \neg p \vee \neg q \quad \text{(De Morgan)}$</li>
            <li>$\neg(p \vee q) \equiv \neg p \wedge \neg q \quad \text{(De Morgan)}$</li>
        </ul>
        <hr style="border: 0; border-top: 1px solid #E2E8F0;">
        <h4>2. นิเสธของตัวบ่งปริมาณ (Quantifier Negation Rules)</h4>
        <ul>
            <li>$\neg \forall x P(x) \equiv \exists x \neg P(x)$</li>
            <li>$\neg \exists x P(x) \equiv \forall x \neg P(x)$</li>
            <li>$\neg \forall x \exists y P(x, y) \equiv \exists x \forall y \neg P(x, y)$</li>
        </ul>
        <hr style="border: 0; border-top: 1px solid #E2E8F0;">
        <h4>3. อนุกรมและหลักการอุปนัยเชิงคณิตศาสตร์</h4>
        <ul>
            <li>ผลบวก $n$ พจน์แรก: $$1 + 2 + 3 + \dots + n = \frac{n(n+1)}{2}$$</li>
            <li>ผลบวกกำลังสาม $n$ พจน์แรก: $$1^3 + 2^3 + 3^3 + \dots + n^3 = \left[\frac{n(n+1)}{2}\right]^2$$</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --- calculator ---
elif menu == "calculator":
    st.markdown('<div class="section-header">⚡ เครื่องมือคำนวณและตรวจสอบสัจนิรันดร์อัตโนมัติ</div>', unsafe_allow_html=True)
    st.markdown("ป้อนประพจน์ที่ต้องการตรวจสอบ (ใช้ `>>` แทนถ้า...แล้ว, `|` แทนหรือ, `&` แทนและ, `~` แกลนนิเสธ):")
    expr_in = st.text_input("ตัวอย่างประพจน์:", value="(p >> q) | (q >> p)")
    if st.button("🚀 ตรวจสอบความเป็นสัจนิรันดร์"):
        try:
            expr = sp.sympify(expr_in)
            syms = sorted([str(s) for s in expr.free_symbols])
            combos = list(itertools.product([True, False], repeat=len(syms)))
            is_taut = True
            for cb in combos:
                mapping = dict(zip([sp.Symbol(s) for s in syms], cb))
                if not bool(expr.subs(mapping)):
                    is_taut = False
                    break
            if is_taut:
                st.success("🎉 ประพจน์นี้เป็นสัจนิรันดร์ (Tautology)")
            else:
                st.warning("⚠️ ประพจน์นี้ไม่เป็นสัจนิรันดร์")
        except Exception as e:
            st.error(f"รูปแบบประพจน์ไม่ถูกต้อง: {e}")

else:
    st.markdown('<div class="section-header">📌 เลือกบทเรียนจากแถบเมนูด้านซ้ายเพื่อศึกษาเนื้อหา</div>', unsafe_allow_html=True)
