import streamlit as st
import pandas as pd
import sympy as sp
import itertools

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="ตรรกศาสตร์เชิงคณิตศาสตร์ | Interactive Truth Tables",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Minimalist Clean White Theme & Custom CSS
# ---------------------------------------------------------
st.markdown("""
<style>
    .stApp {
        background-color: #F8FAFC;
        color: #1E293B;
        font-family: 'Sarabun', -apple-system, sans-serif;
    }
    .main-title-box {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    .main-title-text {
        font-size: 24px;
        font-weight: 700;
        color: #0F172A;
        margin: 0;
    }
    .section-header {
        font-size: 18px;
        font-weight: 700;
        color: #2563EB;
        border-left: 4px solid #2563EB;
        padding-left: 10px;
        margin-top: 20px;
        margin-bottom: 15px;
    }
    .content-box {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
    }
    .solution-box {
        background-color: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-radius: 8px;
        padding: 15px;
        color: #166534;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Helper Function: Generator ตารางค่าความจริง
# ---------------------------------------------------------
def generate_truth_table(variables, expr_str):
    """สร้าง Pandas DataFrame ตารางค่าความจริงอัตโนมัติ"""
    combos = list(itertools.product([True, False], repeat=len(variables)))
    data = []
    expr = sp.sympify(expr_str)
    
    for cb in combos:
        mapping = dict(zip([sp.Symbol(v) for v in variables], cb))
        res = bool(expr.subs(mapping))
        row = list(cb) + [res]
        data.append(row)
        
    cols = variables + [expr_str]
    df = pd.DataFrame(data, columns=cols)
    # แปลง True/False ให้แสดงผลชัดเจนเป็น T/F
    return df.map(lambda x: 'T' if x is True else ('F' if x is False else x))

# ---------------------------------------------------------
# Sidebar Navigation
# ---------------------------------------------------------
st.sidebar.markdown("### 📚 เมนูบทเรียน")

menu_choice = st.sidebar.radio(
    "เลือกหัวข้อที่ต้องการศึกษา:",
    [
        "บทที่ 1: ประพจน์และการให้เหตุผล",
        "บทที่ 2: ตัวเชื่อมและตารางค่าความจริง",
        "บทที่ 3: สัจนิรันดร์และข้อขัดแย้ง",
        "บทที่ 4: การอ้างเหตุผล",
        "บทที่ 5: ประโยคเปิดและตัวบ่งปริมาณ",
        "บทที่ 6: การอุปนัยเชิงคณิตศาสตร์",
        "สรุปสูตรทั้งหมด",
        "เครื่องมือสร้างตารางค่าความจริงอัตโนมัติ"
    ]
)

# ---------------------------------------------------------
# Main Content Area
# ---------------------------------------------------------
st.markdown("""
<div class="main-title-box">
    <div class="main-title-text">📐 สื่อการเรียนรู้วิชาตรรกศาสตร์เชิงคณิตศาสตร์</div>
</div>
""", unsafe_allow_html=True)

# --- บทที่ 1 ---
if menu_choice == "บทที่ 1: ประพจน์และการให้เหตุผล":
    st.markdown('<div class="section-header">📘 บทที่ 1: ประพจน์และการให้เหตุผล</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.markdown("### 📖 เนื้อหาและแนวคิดหลัก")
    st.write("ประพจน์ คือ ประโยคบอกเล่าหรือประโยคปฏิเสธที่มีค่าความจริงเป็นจริง (True) หรือเท็จ (False) อย่างใดอย่างหนึ่งเท่านั้น")
    
    st.markdown("#### กฎการอ้างเหตุผลเบื้องต้น:")
    st.markdown("1. **Modus Ponens:**")
    st.latex(r"p, p \rightarrow q \vdash q")
    st.markdown("2. **Modus Tollens:**")
    st.latex(r"p \rightarrow q, \neg q \vdash \neg p")
    st.markdown('</div>', unsafe_allow_html=True)
    
    with st.expander("💡 ตัวอย่างพร้อมวิธีทำ"):
        st.markdown("**โจทย์:** จงพิจารณาว่าประโยค 'ถ้า $x^2 < 0$ แล้ว $x$ เป็นจำนวนจริง' มีค่าความจริงเป็นอย่างไร?")
        st.markdown('<div class="solution-box"><b>วิธีทำ:</b><br>1. ให้ $p$ คือ $x^2 < 0$ และ $q$ คือ $x$ เป็นจำนวนจริง<br>2. ประพจน์เหตุ $p$ เป็นเท็จเสมอในระบบจำนวนจริง<br>3. ประพจน์ผล $q$ เป็นจริง<br>4. ตามนิยามประพจน์เงื่อนไข $F \\rightarrow T$ จะได้ค่าความจริงเป็น <b>จริง (True)</b></div>', unsafe_allow_html=True)

# --- บทที่ 2 ---
elif menu_choice == "บทที่ 2: ตัวเชื่อมและตารางค่าความจริง":
    st.markdown('<div class="section-header">📗 บทที่ 2: ตัวเชื่อมและตารางค่าความจริง</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.markdown("### 📊 ตารางค่าความจริงพื้นฐานของตัวเชื่อมทางตรรกศาสตร์")
    
    # ตารางตัวเชื่อมพื้นฐาน
    df_basic = pd.DataFrame({
        "p": ["T", "T", "F", "F"],
        "q": ["T", "F", "T", "F"],
        "p ∧ q (และ)": ["T", "F", "F", "F"],
        "p ∨ q (หรือ)": ["T", "T", "T", "F"],
        "p → q (ถ้า...แล้ว)": ["T", "F", "T", "T"],
        "p ↔ q (ก็ต่อเมื่อ)": ["T", "F", "F", "T"]
    })
    st.dataframe(df_basic, use_container_width=True, hide_index=True)
    
    st.markdown("#### กฎเดอมอร์แกน (De Morgan's Laws):")
    st.latex(r"\neg(p \wedge q) \equiv \neg p \vee \neg q")
    st.latex(r"\neg(p \vee q) \equiv \neg p \wedge \neg q")
    st.markdown('</div>', unsafe_allow_html=True)
    
    with st.expander("💡 ตัวอย่างตารางค่าความจริงของ (p ∧ q) → p"):
        st.markdown("**ตารางค่าความจริงของประพจน์ $(p \\wedge q) \\rightarrow p$:**")
        df_ex = generate_truth_table(['p', 'q'], '(p & q) >> p')
        st.dataframe(df_ex, use_container_width=True, hide_index=True)

# --- บทที่ 3 ---
elif menu_choice == "บทที่ 3: สัจนิรันดร์และข้อขัดแย้ง":
    st.markdown('<div class="section-header">📙 บทที่ 3: สัจนิรันดร์และข้อขัดแย้ง</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.markdown("### 📖 นิยาม")
    st.write("• **สัจนิรันดร์ (Tautology):** ประพจน์ที่มีค่าความจริงในตารางค่าความจริงเป็นจริง (T) ทุกกรณี")
    st.write("• **ข้อขัดแย้ง (Contradiction):** ประพจน์ที่มีค่าความจริงในตารางค่าความจริงเป็นเท็จ (F) ทุกกรณี")
    
    st.markdown("#### ตัวอย่างตารางค่าความจริงสัจนิรันดร์ ($p \\vee \\neg p$):")
    df_taut = generate_truth_table(['p'], 'p | ~p')
    st.dataframe(df_taut, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- บทที่ 4 ---
elif menu_choice == "บทที่ 4: การอ้างเหตุผล":
    st.markdown('<div class="section-header">📕 บทที่ 4: การอ้างเหตุผลและความสมเหตุสมผล</div>', unsafe_allow_html=True)
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.markdown("### 📖 แนวคิดการอ้างเหตุผล")
    st.write("การอ้างเหตุผลประกอบด้วยเหตุ (Premises) และผลสรุป (Conclusion) จะสมเหตุสมผลก็ต่อเมื่อเหตุทุกข้อเป็นจริงแล้วผลสรุปต้องเป็นจริงตามเสมอ")
    st.markdown('</div>', unsafe_allow_html=True)

# --- บทที่ 5 ---
elif menu_choice == "บทที่ 5: ประโยคเปิดและตัวบ่งปริมาณ":
    st.markdown('<div class="section-header">🟣 บทที่ 5: ประโยคเปิดและตัวบ่งปริมาณ</div>', unsafe_allow_html=True)
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.markdown("### 📖 นิเสธของตัวบ่งปริมาณ")
    st.latex(r"\neg \forall x P(x) \equiv \exists x \neg P(x)")
    st.latex(r"\neg \exists x P(x) \equiv \forall x \neg P(x)")
    st.markdown('</div>', unsafe_allow_html=True)

# --- บทที่ 6 ---
elif menu_choice == "บทที่ 6: การอุปนัยเชิงคณิตศาสตร์":
    st.markdown('<div class="section-header">📓 บทที่ 6: การอุปนัยเชิงคณิตศาสตร์</div>', unsafe_allow_html=True)
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.markdown("### 📖 สูตรอนุกรมสำคัญ")
    st.markdown("• ผลบวกกำลังสาม $n$ พจน์แรก:")
    st.latex(r"1^3 + 2^3 + \dots + n^3 = \left[\frac{n(n+1)}{2}\right]^2")
    st.markdown('</div>', unsafe_allow_html=True)

# --- สรุปสูตร ---
elif menu_choice == "สรุปสูตรทั้งหมด":
    st.markdown('<div class="section-header">📐 สรุปสูตรและกฎสำคัญทางตรรกศาสตร์</div>', unsafe_allow_html=True)
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.markdown("### กฎสมมูลที่สำคัญ:")
    st.latex(r"p \rightarrow q \equiv \neg p \vee q")
    st.latex(r"p \leftrightarrow q \equiv (p \rightarrow q) \wedge (q \rightarrow p)")
    st.markdown('</div>', unsafe_allow_html=True)

# --- เครื่องมือตารางค่าความจริง ---
elif menu_choice == "เครื่องมือสร้างตารางค่าความจริงอัตโนมัติ":
    st.markdown('<div class="section-header">⚡ เครื่องมือสร้างตารางค่าความจริงอัตโนมัติ (Interactive Truth Table Generator)</div>', unsafe_allow_html=True)
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        vars_input = st.text_input("ตัวแปร (คั่นด้วยเครื่องหมายจุลภาค ,):", value="p, q")
        expr_input = st.text_input("นิพจน์เชิงตรรกศาสตร์:", value="(p & q) >> p")
        st.caption("สัญลักษณ์ที่ใช้ได้: `&` (และ), `|` (หรือ), `~` (นิเสธ), `>>` (ถ้า...แล้ว)")
        btn_gen = st.button("🚀 สร้างตารางค่าความจริง")
        
    with col2:
        if btn_gen or expr_input:
            try:
                var_list = [v.strip() for v in vars_input.split(",") if v.strip()]
                df_result = generate_truth_table(var_list, expr_input)
                st.markdown(f"**ผลลัพธ์ตารางค่าความจริงของ `{expr_input}`:**")
                st.dataframe(df_result, use_container_width=True, hide_index=True)
            except Exception as e:
                st.error(f"รูปแบบนิพจน์ไม่ถูกต้อง: {e}")
    st.markdown('</div>', unsafe_allow_html=True)
