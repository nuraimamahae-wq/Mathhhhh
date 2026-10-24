import itertools
import re
import pandas as pd
import streamlit as st

# =========================================================
# 1. ตั้งค่าหน้าเว็บไซต์ & ธีมฟ้าพาสเทล (Pastel Blue Theme, No White Boxes)
# =========================================================
st.set_page_config(
    page_title="Math Logic Learning & Solver",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .block-container {
        max-width: 1250px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    /* เปลี่ยนธีมหลักเป็นสีฟ้าพาสเทล */
    .stApp {
        background-color: #F0F8FF;
        color: #2C3E50;
        font-family: 'Sarabun', sans-serif;
    }

    h1, h2, h3 {
        color: #1A5276;
    }

    [data-testid="stMetric"] {
        background: #E8F4F8;
        padding: 16px;
        border-radius: 14px;
        border: 1px solid #AED6F1;
    }

    .stButton button {
        border-radius: 10px;
        font-weight: 600;
        background-color: #5499C7;
        color: white;
    }
    
    .stButton button:hover {
        background-color: #2980B9;
        color: white;
    }

    /* แถบเมนูด้านซ้ายสีฟ้าพาสเทล */
    [data-testid="stSidebar"] {
        background-color: #EBF5FB !important;
        border-right: 1px solid #AED6F1;
    }

    .main-title-box {
        background: linear-gradient(135deg, #AED6F1 0%, #85C1E9 100%);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        color: #1B4F72;
        box-shadow: 0 4px 15px rgba(133, 193, 233, 0.3);
        margin-bottom: 25px;
    }

    /* เอาพื้นหลังกล่องสีขาวออก ให้กลืนกับธีมฟ้าพาสเทล */
    .content-card {
        background-color: transparent;
        padding: 10px 0px;
        margin-bottom: 20px;
    }

    .solution-box {
        background-color: #E8F8F5;
        border-left: 4px solid #48C9B0;
        padding: 15px;
        border-radius: 8px;
        color: #0E6655;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# 2. ระบบแปลและคำนวณนิพจน์ตรรกศาสตร์
# =========================================================
TOKEN_PATTERN = re.compile(
    r"\s*(<->|<=>|->|=>|[()~!¬∧∨&|^→↔⊕]|[A-Za-z][A-Za-z0-9_]*)"
)

def tokenize(expression):
    expression = expression.strip()
    if not expression:
        raise ValueError("กรุณาป้อนนิพจน์ตรรกศาสตร์")
    tokens = []
    position = 0
    while position < len(expression):
        if expression[position:].strip() == "":
            break
        match = TOKEN_PATTERN.match(expression, position)
        if not match:
            raise ValueError(f"ไม่รู้จักสัญลักษณ์บริเวณ: {expression[position:]}")
        token = match.group(1)
        tokens.append(token)
        position = match.end()

    normalized = []
    for token in tokens:
        if token in ("~", "!", "¬"):
            normalized.append("NOT")
        elif token in ("&", "∧"):
            normalized.append("AND")
        elif token in ("|", "∨"):
            normalized.append("OR")
        elif token in ("->", "=>", "→"):
            normalized.append("IMP")
        elif token in ("<->", "<=>", "↔"):
            normalized.append("IFF")
        elif token == "^":
            normalized.append("XOR")
        else:
            normalized.append(token)
    return normalized

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def peek(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def consume(self):
        token = self.peek()
        if token is not None:
            self.position += 1
        return token

    def parse(self):
        node = self.parse_iff()
        if self.peek() is not None:
            raise ValueError(f"มีสัญลักษณ์ที่ไม่คาดคิด: {self.peek()}")
        return node

    def parse_iff(self):
        node = self.parse_imp()
        while self.peek() == "IFF":
            self.consume()
            right = self.parse_imp()
            node = ("IFF", node, right)
        return node

    def parse_imp(self):
        node = self.parse_or()
        if self.peek() == "IMP":
            self.consume()
            right = self.parse_imp()
            node = ("IMP", node, right)
        return node

    def parse_or(self):
        node = self.parse_and()
        while self.peek() in ("OR", "XOR"):
            operator = self.consume()
            right = self.parse_and()
            node = (operator, node, right)
        return node

    def parse_and(self):
        node = self.parse_unary()
        while self.peek() == "AND":
            self.consume()
            right = self.parse_unary()
            node = ("AND", node, right)
        return node

    def parse_unary(self):
        token = self.peek()
        if token == "NOT":
            self.consume()
            return ("NOT", self.parse_unary())
        if token == "(":
            self.consume()
            node = self.parse_iff()
            if self.peek() != ")":
                raise ValueError("วงเล็บเปิดและวงเล็บปิดไม่ครบ")
            self.consume()
            return node
        if token is None:
            raise ValueError("นิพจน์ไม่สมบูรณ์")
        if token in (")", "AND", "OR", "IMP", "IFF", "XOR"):
            raise ValueError(f"ตำแหน่งนี้ไม่ถูกต้อง: {token}")
        if token.upper() in ("TRUE", "T"):
            self.consume()
            return ("CONST", True)
        if token.upper() in ("FALSE", "F"):
            self.consume()
            return ("CONST", False)
        if re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", token):
            self.consume()
            return ("VAR", token)
        raise ValueError(f"ไม่สามารถอ่านสัญลักษณ์ {token}")

def parse(expression):
    return Parser(tokenize(expression)).parse()

def variables(node):
    found = set()
    def visit(current):
        if current[0] == "VAR":
            found.add(current[1])
        else:
            for child in current[1:]:
                if isinstance(child, tuple):
                    visit(child)
    visit(node)
    return sorted(found)

def evaluate(node, environment):
    kind = node[0]
    if kind == "CONST":
        return node[1]
    if kind == "VAR":
        if node[1] not in environment:
            raise ValueError(f"ไม่มีค่าความจริงของตัวแปร {node[1]}")
        return bool(environment[node[1]])
    if kind == "NOT":
        return not evaluate(node[1], environment)
    left = evaluate(node[1], environment)
    right = evaluate(node[2], environment)
    if kind == "AND":
        return left and right
    if kind == "OR":
        return left or right
    if kind == "XOR":
        return left != right
    if kind == "IMP":
        return (not left) or right
    if kind == "IFF":
        return left == right
    raise ValueError(f"ไม่รู้จักตัวดำเนินการ {kind}")

def pretty(node):
    kind = node[0]
    if kind == "CONST":
        return "T" if node[1] else "F"
    if kind == "VAR":
        return node[1]
    if kind == "NOT":
        return "¬" + pretty(node[1])
    symbols = {"AND": "∧", "OR": "∨", "XOR": "⊕", "IMP": "→", "IFF": "↔"}
    return "(" + pretty(node[1]) + " " + symbols[kind] + " " + pretty(node[2]) + ")"

def truth_table(node):
    vars_list = variables(node)
    if len(vars_list) > 12:
        raise ValueError("นิพจน์มีตัวแปรมากเกินไป กรุณาใช้ไม่เกิน 12 ตัวแปร")
    rows = []
    for values in itertools.product([True, False], repeat=len(vars_list)):
        env = dict(zip(vars_list, values))
        row = {var: "T" if env[var] else "F" for var in vars_list}
        row[pretty(node)] = "T" if evaluate(node, env) else "F"
        rows.append(row)
    return pd.DataFrame(rows)


# =========================================================
# 3. ฐานข้อมูลเนื้อหา สูตร ตัวอย่าง และโจทย์ 10 ข้อครบทุกบท
# =========================================================
COURSE_DATA = {
    "01 บทที่ 1: ประพจน์และการให้เหตุผล": {
        "title": "บทที่ 1: ประพจน์และการให้เหตุผล",
        "content": """
        ### 📖 เนื้อหาบทที่ 1: ประพจน์และการให้เหตุผล
        * **ประพจน์ (Proposition):** ประโยคบอกเล่าหรือปฏิเสธที่มีค่าความจริงเป็นจริง (True) หรือเท็จ (False) อย่างใดอย่างหนึ่งเท่านั้น ประโยคคำถาม คำสั่ง ขอร้อง อุทาน หรือประโยคเปิดจะไม่เป็นประพจน์
        * **ค่าความจริง:** มี 2 ค่า คือ จริง ($\text{T}$) และ เท็จ ($\text{F}$)
        * **ตัวแปรประพจน์:** นิยมใช้ตัวอักษร $p, q, r, s$ แทนประพจน์ย่อย
        """,
        "examples_formulas": """
        ### 💡 สูตรและตัวอย่างประจำบทที่ 1
        * **สูตรนิเสธเบื้องต้น:** $\neg T \equiv F$ และ $\neg F \equiv T$
        * **ตัวอย่างที่ 1.1:** ประโยค "5 เป็นจำนวนคี่" เป็นประพจน์ มีค่าความจริงเป็น **จริง (T)**
        * **ตัวอย่างที่ 1.2:** ประโยค "อย่าส่งเสียงดัง" ไม่เป็นประพจน์ เพราะเป็นประโยคคำสั่ง
        """,
        "exercises": [
            ("1. ประโยค 'กรุงเทพฯ เป็นเมืองหลวง' เป็นประพจน์หรือไม่?", "เป็นประพจน์ มีค่าความจริงเป็น จริง (T)"),
            ("2. ประโยค 'โปรดเงียบเสียง' เป็นประพจน์หรือไม่?", "ไม่เป็นประพจน์ (เป็นประโยคขอร้อง)"),
            ("3. ประโยค 'x + 5 = 10' เป็นประพจน์หรือไม่?", "ไม่เป็นประพจน์ (เป็นประโยคเปิด)"),
            ("4. ถ้า p เป็นจริง จงหาค่าความจริงของ ¬p", "เท็จ (F)"),
            ("5. ประโยค 'เดือนกุมภาพันธ์มี 30 วัน' มีค่าความจริงใด?", "เท็จ (F)"),
            ("6. ถ้า p = จริง และ q = เท็จ จงหาค่าความจริงของ p ∧ q", "เท็จ (F)"),
            ("7. Modus Ponens มีโครงสร้างอย่างไร?", "[(p → q) ∧ p] ⊢ q"),
            ("8. ประโยค 'ยินดีต้อนรับ' เป็นประพจน์หรือไม่?", "ไม่เป็นประพจน์"),
            ("9. ค่าความจริงของ 5 > 3 คืออะไร?", "จริง (T)"),
            ("10. กำหนด p แทน 'ไฟดับ' เขียนสัญลักษณ์ 'ไฟไม่ดับ'", "¬p")
        ]
    },
    "02 บทที่ 2: ตัวเชื่อมและตารางค่าความจริง": {
        "title": "บทที่ 2: ตัวเชื่อมและตารางค่าความจริง",
        "content": """
        ### 📖 เนื้อหาบทที่ 2: ตัวเชื่อมและตารางค่าความจริง
        * **ตัวเชื่อมพื้นฐาน:** นิเสธ ($\neg$), และ ($\wedge$), หรือ ($\vee$), ถ้า...แล้ว ($\rightarrow$), ก็ต่อเมื่อ ($\leftrightarrow$)
        * **ตารางค่าความจริง:** จำนวนแถวทั้งหมดคำนวณจาก $2^n$ เมื่อ $n$ คือจำนวนตัวแปรประพจน์
        """,
        "examples_formulas": """
        ### 💡 สูตรและตัวอย่างประจำบทที่ 2
        * **กฎเดอมอร์แกน (De Morgan's Laws):** 
          $\neg(p \wedge q) \equiv \neg p \vee \neg q$
          $\neg(p \vee q) \equiv \neg p \wedge \neg q$
        * **ตัวอย่างที่ 2.1:** $T \wedge F \equiv F$ และ $T \vee F \equiv T$
        """,
        "exercises": [
            ("1. จงหาค่าความจริงของ T ∧ F", "เท็จ (F)"),
            ("2. จงหาค่าความจริงของ F ∨ T", "จริง (T)"),
            ("3. ถ้า p เป็นเท็จ และ q เป็นจริง p → q คือ?", "จริง (T)"),
            ("4. ถ้า p และ q ค่าความจริงต่างกัน p ↔ q คือ?", "เท็จ (F)"),
            ("5. นิเสธของ p ∧ q ตามเดอมอร์แกนคือ?", "¬p ∨ ¬q"),
            ("6. ตัวแปร 3 ตัว ตารางค่าความจริงมีกี่แถว?", "8 แถว (2³ = 8)"),
            ("7. ค่าความจริงของ ¬T ∨ F คือ?", "เท็จ (F)"),
            ("8. p → q สมมูลกับประพจน์ใดในรูปตัวเชื่อม หรือ (∨)?", "¬p ∨ q"),
            ("9. ถ้า p ↔ q เป็นจริง สรุป p และ q ได้อย่างไร?", "มีค่าความจริงเหมือนกัน"),
            ("10. หานิเสธของ ¬p ∨ q", "p ∧ ¬q")
        ]
    },
    "03 บทที่ 3: สัจนิรันดร์และข้อขัดแย้ง": {
        "title": "บทที่ 3: สัจนิรันดร์และข้อขัดแย้ง",
        "content": """
        ### 📖 เนื้อหาบทที่ 3: สัจนิรันดร์และข้อขัดแย้ง
        * **สัจนิรันดร์ (Tautology):** ประพจน์ที่เป็นจริงทุกกรณี ($\text{T}$)
        * **ข้อขัดแย้ง (Contradiction):** ประพจน์ที่เป็นเท็จทุกกรณี ($\text{F}$)
        * **คอนทินเจนซี:** ประพจน์ที่มีค่าความจริงทั้งจริงและเท็จคละกัน
        """,
        "examples_formulas": """
        ### 💡 สูตรและตัวอย่างประจำบทที่ 3
        * **สูตรมาตรฐาน:** $p \vee \neg p \equiv T$ (สัจนิรันดร์) และ $p \wedge \neg p \equiv F$ (ข้อขัดแย้ง)
        * **วิธีตรวจสอบทางอ้อม:** สมมติให้ประพจน์หลักเป็นเท็จ ($F$) แล้วใช้กฎตัวเชื่อมไล่ย้อนกลับ หากเกิดข้อขัดแย้งแสดงว่าเป็นสัจนิรันดร์
        """,
        "exercises": [
            ("1. p ∨ ¬p เป็นสูตรประเภทใด?", "สัจนิรันดร์"),
            ("2. p ∧ ¬p เป็นสูตรประเภทใด?", "ข้อขัดแย้ง"),
            ("3. วิธีตรวจสอบสัจนิรันดร์ทางอ้อม สมมติให้ประพจน์เป็นอะไร?", "เท็จ (F)"),
            ("4. ถ้าสมมติแล้วเกิดข้อขัดแย้ง สรุปได้ว่า?", "เป็นสัจนิรันดร์"),
            ("5. (p ∧ q) → p เป็นสัจนิรันดร์หรือไม่?", "เป็นสัจนิรันดร์"),
            ("6. ประพจน์ที่มีทั้งจริงและเท็จปะปนกันเรียกว่า?", "คอนทินเจนซี (Contingency)"),
            ("7. p → (p ∨ q) เป็นสัจนิรันดร์หรือไม่?", "เป็นสัจนิรันดร์"),
            ("8. (p → q) ∧ p → q เป็นสัจนิรันดร์หรือไม่?", "เป็นสัจนิรันดร์"),
            ("9. ตรวจสอบสมมูลของ A และ B ใช้ตัวเชื่อมใดเชื่อม?", "ก็ต่อเมื่อ (↔)"),
            ("10. p ↔ ¬p เป็นสัจนิรันดร์หรือข้อขัดแย้ง?", "ข้อขัดแย้ง")
        ]
    },
    "04 บทที่ 4: การอ้างเหตุผล": {
        "title": "บทที่ 4: การอ้างเหตุผล",
        "content": """
        ### 📖 เนื้อหาบทที่ 4: การอ้างเหตุผล
        * ประกอบด้วยส่วนสำคัญ 2 ส่วน คือ เหตุ ($P_1, P_2, \dots$) และ ข้อสรุป ($C$)
        * **ความสมเหตุสมผล (Valid):** เมื่อเหตุทุกข้อเป็นจริงแล้ว ข้อสรุปต้องเป็นจริงตามเสมอ
        """,
        "examples_formulas": """
        ### 💡 สูตรและตัวอย่างประจำบทที่ 4
        * **Modus Ponens:** $[(p \rightarrow q) \wedge p] \vdash q$
        * **Modus Tollens:** $[(p \rightarrow q) \wedge \neg q] \vdash \neg p$
        * **Hypothetical Syllogism:** $[(p \rightarrow q) \wedge (q \rightarrow r)] \vdash (p \rightarrow r)$
        """,
        "exercises": [
            ("1. การอ้างเหตุผลประกอบด้วยส่วนใดบ้าง?", "เหตุ และ ข้อสรุป"),
            ("2. การอ้างเหตุผลจะสมเหตุสมผลเมื่อใด?", "เหตุจริงทั้งหมดแล้วข้อสรุปต้องจริง"),
            ("3. p → q, p ∴ q เรียกว่ากฎอะไร?", "Modus Ponens"),
            ("4. p → q, ¬q ∴ ¬p เรียกว่ากฎอะไร?", "Modus Tollens"),
            ("5. p → q, q → r สรุปผลคือ?", "p → r"),
            ("6. p ∨ q, ¬p สรุปผลคือ?", "q"),
            ("7. หากมีแถวที่เหตุจริงแต่ผลเท็จ การอ้างเหตุผลจะ?", "ไม่สมเหตุสมผล"),
            ("8. กฎการเพิ่ม (Addition) จาก p สรุปเป็น?", "p ∨ q"),
            ("9. กฎการตัดทอนจาก p ∧ q สรุปเป็น?", "p"),
            ("10. รูปแบบประพจน์รวมของการอ้างเหตุผลที่สมเหตุสมผลต้องเป็น?", "สัจนิรันดร์")
        ]
    },
    "05 บทที่ 5: ประโยคเปิดและตัวบ่งปริมาณ": {
        "title": "บทที่ 5: ประโยคเปิดและตัวบ่งปริมาณ",
        "content": """
        ### 📖 เนื้อหาบทที่ 5: ประโยคเปิดและตัวบ่งปริมาณ
        * **ประโยคเปิด:** ประโยคที่มีตัวแปรและจะกลายเป็นประพจน์เมื่อแทนค่าตัวแปรด้วยสมาชิกในเอกภพสัมพัทธ์ ($\mathcal{U}$)
        * **ตัวบ่งปริมาณ:** สัญลักษณ์สากล ($\forall$) และสัญลักษณ์มีอยู่จริง ($\exists$)
        """,
        "examples_formulas": """
        ### 💡 สูตรและตัวอย่างประจำบทที่ 5
        * **สูตรนิเสธตัวบ่งปริมาณ:** 
          $\neg(\forall x P(x)) \equiv \exists x \neg P(x)$
          $\neg(\exists x P(x)) \equiv \forall x \neg P(x)$
        """,
        "exercises": [
            ("1. x + 2 = 7 เมื่อมีตัวแปรเรียกว่า?", "ประโยคเปิด"),
            ("2. สัญลักษณ์ ∀ หมายถึง?", "สำหรับทุกตัว"),
            ("3. สัญลักษณ์ ∃ หมายถึง?", "มีอย่างน้อยหนึ่งตัว"),
            ("4. นิเสธของ ∀x P(x) คือ?", "∃x ¬P(x)"),
            ("5. นิเสธของ ∃x P(x) คือ?", "∀x ¬P(x)"),
            ("6. U = {1, 2, 3} ค่าความจริงของ ∀x(x > 0) คือ?", "จริง (T)"),
            ("7. U = R ค่าความจริงของ ∃x(x² = 4) คือ?", "จริง (T)"),
            ("8. นิเสธของ ∀x[x > 5] คือ?", "∃x[x ≤ 5]"),
            ("9. นิเสธของ ∃x[x² ≠ 9] คือ?", "∀x[x² = 9]"),
            ("10. ถ้า ∀x P(x) เป็นเท็จ ข้อความใดรับประกันว่าเป็นจริง?", "∃x ¬P(x)")
        ]
    },
    "06 บทที่ 6: การอุปนัยและนิรนัย": {
        "title": "บทที่ 6: การอุปนัยและนิรนัย",
        "content": """
        ### 📖 เนื้อหาบทที่ 6: การอุปนัยและนิรนัย
        * **นิรนัย:** การให้เหตุผลจากหลักการทั่วไปไปสู่ข้อสรุปเฉพาะ
        * **อุปนัย:** การให้เหตุผลจากการสังเกตกรณีเฉพาะหลายๆ ครั้งมาเป็นข้อสรุปทั่วไป
        """,
        "examples_formulas": """
        ### 💡 สูตรและตัวอย่างประจำบทที่ 6
        * **สูตรอนุกรมสำคัญ:**
          $\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$
          $\sum_{i=1}^{n} i^3 = \left[\frac{n(n+1)}{2}\right]^2$
        * **การอุปนัยเชิงคณิตศาสตร์:** พิสูจน์ที่ $n=1$ และสมมติจริงที่ $n=k$ แล้วพิสูจน์ต่อที่ $n=k+1$
        """,
        "exercises": [
            ("1. การสรุปจากกฎทั่วไปสู่ข้อสรุปเฉพาะคือ?", "นิรนัย"),
            ("2. การสรุปจากตัวย่อยสู่กฎทั่วไปคือ?", "อุปนัย"),
            ("3. อุปนัยเชิงคณิตศาสตร์ขั้นแรกต้องพิสูจน์ที่ใด?", "n = 1"),
            ("4. ขั้นที่สองของการอุปนัยเชิงคณิตศาสตร์สมมติที่?", "n = k"),
            ("5. ผลบวก 1+2+...+10 เท่ากับเท่าใด?", "55"),
            ("6. สูตรผลบวกกำลังสอง n พจน์แรกคือ?", "n(n+1)(2n+1)/6"),
            ("7. สูตรผลบวกกำลังสาม n พจน์แรกคือ?", "[n(n+1)/2]²"),
            ("8. วิธีพิสูจน์สำหรับจำนวนนับ n ทุกตัวคือ?", "อุปนัยเชิงคณิตศาสตร์"),
            ("9. ข้อสรุปแบบอุปนัยมีความแน่นอน 100% หรือไม่?", "ไม่แน่นอน 100%"),
            ("10. ผลบวกกำลังสามของ 1 + 2 + 3 คือ?", "36")
        ]
    }
}


# =========================================================
# 4. เมนูด้านข้าง (Sidebar Navigation Structure)
# =========================================================
st.sidebar.title("📘 Math Logic")
st.sidebar.caption("สื่อการเรียนรู้ตรรกศาสตร์เชิงคณิตศาสตร์")

menu_options = ["🏠 หน้าแรก / สรุปภาพรวม"]

for ch_key in COURSE_DATA.keys():
    menu_options.append(f"📚 {ch_key} (เนื้อหา)")
    menu_options.append(f"💡 {ch_key} (สูตรและตัวอย่าง)")
    menu_options.append(f"📝 {ch_key} (โจทย์ 10 ข้อพร้อมเฉลย)")

menu_options.append("📖 รวมสูตรตรรกศาสตร์ทุกบท")
menu_options.append("⚡ เครื่องมือคำนวณตรรกศาสตร์อัตโนมัติ")

selected_menu = st.sidebar.radio("เลือกหัวข้อบทเรียน:", menu_options, label_visibility="collapsed")


# =========================================================
# 5. ระบบแสดงผลเนื้อหาตามเมนูที่เลือก
# =========================================================
st.markdown("""
<div class="main-title-box">
    <div style="font-size: 26px; font-weight: 800; margin: 0;">✨ สื่อการเรียนรู้วิชาตรรกศาสตร์เชิงคณิตศาสตร์ ✨</div>
</div>
""", unsafe_allow_html=True)

# --- หน้าแรก ---
if "🏠 หน้าแรก" in selected_menu:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 📘 ยินดีต้อนรับสู่แอปพลิเคชันเรียนรู้ตรรกศาสตร์")
    st.write("เลือกบทเรียน เมนูย่อย เนื้อหา สูตร ตัวอย่าง หรือโจทย์ 10 ข้อพร้อมเฉลยจากแถบเมนูด้านซ้ายเพื่อเริ่มต้นใช้งานได้ทันทีครับ")
    st.markdown("""
    * **บทที่ 1:** ประพจน์และการให้เหตุผล
    * **บทที่ 2:** ตัวเชื่อมและตารางค่าความจริง
    * **บทที่ 3:** สัจนิรันดร์และข้อขัดแย้ง
    * **บทที่ 4:** การอ้างเหตุผล
    * **บทที่ 5:** ประโยคเปิดและตัวบ่งปริมาณ
    * **บทที่ 6:** การอุปนัยและนิรนัย
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# --- เมนูย่อยเนื้อหาบทที่ 1-6 ---
elif "(เนื้อหา)" in selected_menu:
    for ch_key, data in COURSE_DATA.items():
        if ch_key in selected_menu:
            st.markdown(f'<div class="content-card">', unsafe_allow_html=True)
            st.markdown(f"<h2>📚 {data['title']}</h2>", unsafe_allow_html=True)
            st.markdown(data["content"], unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# --- เมนูย่อยสูตรและตัวอย่างบทที่ 1-6 ---
elif "(สูตรและตัวอย่าง)" in selected_menu:
    for ch_key, data in COURSE_DATA.items():
        if ch_key in selected_menu:
            st.markdown(f'<div class="content-card">', unsafe_allow_html=True)
            st.markdown(f"<h2>💡 สูตรและตัวอย่าง: {data['title']}</h2>", unsafe_allow_html=True)
            st.markdown(data["examples_formulas"], unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# --- เมนูย่อยโจทย์ 10 ข้อพร้อมเฉลยบทที่ 1-6 ---
elif "(โจทย์ 10 ข้อพร้อมเฉลย)" in selected_menu:
    for ch_key, data in COURSE_DATA.items():
        if ch_key in selected_menu:
            st.markdown(f'<div class="content-card">', unsafe_allow_html=True)
            st.markdown(f"<h2>📝 แบบฝึกหัด 10 ข้อพร้อมเฉลย: {data['title']}</h2>", unsafe_allow_html=True)
            for q, a in data["exercises"]:
                st.markdown(f"**{q}**")
                with st.expander("👉 คลิกดูเฉลยคำตอบ"):
                    st.markdown(f'<div class="solution-box"><b>เฉลย:</b> {a}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# --- รวมสูตรตรรกศาสตร์ทุกบท ---
elif "📖 รวมสูตรตรรกศาสตร์ทุกบท" in selected_menu:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 📖 รวมสูตรและกฎสำคัญทางตรรกศาสตร์ทุกบทฉบับสมบูรณ์")
    
    st.markdown("1. **สมมูลที่สำคัญ:**")
    st.latex(r"p \rightarrow q \equiv \neg p \vee q")
    st.latex(r"\neg(p \rightarrow q) \equiv p \wedge \neg q")
    st.latex(r"p \leftrightarrow q \equiv (p \rightarrow q) \wedge (q \rightarrow p)")

    st.markdown("2. **กฎเดอมอร์แกน (De Morgan's Laws):**")
    st.latex(r"\neg(p \wedge q) \equiv \neg p \vee \neg q")
    st.latex(r"\neg(p \vee q) \equiv \neg p \wedge \neg q")

    st.markdown("3. **นิเสธของตัวบ่งปริมาณ:**")
    st.latex(r"\neg(\forall x P(x)) \equiv \exists x \neg P(x)")
    st.latex(r"\neg(\exists x P(x)) \equiv \forall x \neg P(x)")

    st.markdown("4. **อนุกรมและอุปนัยเชิงคณิตศาสตร์:**")
    st.latex(r"\sum_{i=1}^{n} i = \frac{n(n+1)}{2}")
    st.latex(r"\sum_{i=1}^{n} i^2 = \frac{n(n+1)(2n+1)}{6}")
    st.latex(r"\sum_{i=1}^{n} i^3 = \left[\frac{n(n+1)}{2}\right]^2")
    st.markdown('</div>', unsafe_allow_html=True)

# --- เครื่องมือคำนวณตรรกศาสตร์อัตโนมัติ ---
elif "⚡ เครื่องมือคำนวณตรรกศาสตร์อัตโนมัติ" in selected_menu:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### ⚡ เครื่องมือตรวจสอบตรรกศาสตร์และตารางค่าความจริงอัตโนมัติ")
    user_expr = st.text_input("ป้อนประพจน์ (ใช้ & แทนและ, | แทนหรือ, ~ แทนนิเสธ, >> แทนถ้า...แล้ว):", value="(p & q) >> p")
    if st.button("🚀 สร้างตารางค่าความจริง"):
        try:
            node = parse(user_expr)
            df = truth_table(node)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.success("✅ สร้างตารางค่าความจริงสำเร็จเรียบร้อยครับ")
        except Exception as e:
            st.error(f"รูปแบบประพจน์ไม่ถูกต้อง: {e}")
    st.markdown('</div>', unsafe_allow_html=True)
