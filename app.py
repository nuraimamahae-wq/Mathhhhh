import streamlit as st
import sympy as sp
import itertools

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="ตรรกศาสตร์เชิงคณิตศาสตร์ | Interactive App",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom Modern Dark UI Styling (คล้ายเว็บแอปในภาพ)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Dark Theme Background */
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    
    /* Header Container */
    .main-title-box {
        background: linear-gradient(135deg, #1E1B4B 0%, #312E81 100%);
        border: 1px solid #4338CA;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }
    
    .main-title-text {
        font-size: 28px;
        font-weight: 800;
        color: #EEF2FF;
        margin: 0;
    }
    
    /* Section Sub-headers */
    .section-header {
        font-size: 20px;
        font-weight: 700;
        color: #818CF8;
        border-left: 4px solid #6366F1;
        padding-left: 12px;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    /* Content Cards */
    .content-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
    }
    
    /* Blue Challenge Question Card */
    .challenge-card {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        border-radius: 16px;
        padding: 24px;
        color: #FFFFFF;
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 20px;
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.3);
    }
    
    /* Solution Box */
    .solution-card {
        background-color: #064E3B;
        border: 1px solid #059669;
        border-radius: 12px;
        padding: 16px;
        color: #ECFDF5;
        margin-top: 12px;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #020617;
        border-right: 1px solid #1E293B;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "01_theory"

# ---------------------------------------------------------
# Sidebar Navigation (โครงสร้างเมนูย่อยซ้อนในแต่ละบท)
# ---------------------------------------------------------
st.sidebar.markdown("## 📚 บทเรียนและหัวข้อ")

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
if st.sidebar.button("📐 สรุปสูตรทั้งหมด", use_container_width=True):
    st.session_state.selected_menu = "all_formulas"
if st.sidebar.button("📝 แบบทดสอบรวม 10 ข้อ", use_container_width=True):
    st.session_state.selected_menu = "quiz_10"
if st.sidebar.button("⚡ เครื่องมือคำนวณอัตโนมัติ", use_container_width=True):
    st.session_state.selected_menu = "calculator"

# ---------------------------------------------------------
# Display Content Area (ส่วนแสดงผลหลัก)
# ---------------------------------------------------------

# Header
st.markdown("""
<div class="main-title-box">
    <div class="main-title-text">✨ สื่อการเรียนรู้วิชาตรรกศาสตร์เชิงคณิตศาสตร์ ✨</div>
</div>
""", unsafe_allow_html=True)

menu = st.session_state.selected_menu

# --- 01_theory ---
if menu == "01_theory":
    st.markdown('<div class="section-header">📘 บทที่ 1: ประพจน์และการให้เหตุผล - เนื้อหาและแนวคิดหลัก</div>', unsafe_allow_html=True)
    st.markdown(r"""
    <div class="content-card">
        <h3>📖 บทนิยามประพจน์</h3>
        <p><b>ประพจน์ (Proposition)</b> คือ ประโยคบอกเล่าหรือประโยคปฏิเสธที่มีค่าความจริงเป็น <b>จริง ($\text{True}$)</b> หรือ <b>เท็จ ($\text{False}$)</b> อย่างใดอย่างหนึ่งเท่านั้น</p>
        <hr style="border-color: #334155;">
        <h4>📐 กฎการให้เหตุผลเบื้องต้น</h4>
        <ul>
            <li><b>Modus Ponens:</b> $$p, p \rightarrow q \vdash q$$</li>
            <li><b>Modus Tollens:</b> $$p \rightarrow q, \neg q \vdash \neg p$$</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --- 01_ex1 ---
elif menu == "01_ex1":
    st.markdown('<div class="section-header">💡 บทที่ 1: ตัวอย่างพร้อมวิธีทำอย่างละเอียด</div>', unsafe_allow_html=True)
    with st.expander("ตัวอย่างที่ 1: การพิจารณาค่าความจริงของประพจน์เงื่อนไข", expanded=True):
        st.markdown(r"<b>โจทย์:</b> จงพิจารณาว่าประโยค 'ถ้า $x^2 < 0$ แล้ว $x$ เป็นจำนวนจริง' มีค่าความจริงเป็นอย่างไร?")
        st.markdown(r"""
        <div class="solution-card">
            <b>วิธีทำ:</b><br>
            1. ให้ $p$ แทน $x^2 < 0$ และ $q$ แทน $x$ เป็นจำนวนจริง<br>
            2. ประพจน์เหตุ $p$ เป็นเท็จ ($\text{False}$) เสมอในระบบจำนวนจริง<br>
            3. ประพจน์ผล $q$ เป็นจริง ($\text{True}$)<br>
            4. เชื่อมด้วยเงื่อนไข $F \rightarrow T \equiv \text{True}$<br>
            <b>ตอบ:</b> เป็นจริง ($\text{True}$)
        </div>
        """, unsafe_allow_html=True)

# --- 01_challenge1 ---
elif menu == "01_challenge1":
    st.markdown('<div class="challenge-card">โจทย์ท้าทายที่ 1</div>', unsafe_allow_html=True)
    
    st.markdown(r"""
    <div class="content-card">
        <b>โจทย์:</b> กำหนดให้ $p \rightarrow (q \rightarrow r)$ เป็นจริง และ $\neg r \wedge q$ เป็นจริง จงหาค่าความจริงของ $p$
    </div>
    """, unsafe_allow_html=True)
    
    ans = st.text_input("พิมพ์คำตอบของคุณ (เช่น จริง หรือ เท็จ):", key="ans_c1")
    if st.button("ตรวจคำตอบ"):
        if ans.strip() in ["เท็จ", "False", "F", "f"]:
            st.success("🎉 ถูกต้อง! ค่าความจริงของ p คือ เท็จ (False)")
        else:
            st.error("❌ ยังไม่ถูกต้อง ลองคำนวณอีกครั้งนะครับ")
            
    with st.expander("ดูเฉลยละเอียด"):
        st.markdown(r"""
        <div class="solution-card">
            <b>เฉลยวิธีทำ:</b><br>
            1. จาก $\neg r \wedge q \equiv T$ แสดงว่า $\neg r \equiv T \implies r \equiv F$ และ $q \equiv T$<br>
            2. แทนค่าใน $q \rightarrow r$ จะได้ $T \rightarrow F \equiv F$<br>
            3. จากโจทย์ $p \rightarrow (q \rightarrow r) \equiv T$ จะได้ $p \rightarrow F \equiv T$<br>
            4. บังคับให้ $p$ ต้องเป็น <b>เท็จ (False)</b> ถ้านำจริงไปแทนจะได้จริงไปเท็จเป็นเท็จ
        </div>
        """, unsafe_allow_html=True)

# --- 02_theory ---
elif menu == "02_theory":
    st.markdown('<div class="section-header">📗 บทที่ 2: ตัวเชื่อมและตารางค่าความจริง - เนื้อหา</div>', unsafe_allow_html=True)
    st.markdown(r"""
    <div class="content-card">
        <h3>📖 ตัวเชื่อมทางตรรกศาสตร์ (Logical Connectives)</h3>
        <ul>
            <li><b>นิเสธ ($\neg$):</b> กลับค่าความจริง</li>
            <li><b>และ ($\wedge$):</b> เป็นจริงเมื่อจริงทั้งคู่</li>
            <li><b>หรือ ($\vee$):</b> เป็นเท็จเมื่อเท็จทั้งคู่</li>
            <li><b>ถ้า...แล้ว ($\rightarrow$):</b> เป็นเท็จเมื่อ หน้าจริง-หลังเท็จ</li>
            <li><b>ก็ต่อเมื่อ ($\leftrightarrow$):</b> เป็นจริงเมื่อค่าความจริงเหมือนกัน</li>
        </ul>
        <hr style="border-color: #334155;">
        <h4>📐 กฎเดอมอร์แกน (De Morgan's Laws)</h4>
        $$\neg(p \wedge q) \equiv \neg p \vee \neg q$$
        $$\neg(p \vee q) \equiv \neg p \wedge \neg q$$
    </div>
    """, unsafe_allow_html=True)

# --- 02_ex2 ---
elif menu == "02_ex2":
    st.markdown('<div class="section-header">💡 บทที่ 2: ตัวอย่างการจัดรูปประพจน์</div>', unsafe_allow_html=True)
    with st.expander("ตัวอย่างที่ 2: การแปลงประพจน์ด้วยกฎสมมูล", expanded=True):
        st.markdown(r"<b>โจทย์:</b> จงแปลง $\neg(p \rightarrow \neg q)$ ให้เหลือเฉพาะตัวเชื่อมพื้นฐาน")
        st.markdown(r"""
        <div class="solution-card">
            <b>วิธีทำ:</b><br>
            1. จากสมมูล $A \rightarrow B \equiv \neg A \vee B$ จัดรูปในวงเล็บได้ $\neg p \vee \neg q$<br>
            2. ใส่เครื่องหมายนิเสธหน้าวงเล็บ $\neg(\neg p \vee \neg q)$<br>
            3. กระจายนิเสธด้วยกฎเดอมอร์แกนจะได้ $(\neg\neg p \wedge \neg\neg q)$<br>
            4. ใช้กฎนิเสธซ้อนตัดเครื่องหมายออกจะได้ $p \wedge q$<br>
            <b>ตอบ:</b> $p \wedge q$
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
            st.success("🎉 ถูกต้อง! จำนวนแถวทั้งหมดคือ 2^n แถว")
        else:
            st.error("❌ คำตอบยังไม่ถูกต้อง ลองตอบในรูป 2^n ดูนะครับ")

# --- 03_theory ---
elif menu == "03_theory":
    st.markdown('<div class="section-header">📙 บทที่ 3: สัจนิรันดร์และข้อขัดแย้ง - เนื้อหา</div>', unsafe_allow_html=True)
    st.markdown(r"""
    <div class="content-card">
        <h3>📖 นิยามความหมาย</h3>
        <ul>
            <li><b>สัจนิรันดร์ (Tautology):</b> ประพจน์ที่มีค่าความจริงเป็น <b>จริงทุกกรณี</b></li>
            <li><b>ข้อขัดแย้ง (Contradiction):</b> ประพจน์ที่มีค่าความจริงเป็น <b>เท็จทุกกรณี</b></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --- 03_ex3 ---
elif menu == "03_ex3":
    st.markdown('<div class="section-header">💡 บทที่ 3: ตัวอย่างการหาข้อขัดแย้ง</div>', unsafe_allow_html=True)
    with st.expander("ตัวอย่างที่ 3: ตรวจสอบสัจนิรันดร์โดยการหาข้อขัดแย้ง", expanded=True):
        st.markdown(r"<b>โจทย์:</b> จงตรวจสอบว่า $[(p \rightarrow q) \wedge p] \rightarrow q$ เป็นสัจนิรันดร์หรือไม่")
        st.markdown(r"""
        <div class="solution-card">
            <b>วิธีทำ:</b><br>
            1. สมมติให้ประพจน์รวมเป็นเท็จ ($\equiv F$)<br>
            2. จะได้ฝั่งซ้ายเป็นจริง และ $q$ เป็นเท็จ ($q \equiv F$)<br>
            3. จากฝั่งซ้ายเป็นจริง จะได้ $p \equiv T$ และ $p \rightarrow q \equiv T$<br>
            4. แทน $p \equiv T, q \equiv F$ ใน $p \rightarrow q$ จะได้ $T \rightarrow F \equiv F$ ซึ่งขัดแย้งกับข้อ 3<br>
            <b>ตอบ:</b> เกิดข้อขัดแย้ง แสดงว่าประพจน์นี้ <b>เป็นสัจนิรันดร์ (Tautology)</b>
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
            st.success("🎉 ถูกต้อง! $p \wedge \neg p$ เป็นเท็จทุกกรณี จึงเป็นข้อขัดแย้ง")
        else:
            st.error("❌ ยังไม่ถูกต้อง ลองทบทวนดูอีกครั้งนะครับ")

# --- 04_theory & others ---
elif menu == "04_theory":
    st.markdown('<div class="section-header">📕 บทที่ 4: การอ้างเหตุผล - เนื้อหา</div>', unsafe_allow_html=True)
    st.markdown(r"""
    <div class="content-card">
        <h3>📖 ความสมเหตุสมผล (Validity)</h3>
        <p>การอ้างเหตุผลจะ<b>สมเหตุสมผล</b> ก็ต่อเมื่อ เหตุทุกข้อเป็นจริง แล้วบังคับให้ผลสรุปต้องเป็นจริงเสมอ</p>
    </div>
    """, unsafe_allow_html=True)

elif menu == "all_formulas":
    st.markdown('<div class="section-header">📐 สรุปสูตรตรรกศาสตร์รวมทุกบท</div>', unsafe_allow_html=True)
    st.markdown(r"""
    <div class="content-card">
        <h4>1. กฎการสมมูลที่สำคัญ</h4>
        <ul>
            <li>$p \rightarrow q \equiv \neg p \vee q$</li>
            <li>$\neg(p \rightarrow q) \equiv p \wedge \neg q$</li>
            <li>$p \leftrightarrow q \equiv (p \rightarrow q) \wedge (q \rightarrow p)$</li>
            <li>$\neg(p \wedge q) \equiv \neg p \vee \neg q$</li>
            <li>$\neg(p \vee q) \equiv \neg p \wedge \neg q$</li>
        </ul>
        <h4>2. นิเสธตัวบ่งปริมาณ</h4>
        <ul>
            <li>$\neg \forall x P(x) \equiv \exists x \neg P(x)$</li>
            <li>$\neg \exists x P(x) \equiv \forall x \neg P(x)$</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

elif menu == "calculator":
    st.markdown('<div class="section-header">⚡ เครื่องมือคำนวณสัจนิรันดร์อัตโนมัติ</div>', unsafe_allow_html=True)
    expr_in = st.text_input("ป้อนประพจน์ (ใช้ >> แทนการถ้า...แล้ว, | แทนหรือ, & แทนและ):", value="(p >> q) | (q >> p)")
    if st.button("ตรวจสอบ"):
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
