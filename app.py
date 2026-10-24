import streamlit as st
import itertools

st.set_page_config(
    page_title="Math Logic Learning & Solver",
    page_icon="📘",
    layout="wide"
)

st.title("📘 Math Logic Learning & Solver")
st.write("เว็บไซต์สื่อการเรียนรู้ตรรกศาสตร์ทางคณิตศาสตร์")

menu = st.sidebar.selectbox(
    "📚 เลือกเมนู",
    [
        "🏠 หน้าแรก",
        "📚 บทเรียน",
        "🧮 ตารางค่าความจริง",
        "🌳 แผนภาพต้นไม้",
        "📖 รวมสูตรตรรกศาสตร์",
        "📝 แบบฝึกหัด",
        "ℹ️ เกี่ยวกับเว็บไซต์"
    ]
)

lessons = {
    "บทที่ 1 ความรู้เบื้องต้น": {
        "ความหมายของตรรกศาสตร์":
            "ตรรกศาสตร์เป็นศาสตร์ที่ศึกษาหลักการให้เหตุผลอย่างสมเหตุสมผล",
        "ประพจน์":
            "ประพจน์คือประโยคบอกเล่าที่สามารถระบุค่าความจริงได้ว่าเป็นจริงหรือเท็จ",
        "ค่าความจริง":
            "ค่าความจริงประกอบด้วย True (T) และ False (F)"
    },

    "บทที่ 2 ตัวเชื่อมทางตรรกศาสตร์": {
        "นิเสธ":
            "¬p เป็นการเปลี่ยนค่าความจริงของ p ให้ตรงกันข้าม",
        "และ":
            "p ∧ q เป็นจริงเมื่อ p และ q เป็นจริงทั้งคู่",
        "หรือ":
            "p ∨ q เป็นเท็จเมื่อ p และ q เป็นเท็จทั้งคู่",
        "ถ้า...แล้ว":
            "p → q เป็นเท็จเมื่อ p จริง แต่ q เท็จ",
        "ก็ต่อเมื่อ":
            "p ↔ q เป็นจริงเมื่อ p และ q มีค่าความจริงเหมือนกัน"
    },

    "บทที่ 3 สัจนิรันดร์": {
        "สัจนิรันดร์":
            "ประพจน์ที่เป็นจริงในทุกกรณี",
        "ข้อขัดแย้ง":
            "ประพจน์ที่เป็นเท็จในทุกกรณี"
    },

    "บทที่ 4 การอ้างเหตุผล": {
        "Modus Ponens":
            "ถ้า p → q เป็นจริง และ p เป็นจริง จะสรุปได้ว่า q",
        "Modus Tollens":
            "ถ้า p → q เป็นจริง และ ¬q เป็นจริง จะสรุปได้ว่า ¬p"
    },

    "บทที่ 5 ประโยคเปิดและตัวบ่งปริมาณ": {
        "ประโยคเปิด":
            "ประโยคที่มีตัวแปรและยังไม่สามารถระบุค่าความจริงได้จนกว่าจะกำหนดค่าหรือขอบเขต",
        "Universal Quantifier":
            "∀ หมายถึง สำหรับทุกตัว",
        "Existential Quantifier":
            "∃ หมายถึง มีอย่างน้อยหนึ่งตัว"
    },

    "บทที่ 6 การให้เหตุผล": {
        "อุปนัย":
            "การสรุปหลักการทั่วไปจากกรณีตัวอย่าง",
        "นิรนัย":
            "การสรุปผลจากหลักการหรือเหตุที่กำหนด"
    }
}

if menu == "🏠 หน้าแรก":
    st.header("ยินดีต้อนรับ")
    st.info("เรียนรู้ตรรกศาสตร์ผ่านบทเรียน ตารางค่าความจริง และแบบฝึกหัด")

elif menu == "📚 บทเรียน":
    chapter = st.selectbox("เลือกบทเรียน", list(lessons.keys()))

    topic = st.selectbox(
        "เลือกหัวข้อย่อย",
        list(lessons[chapter].keys())
    )

    st.subheader(topic)
    st.write(lessons[chapter][topic])

elif menu == "🧮 ตารางค่าความจริง":
    st.header("Truth Table Generator")

    operation = st.selectbox(
        "เลือกตัวเชื่อม",
        ["AND", "OR", "IMPLIES", "BICONDITIONAL"]
    )

    def calculate(p, q, operation):
        if operation == "AND":
            return p and q
        elif operation == "OR":
            return p or q
        elif operation == "IMPLIES":
            return (not p) or q
        elif operation == "BICONDITIONAL":
            return p == q

    rows = []

    for p, q in itertools.product([True, False], repeat=2):
        result = calculate(p, q, operation)

        rows.append({
            "p": "T" if p else "F",
            "q": "T" if q else "F",
            "ผลลัพธ์": "T" if result else "F"
        })

    st.table(rows)

elif menu == "🌳 แผนภาพต้นไม้":
    st.header("🌳 Truth Tree")

    st.write("ตัวอย่างแผนภาพต้นไม้ทางตรรกศาสตร์")

    st.code("""
       F(p ∨ ¬p)
            |
           Fp
            |
          F(¬p)
            |
           Tp
            |
            ×
         กิ่งปิด
    """)

    st.info("ตัวอย่างนี้แสดงการตรวจสอบสัจนิรันดร์ด้วยแผนภาพต้นไม้")

elif menu == "📖 รวมสูตรตรรกศาสตร์":
    st.header("สูตรสำคัญ")

    st.latex(r"\neg(p \land q) \equiv \neg p \lor \neg q")
    st.latex(r"\neg(p \lor q) \equiv \neg p \land \neg q")
    st.latex(r"p \rightarrow q \equiv \neg p \lor q")
    st.latex(r"p \leftrightarrow q \equiv (p \rightarrow q)\land(q \rightarrow p)")

elif menu == "📝 แบบฝึกหัด":
    st.header("แบบฝึกหัดตรรกศาสตร์")

    answer = st.radio(
        "ประพจน์ p ∧ q เป็นจริงเมื่อใด?",
        [
            "p จริง และ q จริง",
            "p จริง และ q เท็จ",
            "p เท็จ และ q จริง"
        ]
    )

    if st.button("ตรวจคำตอบ"):
        if answer == "p จริง และ q จริง":
            st.success("ถูกต้อง!")
        else:
            st.error("ยังไม่ถูกต้อง ลองใหม่อีกครั้ง")

elif menu == "ℹ️ เกี่ยวกับเว็บไซต์":
    st.header("About")
    st.write("เว็บไซต์นี้จัดทำขึ้นเพื่อส่งเสริมการเรียนรู้ตรรกศาสตร์ทางคณิตศาสตร์")
