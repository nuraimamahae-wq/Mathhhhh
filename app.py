import streamlit as st
import itertools
import re
import pandas as pd
# =========================
# ตั้งค่าเว็บไซต์
# =========================
st.set_page_config(
    page_title="Math Logic Learning & Solver",
    page_icon="📘",
    layout="wide"
)
# =========================
# เมนูด้านซ้าย
# =========================
st.sidebar.title("📘 Math Logic")
st.sidebar.write("Mathematical Logic Learning")
st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "เลือกเมนูที่ต้องการ",
    [
        "🏠 หน้าแรก",
        "📚 บทที่ 1 ความรู้เบื้องต้น",
        "📚 บทที่ 2 ตัวเชื่อมตรรกศาสตร์",
        "📚 บทที่ 3 สัจนิรันดร์",
        "📚 บทที่ 4 การอ้างเหตุผล",
        "📚 บทที่ 5 ประโยคเปิดและตัวบ่งปริมาณ",
        "📚 บทที่ 6 การให้เหตุผล",
        "🧮 ตารางค่าความจริง",
        "🧠 เครื่องตรวจสูตรตรรกศาสตร์",
        "🌳 แผนภาพต้นไม้",
        "📖 รวมสูตรตรรกศาสตร์",
        "📝 แบบฝึกหัด",
        "🎮 เกมตรรกศาสตร์",
        "📊 แบบทดสอบ",
        "ℹ️ เกี่ยวกับเว็บไซต์"
    ]
)
st.sidebar.markdown("---")
st.sidebar.caption("Learn • Practice • Solve")
# =========================
# เนื้อหาบทเรียน
# =========================
lessons = {
    "📚 บทที่ 1 ความรู้เบื้องต้น": {
        "ความหมายของตรรกศาสตร์": """
ตรรกศาสตร์ทางคณิตศาสตร์เป็นการศึกษาเกี่ยวกับประพจน์
ค่าความจริง และการให้เหตุผลอย่างเป็นระบบ
ตรรกศาสตร์ช่วยให้เราตรวจสอบได้ว่าข้อสรุป
มีความสมเหตุสมผลจากเหตุที่กำหนดหรือไม่
""",
        "ประพจน์": """
ประพจน์ คือ ประโยคบอกเล่าที่สามารถระบุค่าความจริงได้
ว่าเป็นจริง (True: T) หรือเท็จ (False: F)
ตัวอย่าง
- 2 เป็นจำนวนคู่ : จริง
- 5 น้อยกว่า 3 : เท็จ
- กรุณาปิดประตู : ไม่เป็นประพจน์
- x + 2 = 5 : เป็นประโยคเปิดเมื่อยังไม่กำหนดค่า x
""",
        "ไวยากรณ์และความหมาย": """
ไวยากรณ์ (Syntax) คือ รูปแบบการเขียนสูตรตรรกศาสตร์
ความหมาย (Semantics) คือ การพิจารณาค่าความจริงของสูตร
"""
    },
    "📚 บทที่ 2 ตัวเชื่อมตรรกศาสตร์": {
        "ตัวเชื่อมตรรกศาสตร์": """
¬p อ่านว่า ไม่ p (นิเสธ)
p ∧ q อ่านว่า p และ q
p ∨ q อ่านว่า p หรือ q
p → q อ่านว่า ถ้า p แล้ว q
p ↔ q อ่านว่า p ก็ต่อเมื่อ q
""",
        "ความหมายของตัวเชื่อม": """
1. ¬p เป็นจริงเมื่อ p เป็นเท็จ
2. p ∧ q เป็นจริงเมื่อ p และ q เป็นจริงทั้งคู่
3. p ∨ q เป็นจริงเมื่อมีอย่างน้อยหนึ่งประพจน์เป็นจริง
4. p → q เป็นเท็จเฉพาะเมื่อ p จริง แต่ q เท็จ
5. p ↔ q เป็นจริงเมื่อ p และ q มีค่าความจริงเหมือนกัน
""",
        "ตารางค่าความจริงเบื้องต้น": """
ถ้ามีตัวแปร p และ q จะมีค่าความจริงทั้งหมด 4 กรณี
1. p = T, q = T
2. p = T, q = F
3. p = F, q = T
4. p = F, q = F
ถ้ามีตัวแปร n ตัว จะมีจำนวนแถวเท่ากับ 2ⁿ
"""
    },
    "📚 บทที่ 3 สัจนิรันดร์": {
        "สัจนิรันดร์": """
สัจนิรันดร์ (Tautology) คือสูตรที่มีค่าความจริงเป็นจริง
ทุกกรณี
ตัวอย่าง
p ∨ ¬p
ไม่ว่า p จะเป็นจริงหรือเท็จ สูตรนี้จะเป็นจริงเสมอ
""",
        "ข้อขัดแย้ง": """
ข้อขัดแย้ง (Contradiction) คือสูตรที่มีค่าความจริงเป็นเท็จ
ทุกกรณี
ตัวอย่าง
p ∧ ¬p
เพราะ p และ ¬p ไม่สามารถเป็นจริงพร้อมกันได้
""",
        "สมมูลทางตรรกศาสตร์": """
สูตรสองสูตรสมมูลกัน เมื่อมีค่าความจริงตรงกันทุกกรณี
สัญลักษณ์ ≡ ใช้แทนความสมมูลทางตรรกศาสตร์
ตัวอย่าง
¬(p ∧ q) ≡ ¬p ∨ ¬q
¬(p ∨ q) ≡ ¬p ∧ ¬q
"""
    },
    "📚 บทที่ 4 การอ้างเหตุผล": {
        "ความหมายของการอ้างเหตุผล": """
การอ้างเหตุผลประกอบด้วยเหตุ (Premises)
และผลสรุป (Conclusion)
การอ้างเหตุผลสมเหตุสมผล เมื่อไม่มีกรณีที่เหตุทุกข้อจริง
แต่ผลสรุปเป็นเท็จ
""",
        "Modus Ponens": """
รูปแบบการอ้างเหตุผล
1. p → q
2. p
ดังนั้น q
ตัวอย่าง
ถ้าฝนตก ถนนจะเปียก
ฝนตก
ดังนั้น ถนนเปียก
""",
        "Modus Tollens": """
รูปแบบการอ้างเหตุผล
1. p → q
2. ¬q
ดังนั้น ¬p
เป็นรูปแบบการให้เหตุผลที่ใช้การปฏิเสธผล
เพื่อนำไปสู่การปฏิเสธเหตุ
""",
        "การอ้างเหตุผลที่ไม่สมเหตุสมผล": """
ตัวอย่างรูปแบบที่ไม่สมเหตุสมผล
1. p → q
2. q
ดังนั้น p
รูปแบบนี้เรียกว่า Affirming the Consequent
เพราะ q อาจเกิดจากเหตุอื่นได้
"""
    },
    "📚 บทที่ 5 ประโยคเปิดและตัวบ่งปริมาณ": {
        "ประโยคเปิด": """
ประโยคเปิดเป็นประโยคที่มีตัวแปร
ค่าความจริงขึ้นอยู่กับค่าที่นำมาแทนตัวแปร
ตัวอย่าง
x > 3
เมื่อ x = 5 ข้อความเป็นจริง
เมื่อ x = 2 ข้อความเป็นเท็จ
""",
        "ตัวบ่งปริมาณ": """
∀x P(x) อ่านว่า สำหรับทุก x, P(x)
∃x P(x) อ่านว่า มี x อย่างน้อยหนึ่งตัวที่ P(x)
∀ เรียกว่า ตัวบ่งปริมาณสากล
∃ เรียกว่า ตัวบ่งปริมาณมีอยู่
""",
        "นิเสธของตัวบ่งปริมาณ": """
กฎที่ควรจำ
¬(∀x P(x)) ≡ ∃x ¬P(x)
¬(∃x P(x)) ≡ ∀x ¬P(x)
การนิเสธข้อความว่า ทุกตัวมีสมบัติ P
คือ มีอย่างน้อยหนึ่งตัวที่ไม่มีสมบัติ P
"""
    },
    "📚 บทที่ 6 การให้เหตุผล": {
        "การให้เหตุผลแบบนิรนัย": """
การให้เหตุผลแบบนิรนัย (Deductive Reasoning)
เริ่มจากหลักการทั่วไปแล้วนำมาใช้กับกรณีเฉพาะ
หากเหตุเป็นจริงและรูปแบบการให้เหตุผลถูกต้อง
ผลสรุปจะตามมาจากเหตุ
""",
        "การให้เหตุผลแบบอุปนัย": """
การให้เหตุผลแบบอุปนัย (Inductive Reasoning)
เริ่มจากการสังเกตตัวอย่างหลายกรณี
แล้วนำมาคาดคะเนเป็นข้อสรุปทั่วไป
ข้อสรุปจากการอุปนัยอาจผิดได้
หากมีตัวอย่างที่ไม่เป็นไปตามรูปแบบ
""",
        "อุปนัยเชิงคณิตศาสตร์": """
การพิสูจน์โดยอุปนัยเชิงคณิตศาสตร์มีขั้นตอนสำคัญ
1. ขั้นฐาน (Base Case)
พิสูจน์ว่าข้อความจริงสำหรับค่าเริ่มต้น
2. ขั้นอุปนัย (Inductive Step)
สมมติว่าข้อความจริงเมื่อ n = k
แล้วพิสูจน์ว่าข้อความจริงเมื่อ n = k + 1
"""
    }
}
# =========================
# ฟังก์ชันสร้างตารางค่าความจริง
# =========================
def tokenize(expression):
    pattern = r"<->|↔|->|→|[()¬~!∧&∨|]|[A-Za-z][A-Za-z0-9_]*"
    tokens = re.findall(pattern, expression)
    cleaned = re.sub(r"\s+", "", expression)
    normalized_input = expression
    for old, new in [
        ("<->", "↔"),
        ("->", "→"),
        ("~", "¬"),
        ("!", "¬"),
        ("&", "∧"),
        ("|", "∨")
    ]:
        normalized_input = normalized_input.replace(old, new)
    normalized_input = re.sub(r"\s+", "", normalized_input)
    normalized_tokens = []
    for token in tokens:
        token = {
            "<->": "↔",
            "->": "→",
            "~": "¬",
            "!": "¬",
            "&": "∧",
            "|": "∨"
        }.get(token, token)
        normalized_tokens.append(token)
    if "".join(normalized_tokens) != normalized_input:
        raise ValueError(
            "สูตรมีสัญลักษณ์ที่ไม่รองรับ กรุณาตรวจสอบสูตรอีกครั้ง"
        )
    return normalized_tokens
class FormulaParser:
    def __init__(self, tokens, values):
        self.tokens = tokens
        self.values = values
        self.position = 0
    def peek(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None
    def take(self, expected=None):
        token = self.peek()
        if token is None:
            raise ValueError("สูตรไม่สมบูรณ์")
        if expected is not None and token != expected:
            raise ValueError(f"คาดว่าจะพบ {expected}")
        self.position += 1
        return token
    def parse(self):
        result = self.parse_iff()
        if self.peek() is not None:
            raise ValueError(f"มีสัญลักษณ์เกิน: {self.peek()}")
        return result
    def parse_iff(self):
        left = self.parse_implies()
        while self.peek() == "↔":
            self.take()
            right = self.parse_implies()
            left = left == right
        return left
    def parse_implies(self):
        left = self.parse_or()
        if self.peek() == "→":
            self.take()
            right = self.parse_implies()
            return (not left) or right
        return left
    def parse_or(self):
        left = self.parse_and()
        while self.peek() == "∨":
            self.take()
            right = self.parse_and()
            left = left or right
        return left
    def parse_and(self):
        left = self.parse_not()
        while self.peek() == "∧":
            self.take()
            right = self.parse_not()
            left = left and right
        return left
    def parse_not(self):
        if self.peek() == "¬":
            self.take()
            return not self.parse_not()
        return self.parse_atom()
    def parse_atom(self):
        token = self.peek()
        if token == "(":
            self.take("(")
            result = self.parse_iff()
            self.take(")")
            return result
        if token is None:
            raise ValueError("สูตรไม่สมบูรณ์")
        if token in ("∧", "∨", "→", "↔", ")"):
            raise ValueError(f"ตำแหน่งตัวเชื่อมไม่ถูกต้องใกล้ {token}")
        self.take()
        if token.upper() == "T":
            return True
        if token.upper() == "F":
            return False
        if token not in self.values:
            raise ValueError(f"ไม่พบค่าความจริงของตัวแปร {token}")
        return bool(self.values[token])
def evaluate_formula(expression, values):
    tokens = tokenize(expression)
    return FormulaParser(tokens, values).parse()
def get_variables(expression):
    tokens = tokenize(expression)
    return sorted({
        token for token in tokens
        if re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", token)
        and token.upper() not in ("T", "F")
    })
def create_truth_table(expression):
    variables = get_variables(expression)
    if len(variables) > 8:
        raise ValueError("ระบบรองรับตัวแปรไม่เกิน 8 ตัว")
    rows = []
    for combination in itertools.product(
        [True, False],
        repeat=len(variables)
    ):
        values = dict(zip(variables, combination))
        result = evaluate_formula(expression, values)
        row = {
            variable: "T" if values[variable] else "F"
            for variable in variables
        }
        row[expression] = "T" if result else "F"
        rows.append(row)
    return pd.DataFrame(rows)
# =========================
# หน้าแรก
# =========================
if menu == "🏠 หน้าแรก":
    st.title("📘 Math Logic Learning & Solver")
    st.subheader("เว็บไซต์เรียนรู้ตรรกศาสตร์ทางคณิตศาสตร์")
    st.write("""
    เว็บไซต์นี้จัดทำขึ้นเพื่อช่วยทบทวนเนื้อหาตรรกศาสตร์ทางคณิตศาสตร์
    และฝึกตรวจสอบค่าความจริงของประพจน์
    """)
    col1, col2, col3 = st.columns(3)
    col1.metric("บทเรียน", "6 บท")
    col2.metric("เครื่องมือ", "2 แบบ")
    col3.metric("กิจกรรม", "3 แบบ")
    st.markdown("### วิธีใช้งานเว็บไซต์")
    st.markdown("""
    1. เลือกบทเรียนจากเมนูด้านซ้าย
    2. ทดลองสร้างตารางค่าความจริง
    3. ตรวจสอบสูตรตรรกศาสตร์
    4. ทบทวนสูตรที่สำคัญ
    5. ฝึกทำแบบฝึกหัด เกม และแบบทดสอบ
    """)
    st.info("ตัวอย่างสูตรที่ทดลองได้: p ∧ q, ¬p ∨ q, p → q")
# =========================
# แสดงบทเรียน
# =========================
elif menu in lessons:
    st.title(menu)
    topics = lessons[menu]
    topic = st.selectbox("เลือกหัวข้อย่อย", list(topics.keys()))
    st.markdown(topics[topic])
# =========================
# ตารางค่าความจริง
# =========================
elif menu == "🧮 ตารางค่าความจริง":
    st.title("🧮 ตารางค่าความจริง")
    st.write("กรอกสูตรตรรกศาสตร์ที่ต้องการตรวจสอบ")
    expression = st.text_input(
        "สูตรตรรกศาสตร์",
        value="(p → q) ∧ p"
    )
    st.caption(
        "ใช้ p, q, r และตัวเชื่อม ¬, ∧, ∨, →, ↔ "
        "รวมถึงวงเล็บ"
    )
    if st.button("สร้างตารางค่าความจริง"):
        try:
            table = create_truth_table(expression)
            st.success("สร้างตารางเรียบร้อยแล้ว")
            st.dataframe(
                table,
                use_container_width=True,
                hide_index=True
            )
        except Exception as error:
            st.error(f"เกิดข้อผิดพลาด: {error}")
# =========================
# เครื่องตรวจสูตร
# =========================
elif menu == "🧠 เครื่องตรวจสูตรตรรกศาสตร์":
    st.title("🧠 เครื่องตรวจสูตรตรรกศาสตร์")
    expression = st.text_input(
        "กรอกสูตรที่ต้องการตรวจ",
        value="p ∨ ¬p"
    )
    if st.button("ตรวจสอบสูตร"):
        try:
            table = create_truth_table(expression)
            results = table[expression].tolist()
            if all(value == "T" for value in results):
                st.success("ผลลัพธ์: สัจนิรันดร์ (Tautology)")
            elif all(value == "F" for value in results):
                st.error("ผลลัพธ์: ข้อขัดแย้ง (Contradiction)")
            else:
                st.info(
                    "ผลลัพธ์: เป็นจริงบางกรณีและเป็นเท็จบางกรณี "
                    "(Contingency)"
                )
            st.dataframe(
                table,
                use_container_width=True,
                hide_index=True
            )
        except Exception as error:
            st.error(f"เกิดข้อผิดพลาด: {error}")
# =========================
# แผนภาพต้นไม้
# =========================
elif menu == "🌳 แผนภาพต้นไม้":
    st.title("🌳 แผนภาพต้นไม้ (Truth Tree)")
    example = st.selectbox(
        "เลือกตัวอย่าง",
        [
            "p ∨ ¬p",
            "p ∧ ¬p",
            "p → q"
        ]
    )
    if example == "p ∨ ¬p":
        st.subheader("ตัวอย่าง: p ∨ ¬p")
        st.write("""
        สมมติให้ p ∨ ¬p เป็นเท็จ
        จะต้องได้ว่า p เป็นเท็จ และ ¬p เป็นเท็จ
        แต่ถ้า p เป็นเท็จ จะทำให้ ¬p เป็นจริง
        จึงเกิดความขัดแย้ง
        """)
        st.code("""
F(p ∨ ¬p)
├── F(p)
└── F(¬p) → T(p)
    เกิดความขัดแย้ง
        """)
        st.success("สูตรนี้เป็นสัจนิรันดร์")
    elif example == "p ∧ ¬p":
        st.subheader("ตัวอย่าง: p ∧ ¬p")
        st.write("""
        หากสมมติให้ p ∧ ¬p เป็นจริง
        จะต้องได้ว่า p เป็นจริงและ ¬p เป็นจริง
        ซึ่งหมายความว่า p ต้องเป็นทั้งจริงและเท็จ
        จึงเกิดความขัดแย้ง
        """)
        st.code("""
T(p ∧ ¬p)
├── T(p)
└── T(¬p) → F(p)
    เกิดความขัดแย้ง
        """)
        st.success("สูตรนี้เป็นข้อขัดแย้ง")
    else:
        st.subheader("ตัวอย่าง: p → q")
        st.write("""
        ถ้า p → q เป็นเท็จ จะต้องมี p เป็นจริงและ q เป็นเท็จ
        """)
        st.code("""
F(p → q)
├── T(p)
└── F(q)
        """)
    st.warning(
        "ส่วนนี้เป็นตัวอย่างเพื่อการเรียนรู้ "
        "ยังไม่ได้สร้างแผนภาพต้นไม้ให้อัตโนมัติสำหรับทุกสูตร"
    )
# =========================
# รวมสูตร
# =========================
elif menu == "📖 รวมสูตรตรรกศาสตร์":
    st.title("📖 รวมสูตรตรรกศาสตร์")
    formulas = [
        ("กฎนิเสธซ้อน", r"\neg(\neg p) \equiv p"),
        (
            "กฎของเดอมอร์แกน",
            r"\neg(p \land q) \equiv \neg p \lor \neg q"
        ),
        (
            "กฎของเดอมอร์แกน",
            r"\neg(p \lor q) \equiv \neg p \land \neg q"
        ),
        (
            "อิมพลิเคชัน",
            r"p \to q \equiv \neg p \lor q"
        ),
        (
            "สมมูล",
            r"p \leftrightarrow q \equiv "
            r"(p \to q) \land (q \to p)"
        ),
        (
            "กฎสลับที่ของ และ",
            r"p \land q \equiv q \land p"
        ),
        (
            "กฎสลับที่ของ หรือ",
            r"p \lor q \equiv q \lor p"
        ),
        (
            "นิเสธตัวบ่งปริมาณสากล",
            r"\neg(\forall x\,P(x)) "
            r"\equiv \exists x\,\neg P(x)"
        ),
        (
            "นิเสธตัวบ่งปริมาณมีอยู่",
            r"\neg(\exists x\,P(x)) "
            r"\equiv \forall x\,\neg P(x)"
        )
    ]
    for title, formula in formulas:
        st.markdown(f"**{title}**")
        st.latex(formula)
        st.markdown("---")
# =========================
# แบบฝึกหัด
# =========================
elif menu == "📝 แบบฝึกหัด":
    st.title("📝 แบบฝึกหัดตรรกศาสตร์")
    questions = [
        {
            "question": "1. ถ้า p เป็นจริง ¬p จะเป็นอย่างไร?",
            "options": ["จริง", "เท็จ"],
            "answer": "เท็จ",
            "explain": "นิเสธของประพจน์จริงเป็นเท็จ"
        },
        {
            "question": "2. p ∧ q เป็นจริงเมื่อใด?",
            "options": [
                "p และ q จริงทั้งคู่",
                "p หรือ q จริงอย่างน้อยหนึ่งตัว"
            ],
            "answer": "p และ q จริงทั้งคู่",
            "explain": "ตัวเชื่อม ∧ ต้องให้ทั้งสองประพจน์เป็นจริง"
        },
        {
            "question": "3. p ∨ ¬p เป็นสูตรชนิดใด?",
            "options": ["สัจนิรันดร์", "ข้อขัดแย้ง"],
            "answer": "สัจนิรันดร์",
            "explain": "สูตรนี้เป็นจริงทุกกรณี"
        },
        {
            "question": "4. p → q เป็นเท็จเมื่อใด?",
            "options": [
                "p จริงและ q เท็จ",
                "p เท็จและ q จริง"
            ],
            "answer": "p จริงและ q เท็จ",
            "explain": "อิมพลิเคชันเป็นเท็จเฉพาะกรณีนี้"
        },
        {
            "question": "5. ∀x หมายถึงอะไร?",
            "options": [
                "สำหรับทุก x",
                "มี x อย่างน้อยหนึ่งตัว"
            ],
            "answer": "สำหรับทุก x",
            "explain": "∀ เป็นตัวบ่งปริมาณสากล"
        }
    ]
    with st.form("exercise_form"):
        answers = []
        for i, question in enumerate(questions):
            answer = st.radio(
                question["question"],
                question["options"],
                key=f"exercise_{i}"
            )
            answers.append(answer)
        submitted = st.form_submit_button("ตรวจคำตอบ")
    if submitted:
        score = 0
        for i, question in enumerate(questions):
            if answers[i] == question["answer"]:
                score += 1
                st.success(f"ข้อ {i + 1}: ถูกต้อง")
            else:
                st.error(
                    f"ข้อ {i + 1}: คำตอบที่ถูกคือ "
                    f"{question['answer']}"
                )
            st.caption(question["explain"])
        st.metric("คะแนนรวม", f"{score} / {len(questions)}")
# =========================
# เกมตรรกศาสตร์
# =========================
elif menu == "🎮 เกมตรรกศาสตร์":
    st.title("🎮 เกมจับคู่ตัวเชื่อมตรรกศาสตร์")
    pairs = [
        ("¬p", "นิเสธ p"),
        ("p ∧ q", "p และ q"),
        ("p ∨ q", "p หรือ q"),
        ("p → q", "ถ้า p แล้ว q"),
        ("p ↔ q", "p ก็ต่อเมื่อ q")
    ]
    choices = [
        "นิเสธ p",
        "p และ q",
        "p หรือ q",
        "ถ้า p แล้ว q",
        "p ก็ต่อเมื่อ q"
    ]
    with st.form("game_form"):
        answers = {}
        for symbol, meaning in pairs:
            answers[symbol] = st.selectbox(
                f"{symbol} หมายถึงอะไร?",
                choices,
                key=f"game_{symbol}"
            )
        submitted = st.form_submit_button("ตรวจคะแนน")
    if submitted:
        score = sum(
            answers[symbol] == meaning
            for symbol, meaning in pairs
        )
        st.metric("คะแนนเกม", f"{score} / {len(pairs)}")
        if score == len(pairs):
            st.balloons()
            st.success("ยอดเยี่ยม! ตอบถูกทุกข้อ")
        else:
            st.info("ลองทบทวนบทที่ 2 แล้วเล่นอีกครั้ง")
# =========================
# แบบทดสอบ
# =========================
elif menu == "📊 แบบทดสอบ":
    st.title("📊 แบบทดสอบท้ายบท")
    quiz = [
        (
            "1. สัญลักษณ์ใดแทนการนิเสธ?",
            ["∧", "¬", "→", "↔"],
            "¬"
        ),
        (
            "2. p ∧ ¬p เป็นสูตรชนิดใด?",
            ["สัจนิรันดร์", "ข้อขัดแย้ง"],
            "ข้อขัดแย้ง"
        ),
        (
            "3. p → q เป็นเท็จเมื่อใด?",
            ["T,T", "T,F", "F,T", "F,F"],
            "T,F"
        ),
        (
            "4. ∀ อ่านว่าอย่างไร?",
            ["มีอย่างน้อยหนึ่ง", "สำหรับทุก"],
            "สำหรับทุก"
        ),
        (
            "5. Modus Ponens คือรูปแบบใด?",
            [
                "p → q, p ∴ q",
                "p → q, q ∴ p",
                "p ∨ q, p ∴ q"
            ],
            "p → q, p ∴ q"
        )
    ]
    with st.form("quiz_form"):
        answers = []
        for i, (question, options, correct) in enumerate(quiz):
            answer = st.radio(
                question,
                options,
                key=f"quiz_{i}"
            )
            answers.append(answer)
        submitted = st.form_submit_button("ส่งแบบทดสอบ")
    if submitted:
        score = 0
        for i, (question, options, correct) in enumerate(quiz):
            if answers[i] == correct:
                score += 1
                st.success(f"ข้อ {i + 1}: ถูกต้อง")
            else:
                st.error(
                    f"ข้อ {i + 1}: เฉลยคือ {correct}"
                )
        st.metric("คะแนนรวม", f"{score} / {len(quiz)}")
# =========================
# เกี่ยวกับเว็บไซต์
# =========================
elif menu == "ℹ️ เกี่ยวกับเว็บไซต์":
    st.title("ℹ️ เกี่ยวกับเว็บไซต์")
    st.write("""
    Math Logic Learning & Solver
    เป็นเว็บไซต์สื่อการเรียนรู้ตรรกศาสตร์ทางคณิตศาสตร์
    ภายในเว็บไซต์ประกอบด้วย
    - บทเรียนตรรกศาสตร์ 6 บท
    - เครื่องสร้างตารางค่าความจริง
    - เครื่องตรวจสูตรตรรกศาสตร์
    - ตัวอย่างแผนภาพต้นไม้
    - รวมสูตรตรรกศาสตร์
    - แบบฝึกหัด 10 ข้อ เกม และแบบทดสอบ 10ข้อ
    เว็บไซต์นี้จัดทำขึ้นเพื่อใช้ประกอบการเรียนรู้
    และทบทวนเนื้อหาตรรกศาสตร์ทางคณิตศาสตร์
    """)
