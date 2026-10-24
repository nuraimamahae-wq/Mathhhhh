import itertools
import random
import re

import pandas as pd
import streamlit as st


# =========================================================
# 1. ตั้งค่าหน้าเว็บไซต์ (Modern Minimal Pink Theme)
# =========================================================

st.set_page_config(
    page_title="Math Logic Learning & Solver",
    page_icon="🧠",
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

    h1, h2, h3 {
        color: #433878;
    }

    [data-testid="stMetric"] {
        background: #f1efff;
        padding: 16px;
        border-radius: 14px;
    }

    .stButton button {
        border-radius: 10px;
        font-weight: 600;
    }

    [data-testid="stSidebar"] {
        background-color: #f7f5ff;
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
    """แปลงนิพจน์ให้เป็นรายการสัญลักษณ์"""

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
            raise ValueError(
                f"ไม่รู้จักสัญลักษณ์บริเวณ: {expression[position:]}"
            )

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
    """
    ลำดับความสำคัญ:
    1. NOT
    2. AND
    3. OR / XOR
    4. IMPLICATION
    5. BICONDITIONAL
    """

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
            raise ValueError(
                f"มีสัญลักษณ์ที่ไม่คาดคิด: {self.peek()}"
            )

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
    """รวบรวมตัวแปรโดยไม่ซ้ำกัน"""

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
    """คำนวณค่าความจริงของนิพจน์"""

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
    """แสดงนิพจน์ให้อ่านง่าย"""

    kind = node[0]

    if kind == "CONST":
        return "T" if node[1] else "F"

    if kind == "VAR":
        return node[1]

    if kind == "NOT":
        return "¬" + pretty(node[1])

    symbols = {
        "AND": "∧",
        "OR": "∨",
        "XOR": "⊕",
        "IMP": "→",
        "IFF": "↔",
    }

    return (
        "("
        + pretty(node[1])
        + " "
        + symbols[kind]
        + " "
        + pretty(node[2])
        + ")"
    )


def truth_table(node):
    """สร้างตารางค่าความจริง"""

    vars_list = variables(node)

    if len(vars_list) > 12:
        raise ValueError(
            "นิพจน์มีตัวแปรมากเกินไป กรุณาใช้ไม่เกิน 12 ตัวแปร"
        )

    rows = []

    for values in itertools.product([True, False], repeat=len(vars_list)):
        env = dict(zip(vars_list, values))

        row = {
            var: "T" if env[var] else "F"
            for var in vars_list
        }

        row[pretty(node)] = (
            "T" if evaluate(node, env) else "F"
        )

        rows.append(row)

    return pd.DataFrame(rows)


def classify(node):
    """จำแนกประเภทของสูตร"""

    results = []

    for values in itertools.product(
        [True, False], repeat=len(variables(node))
    ):
        env = dict(zip(variables(node), values))
        results.append(evaluate(node, env))

    if all(results):
        return "สัจนิรันดร์ (Tautology)"

    if not any(results):
        return "ข้อขัดแย้ง (Contradiction)"

    return "กรณีอื่นหรือประพจน์ไม่แน่นอน (Contingency)"


def equivalence(left, right):
    """ตรวจสอบว่าสูตรสองสูตรสมมูลกันหรือไม่"""

    all_vars = sorted(set(variables(left)) | set(variables(right)))

    if len(all_vars) > 12:
        raise ValueError("ใช้ตัวแปรรวมกันไม่เกิน 12 ตัว")

    for values in itertools.product([True, False], repeat=len(all_vars)):
        env = dict(zip(all_vars, values))

        left_result = evaluate(left, env)
        right_result = evaluate(right, env)

        if left_result != right_result:
            return False, env

    return True, None


def check_argument(premises, conclusion):
    """
    ตรวจความสมเหตุสมผล:
    เหตุทุกข้อจริง แต่ข้อสรุปเท็จหรือไม่
    """

    all_vars = set(variables(conclusion))

    for premise in premises:
        all_vars.update(variables(premise))

    all_vars = sorted(all_vars)

    if len(all_vars) > 12:
        raise ValueError("ใช้ตัวแปรรวมกันไม่เกิน 12 ตัว")

    for values in itertools.product([True, False], repeat=len(all_vars)):
        env = dict(zip(all_vars, values))

        all_premises_true = all(
            evaluate(premise, env) for premise in premises
        )

        conclusion_false = not evaluate(conclusion, env)

        if all_premises_true and conclusion_false:
            return False, env

    return True, None


# =========================================================
# 3. เนื้อหาบทเรียนและหัวข้อย่อย
# =========================================================

LESSONS = {
    "บทที่ 1 ความรู้เบื้องต้นเกี่ยวกับตรรกศาสตร์": [
        (
            "ความหมายของตรรกศาสตร์",
            "ตรรกศาสตร์เป็นศาสตร์ที่ศึกษาหลักการให้เหตุผล "
            "การตรวจสอบข้ออ้าง และความสัมพันธ์ระหว่างเหตุและผล",
            "ถ้า p แทนประโยคว่า วันนี้ฝนตก "
            "และ q แทนประโยคว่า ถนนเปียก "
            "สามารถศึกษาความสัมพันธ์ของ p และ q ได้"
        ),
        (
            "ประพจน์",
            "ประพจน์คือประโยคบอกเล่าที่สามารถระบุค่าความจริงได้ว่าเป็นจริงหรือเท็จ",
            "2 + 3 = 5 เป็นประพจน์จริง ส่วน 2 + 3 = 6 เป็นประพจน์เท็จ"
        ),
        (
            "ค่าความจริง",
            "ค่าความจริงมีสองค่า ได้แก่ จริง (True หรือ T) และเท็จ (False หรือ F)",
            "p = T หมายถึงประพจน์ p เป็นจริง"
        ),
        (
            "ตัวแปรประพจน์",
            "นิยมใช้ตัวอักษร p, q, r แทนประพจน์ต่าง ๆ",
            "ให้ p แทนประโยคว่า 5 เป็นจำนวนคี่ ดังนั้น p มีค่าความจริงเป็น T"
        ),
    ],

    "บทที่ 2 ตัวเชื่อมตรรกศาสตร์": [
        (
            "นิเสธ",
            "นิเสธของ p เขียนเป็น ¬p มีค่าความจริงตรงข้ามกับ p",
            "ถ้า p เป็นจริง แล้ว ¬p เป็นเท็จ"
        ),
        (
            "การเชื่อมแบบและ",
            "p ∧ q เป็นจริงเมื่อ p และ q เป็นจริงทั้งคู่เท่านั้น",
            "T ∧ T = T แต่ T ∧ F = F"
        ),
        (
            "การเชื่อมแบบหรือ",
            "p ∨ q เป็นจริงเมื่อมีอย่างน้อยหนึ่งประพจน์เป็นจริง",
            "T ∨ F = T และ F ∨ F = F"
        ),
        (
            "อิมพลิเคชัน",
            "p → q เป็นเท็จเพียงกรณีเดียว คือ p เป็นจริงและ q เป็นเท็จ",
            "T → F = F ส่วน F → T = T"
        ),
        (
            "สมมูลสองทาง",
            "p ↔ q เป็นจริงเมื่อ p และ q มีค่าความจริงเหมือนกัน",
            "T ↔ T = T และ T ↔ F = F"
        ),
        (
            "ตารางค่าความจริงเบื้องต้น",
            "ตารางค่าความจริงใช้แสดงผลของตัวเชื่อมทุกกรณีที่เป็นไปได้",
            "ตัวแปร 2 ตัวมีกรณีค่าความจริงทั้งหมด 2² = 4 กรณี"
        ),
    ],

    "บทที่ 3 สัจนิรันดร์และสมมูล": [
        (
            "สัจนิรันดร์",
            "สูตรที่เป็นจริงทุกกรณีของค่าความจริง เรียกว่าสัจนิรันดร์",
            "p ∨ ¬p เป็นสัจนิรันดร์"
        ),
        (
            "ข้อขัดแย้ง",
            "สูตรที่เป็นเท็จทุกกรณี เรียกว่าข้อขัดแย้ง",
            "p ∧ ¬p เป็นข้อขัดแย้ง"
        ),
        (
            "กรณีอื่น",
            "สูตรที่มีทั้งกรณีจริงและกรณีเท็จ เรียกว่า contingency",
            "p ∧ q มีทั้งกรณีจริงและกรณีเท็จ"
        ),
        (
            "สมมูลทางตรรกศาสตร์",
            "สูตรสองสูตรสมมูลกันเมื่อมีค่าความจริงตรงกันทุกกรณี",
            "p → q สมมูลกับ ¬p ∨ q"
        ),
        (
            "กฎของเดอมอร์แกน",
            "กฎของเดอมอร์แกนใช้เปลี่ยนนิเสธของนิพจน์ที่มีตัวเชื่อมและหรือ",
            "¬(p ∧ q) สมมูลกับ ¬p ∨ ¬q"
        ),
    ],

    "บทที่ 4 การอ้างเหตุผล": [
        (
            "ความหมายของการอ้างเหตุผล",
            "การอ้างเหตุผลประกอบด้วยเหตุหรือข้ออ้าง และข้อสรุป",
            "เหตุ: ถ้า p แล้ว q และ p เป็นจริง ข้อสรุปคือ q"
        ),
        (
            "Modus Ponens",
            "รูปแบบ: p → q, p ดังนั้น q",
            "ถ้าฝนตก ถนนเปียก; ฝนตก; ดังนั้นถนนเปียก"
        ),
        (
            "Modus Tollens",
            "รูปแบบ: p → q, ¬q ดังนั้น ¬p",
            "ถ้าฝนตก ถนนเปียก; ถนนไม่เปียก; ดังนั้นฝนไม่ตก"
        ),
        (
            "การตรวจความสมเหตุสมผล",
            "การอ้างเหตุผลสมเหตุสมผลเมื่อไม่มีกรณีที่เหตุทุกข้อจริงแต่ข้อสรุปเท็จ",
            "สามารถตรวจได้ด้วยตารางค่าความจริง"
        ),
    ],

    "บทที่ 5 ประโยคเปิดและตัวบ่งปริมาณ": [
        (
            "ประโยคเปิด",
            "ประโยคเปิดมีตัวแปรและยังไม่สามารถกำหนดค่าความจริงได้แน่นอนจนกว่าจะกำหนดค่าตัวแปร",
            "x + 2 = 5 จะเป็นจริงเมื่อ x = 3"
        ),
        (
            "ตัวบ่งปริมาณสากล",
            "สัญลักษณ์ ∀ หมายถึง สำหรับทุกตัวหรือทุกสมาชิกในขอบเขตที่กำหนด",
            "∀x P(x) หมายถึง P(x) เป็นจริงสำหรับทุก x ในขอบเขตนั้น"
        ),
        (
            "ตัวบ่งปริมาณมีอยู่",
            "สัญลักษณ์ ∃ หมายถึง มีอย่างน้อยหนึ่งตัวที่ทำให้ข้อความเป็นจริง",
            "∃x P(x) หมายถึง มี x อย่างน้อยหนึ่งค่าที่ทำให้ P(x) เป็นจริง"
        ),
        (
            "นิเสธของตัวบ่งปริมาณ",
            "การปฏิเสธข้อความที่มีตัวบ่งปริมาณต้องเปลี่ยนชนิดของตัวบ่งปริมาณ",
            "¬(∀x P(x)) สมมูลกับ ∃x ¬P(x)"
        ),
    ],

    "บทที่ 6 การให้เหตุผลและการพิสูจน์": [
        (
            "การให้เหตุผลแบบนิรนัย",
            "การให้เหตุผลจากหลักทั่วไปไปสู่ข้อสรุปเฉพาะ",
            "มนุษย์ทุกคนต้องการน้ำ; ก เป็นมนุษย์; ดังนั้น ก ต้องการน้ำ"
        ),
        (
            "การให้เหตุผลแบบอุปนัย",
            "การให้เหตุผลจากการสังเกตหลายกรณีเพื่อคาดการณ์ข้อสรุปทั่วไป",
            "สังเกตหลายครั้งแล้วพบรูปแบบเดียวกัน จึงคาดการณ์ว่ารูปแบบนั้นอาจเกิดขึ้นทั่วไป"
        ),
        (
            "การพิสูจน์ทางคณิตศาสตร์",
            "การพิสูจน์ต้องใช้ข้อกำหนด นิยาม และเหตุผลที่ถูกต้องเพื่อสนับสนุนข้อสรุป",
            "เริ่มจากสมมติฐาน แล้วแสดงขั้นตอนที่นำไปสู่ข้อสรุป"
        ),
    ],
}


FORMULAS = {
    "1. ตัวเชื่อมตรรกศาสตร์": [
        "¬p : นิเสธของ p",
        "p ∧ q : p และ q",
        "p ∨ q : p หรือ q",
        "p → q : ถ้า p แล้ว q",
        "p ↔ q : p ก็ต่อเมื่อ q",
    ],

    "2. อิมพลิเคชันและสมมูล": [
        "p → q ≡ ¬p ∨ q",
        "p → q ≡ ¬q → ¬p",
        "p ↔ q ≡ (p → q) ∧ (q → p)",
        "p ↔ q ≡ (p ∧ q) ∨ (¬p ∧ ¬q)",
    ],

    "3. กฎของเดอมอร์แกน": [
        "¬(p ∧ q) ≡ ¬p ∨ ¬q",
        "¬(p ∨ q) ≡ ¬p ∧ ¬q",
    ],

    "4. กฎเอกลักษณ์และการครอบงำ": [
        "p ∧ T ≡ p",
        "p ∨ F ≡ p",
        "p ∨ T ≡ T",
        "p ∧ F ≡ F",
    ],

    "5. กฎนิเสธซ้อนและกฎไอดอมโพเทนต์": [
        "¬(¬p) ≡ p",
        "p ∧ p ≡ p",
        "p ∨ p ≡ p",
    ],

    "6. กฎการสลับที่และการเปลี่ยนหมู่": [
        "p ∧ q ≡ q ∧ p",
        "p ∨ q ≡ q ∨ p",
        "(p ∧ q) ∧ r ≡ p ∧ (q ∧ r)",
        "(p ∨ q) ∨ r ≡ p ∨ (q ∨ r)",
    ],

    "7. กฎการแจกแจง": [
        "p ∧ (q ∨ r) ≡ (p ∧ q) ∨ (p ∧ r)",
        "p ∨ (q ∧ r) ≡ (p ∨ q) ∧ (p ∨ r)",
    ],

    "8. การอ้างเหตุผล": [
        "Modus Ponens: p → q, p ∴ q",
        "Modus Tollens: p → q, ¬q ∴ ¬p",
        "Hypothetical Syllogism: p → q, q → r ∴ p → r",
        "Disjunctive Syllogism: p ∨ q, ¬p ∴ q",
    ],

    "9. ตัวบ่งปริมาณ": [
        "¬(∀x P(x)) ≡ ∃x ¬P(x)",
        "¬(∃x P(x)) ≡ ∀x ¬P(x)",
    ],
}


QUESTIONS = [
    {
        "question": "ถ้า p เป็นจริง แล้ว ¬p มีค่าเป็นอะไร?",
        "options": ["จริง (T)", "เท็จ (F)"],
        "answer": "เท็จ (F)",
        "explanation": "นิเสธจะมีค่าความจริงตรงข้ามกับประพจน์เดิม",
    },
    {
        "question": "T ∧ F มีค่าเป็นอะไร?",
        "options": ["จริง (T)", "เท็จ (F)"],
        "answer": "เท็จ (F)",
        "explanation": "การเชื่อมแบบและต้องจริงทั้งสองข้างจึงจะเป็นจริง",
    },
    {
        "question": "T ∨ F มีค่าเป็นอะไร?",
        "options": ["จริง (T)", "เท็จ (F)"],
        "answer": "จริง (T)",
        "explanation": "การเชื่อมแบบหรือเป็นจริงเมื่อมีอย่างน้อยหนึ่งข้างจริง",
    },
    {
        "question": "p ∨ ¬p เป็นสูตรประเภทใด?",
        "options": [
            "สัจนิรันดร์",
            "ข้อขัดแย้ง",
            "กรณีอื่น",
        ],
        "answer": "สัจนิรันดร์",
        "explanation": "p และ ¬p ต้องมีค่าตรงข้ามกัน จึงมีอย่างน้อยหนึ่งข้างจริงเสมอ",
    },
    {
        "question": "p ∧ ¬p เป็นสูตรประเภทใด?",
        "options": [
            "สัจนิรันดร์",
            "ข้อขัดแย้ง",
            "กรณีอื่น",
        ],
        "answer": "ข้อขัดแย้ง",
        "explanation": "p และ ¬p ไม่สามารถเป็นจริงพร้อมกันได้",
    },
    {
        "question": "p → q จะเป็นเท็จในกรณีใด?",
        "options": [
            "p จริง และ q จริง",
            "p จริง และ q เท็จ",
            "p เท็จ และ q จริง",
            "p เท็จ และ q เท็จ",
        ],
        "answer": "p จริง และ q เท็จ",
        "explanation": "อิมพลิเคชันเป็นเท็จเฉพาะกรณี T → F",
    },
]


# =========================================================
# 4. สร้างเมนูด้านซ้าย พร้อมหัวข้อย่อยทุกหัวข้อ
# =========================================================

HOME = "🏠 หน้าแรก"
CALCULATOR = "🧮 เครื่องคำนวณตรรกศาสตร์"
TREE = "🌳 แผนภาพต้นไม้"
FORMULA = "📖 รวมสูตรตรรกศาสตร์"
PRACTICE = "📝 แบบฝึกหัด"
GAME = "🎮 เกมตรรกศาสตร์"
QUIZ = "📊 แบบทดสอบ"
ABOUT = "ℹ️ เกี่ยวกับเว็บไซต์"

MAIN_MENU = [
    HOME,
    CALCULATOR,
    TREE,
    FORMULA,
    PRACTICE,
    GAME,
    QUIZ,
    ABOUT,
]

lesson_routes = {}
chapter_routes = {}

for chapter, topics in LESSONS.items():
    chapter_routes[chapter] = chapter

    for title, description, example in topics:
        label = f" ↳ {title}"
        lesson_routes[label] = (
            chapter,
            title,
            description,
            example,
        )

st.sidebar.title("🧠 Math Logic")
st.sidebar.caption("Learning • Practice • Solver")

st.sidebar.markdown("---")
st.sidebar.subheader("เมนูหลัก")

selected_main = st.sidebar.radio(
    "เมนูหลัก",
    MAIN_MENU,
    label_visibility="collapsed",
    key="selected_main",
)

st.sidebar.markdown("---")
st.sidebar.subheader("📚 บทเรียน")

lesson_options = []

for chapter, topics in LESSONS.items():
    lesson_options.append(chapter)

    for title, description, example in topics:
        lesson_options.append(f" ↳ {title}")

selected_lesson = st.sidebar.radio(
    "เลือกบทเรียนหรือหัวข้อย่อย",
    lesson_options,
    label_visibility="collapsed",
    key="selected_lesson",
)

# กดบทหรือหัวข้อย่อยแล้วเปิดบทเรียนได้ทันที
if selected_lesson in chapter_routes:
    page_type = "lesson_chapter"
    selected_chapter = chapter_routes[selected_lesson]
    selected_topic = None

elif selected_lesson in lesson_routes:
    page_type = "lesson_topic"
    (
        selected_chapter,
        selected_topic,
        selected_description,
        selected_example,
    ) = lesson_routes[selected_lesson]

else:
    page_type = "main"


# =========================================================
# 5. ฟังก์ชันแสดงบทเรียน
# =========================================================

def render_lesson(chapter, topic=None):
    st.title("📚 " + chapter)

    topics = LESSONS[chapter]

    if topic is None:
        st.info(
            "เลือกหัวข้อย่อยจากเมนูด้านซ้าย "
            "หรืออ่านภาพรวมของบทเรียนด้านล่าง"
        )

        for title, description, example in topics:
            with st.expander(title):
                st.write(description)
                st.markdown("**ตัวอย่าง**")
                st.success(example)

        return

    selected = next(
        (item for item in topics if item[0] == topic),
        None,
    )

    if selected is None:
        st.error("ไม่พบหัวข้อที่เลือก")
        return

    title, description, example = selected

    st.header(title)
    st.write(description)

    st.markdown("### ตัวอย่าง")
    st.success(example)

    st.markdown("### สรุป")
    st.write(
        "ควรทำความเข้าใจความหมายของนิยาม "
        "สัญลักษณ์ และเงื่อนไขที่เกี่ยวข้อง "
        "ก่อนนำไปใช้แก้โจทย์"
    )

    with st.expander("หัวข้ออื่นในบทนี้"):
        for other_title, other_description, other_example in topics:
            st.markdown(f"**{other_title}**")
            st.write(other_description)
            st.caption("ตัวอย่าง: " + other_example)


# =========================================================
# 6. หน้าแรก
# =========================================================

if page_type == "lesson_chapter":
    render_lesson(selected_chapter)

elif page_type == "lesson_topic":
    render_lesson(selected_chapter, selected_topic)

elif selected_main == HOME:
    st.title("🧠 Math Logic Learning & Solver")

    st.subheader(
        "เว็บไซต์สื่อการเรียนรู้ตรรกศาสตร์ทางคณิตศาสตร์"
    )

    st.write(
        "เรียนรู้เนื้อหา ทบทวนสูตร ทดลองสร้างตารางค่าความจริง "
        "และฝึกทำแบบฝึกหัดได้ในเว็บไซต์เดียว"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("บทเรียน", len(LESSONS))
    col2.metric(
        "หัวข้อย่อย",
        sum(len(topics) for topics in LESSONS.values()),
    )
    col3.metric("เครื่องมือหลัก", len(MAIN_MENU) - 2)

    st.markdown("## 🚀 เริ่มต้นใช้งาน")

    st.markdown("""
    1. เลือกบทเรียนหรือหัวข้อย่อยจากเมนูด้านซ้าย
    2. เลือกเครื่องคำนวณเพื่อตรวจสอบค่าความจริง
    3. เปิดรวมสูตรเพื่อทบทวนกฎตรรกศาสตร์
    4. ฝึกฝนด้วยแบบฝึกหัด เกม และแบบทดสอบ
    """)

    st.markdown("## สัญลักษณ์ตรรกศาสตร์ที่รองรับ")

    st.code("""
¬p       นิเสธ
p ∧ q    และ
p ∨ q    หรือ
p → q    ถ้า...แล้ว
p ↔ q    ก็ต่อเมื่อ
    """)

    st.caption(
        "สามารถใช้ ~p, p & q, p | q, p -> q และ p <-> q ได้ด้วย"
    )

    st.warning(
        "เครื่องคำนวณรองรับตรรกศาสตร์ประพจน์ "
        "แต่ยังไม่คำนวณตัวบ่งปริมาณ ∀ และ ∃ โดยตรง"
    )


# =========================================================
# 7. เครื่องคำนวณตรรกศาสตร์
# =========================================================

elif selected_main == CALCULATOR:
    st.title("🧮 เครื่องคำนวณตรรกศาสตร์")

    st.write(
        "กรอกสูตรโดยใช้ตัวแปร p, q, r และตัวเชื่อมตรรกศาสตร์"
    )

    tabs = st.tabs([
        "ค่าความจริง",
        "ตารางค่าความจริง",
        "ตรวจประเภทสูตร",
        "ตรวจสมมูล",
        "ตรวจการอ้างเหตุผล",
    ])

    with tabs[0]:
        expression = st.text_input(
            "นิพจน์",
            "(p & q) -> r",
            key="single_expression",
        )

        if st.button("คำนวณ", key="single_calculate"):
            try:
                node = parse(expression)
                vars_list = variables(node)

                environment = {}

                for var in vars_list:
                    value = st.selectbox(
                        f"ค่าความจริงของ {var}",
                        ["T", "F"],
                        key=f"single_{var}",
                    )

                    environment[var] = value == "T"

                result = evaluate(node, environment)

                st.success(
                    f"{pretty(node)} = "
                    f"{'T (จริง)' if result else 'F (เท็จ)'}"
                )

            except (ValueError, KeyError) as error:
                st.error(str(error))

    with tabs[1]:
        expression = st.text_input(
            "สูตรสำหรับสร้างตาราง",
            "(p & q) -> r",
            key="table_expression",
        )

        if st.button("สร้างตาราง", key="create_table"):
            try:
                node = parse(expression)
                df = truth_table(node)

                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                )

                st.caption(
                    f"จำนวนแถวทั้งหมด: {len(df)}"
                )

            except ValueError as error:
                st.error(str(error))

    with tabs[2]:
        expression = st.text_input(
            "สูตรที่ต้องการตรวจสอบ",
            "p | ~p",
            key="classify_expression",
        )

        if st.button("ตรวจประเภท", key="classify_button"):
            try:
                node = parse(expression)
                st.success(classify(node))

                df = truth_table(node)
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                )

            except ValueError as error:
                st.error(str(error))

    with tabs[3]:
        left = st.text_input(
            "สูตร A",
            "p -> q",
            key="equiv_left",
        )

        right = st.text_input(
            "สูตร B",
            "~p | q",
            key="equiv_right",
        )

        if st.button("ตรวจสอบสมมูล", key="equiv_button"):
            try:
                same, counterexample = equivalence(
                    parse(left),
                    parse(right),
                )

                if same:
                    st.success(
                        "สูตรทั้งสองสมมูลกันทุกกรณี"
                    )
                else:
                    st.error("สูตรทั้งสองไม่สมมูลกัน")
                    st.write(
                        "ตัวอย่างค่าความจริงที่ทำให้ต่างกัน:",
                        counterexample,
                    )

            except ValueError as error:
                st.error(str(error))

    with tabs[4]:
        premise_text = st.text_area(
            "เหตุ (หนึ่งประพจน์ต่อหนึ่งบรรทัด)",
            "p -> q\np",
            key="premise_text",
        )

        conclusion_text = st.text_input(
            "ข้อสรุป",
            "q",
            key="conclusion_text",
        )

        if st.button(
            "ตรวจสอบการอ้างเหตุผล",
            key="argument_button",
        ):
            try:
                premises = [
                    parse(line)
                    for line in premise_text.splitlines()
                    if line.strip()
                ]

                if not premises:
                    raise ValueError(
                        "กรุณากรอกเหตุอย่างน้อยหนึ่งข้อ"
                    )

                valid, counterexample = check_argument(
                    premises,
                    parse(conclusion_text),
                )

                if valid:
                    st.success(
                        "สมเหตุสมผล: ไม่มีกรณีที่เหตุทุกข้อจริง "
                        "แต่ข้อสรุปเป็นเท็จ"
                    )
                else:
                    st.error("การอ้างเหตุผลไม่สมเหตุสมผล")
                    st.write(
                        "กรณีที่เหตุทุกข้อจริงแต่ข้อสรุปเท็จ:",
                        counterexample,
                    )

            except ValueError as error:
                st.error(str(error))


# =========================================================
# 8. แผนภาพต้นไม้
# =========================================================

elif selected_main == TREE:
    st.title("🌳 แผนภาพต้นไม้ทางตรรกศาสตร์")

    st.write(
        "หน้านี้แสดงแนวคิดพื้นฐานของ Semantic Tableau "
        "เพื่อใช้ศึกษาและฝึกวิเคราะห์สูตร"
    )

    st.markdown("### กฎพื้นฐาน")

    rules = {
        "นิเสธ": [
            "T ¬A เปลี่ยนเป็น F A",
            "F ¬A เปลี่ยนเป็น T A",
        ],
        "ตัวเชื่อมและ": [
            "T(A ∧ B): T A และ T B อยู่กิ่งเดียวกัน",
            "F(A ∧ B): แตกกิ่ง F A หรือ F B",
        ],
        "ตัวเชื่อมหรือ": [
            "T(A ∨ B): แตกกิ่ง T A หรือ T B",
            "F(A ∨ B): F A และ F B อยู่กิ่งเดียวกัน",
        ],
        "อิมพลิเคชัน": [
            "T(A → B): แตกกิ่ง F A หรือ T B",
            "F(A → B): T A และ F B อยู่กิ่งเดียวกัน",
        ],
    }

    for title, items in rules.items():
        with st.expander(title):
            for item in items:
                st.write("• " + item)

    st.markdown("### ตัวอย่าง: ตรวจสอบ p ∨ ¬p")

    st.graphviz_chart("""
    digraph {
        rankdir=TB
        node [shape=box, style="rounded,filled", fillcolor="#F1EFFF"]
        A [label="F(p ∨ ¬p)"]
        B [label="Fp"]
        C [label="F¬p"]
        D [label="Fp"]
        E [label="Tp"]
        X [label="ปิดกิ่ง"]
        A -> B
        A -> C
        B -> D
        C -> E
        D -> X
        E -> X
    }
    """)

    st.info(
        "ภาพนี้เป็นตัวอย่างประกอบการเรียนรู้ "
        "ไม่ใช่เครื่องมือสร้างต้นไม้จากสูตรที่ผู้ใช้ป้อนโดยอัตโนมัติ"
    )


# =========================================================
# 9. รวมสูตรตรรกศาสตร์
# =========================================================

elif selected_main == FORMULA:
    st.title("📖 รวมสูตรตรรกศาสตร์")

    st.write(
        "เลือกหมวดสูตรเพื่อทบทวนความหมายและรูปแบบที่ใช้บ่อย"
    )

    for category, formulas in FORMULAS.items():
        with st.expander(category):
            for formula in formulas:
                st.code(formula, language=None)


# =========================================================
# 10. แบบฝึกหัด
# =========================================================

elif selected_main == PRACTICE:
    st.title("📝 แบบฝึกหัดตรรกศาสตร์")

    st.write(
        "เลือกคำตอบแต่ละข้อ จากนั้นกดปุ่มตรวจคำตอบ"
    )

    for i, question in enumerate(QUESTIONS):
        with st.container(border=True):
            st.markdown(
                f"### ข้อ {i + 1}. {question['question']}"
            )

            answer = st.radio(
                "คำตอบ",
                question["options"],
                index=None,
                key=f"practice_{i}",
                label_visibility="collapsed",
            )

            if st.button(
                "ตรวจคำตอบ",
                key=f"check_practice_{i}",
            ):
                if answer is None:
                    st.warning("กรุณาเลือกคำตอบก่อน")
                elif answer == question["answer"]:
                    st.success(
                        "ถูกต้อง! " + question["explanation"]
                    )
                else:
                    st.error(
                        "คำตอบที่ถูกคือ "
                        + question["answer"]
                    )
                    st.info(question["explanation"])


# =========================================================
# 11. เกมตรรกศาสตร์
# =========================================================

elif selected_main == GAME:
    st.title("🎮 เกมทายค่าความจริง")

    st.write(
        "ฝึกคิดค่าความจริงจากตัวเชื่อมตรรกศาสตร์"
    )

    if "game_question" not in st.session_state:
        st.session_state.game_question = {
            "p": random.choice([True, False]),
            "q": random.choice([True, False]),
            "operator": random.choice(["AND", "OR", "IMP"]),
        }

    question = st.session_state.game_question

    p = question["p"]
    q = question["q"]
    operator = question["operator"]

    symbols = {
        "AND": "∧",
        "OR": "∨",
        "IMP": "→",
    }

    answers = {
        "AND": p and q,
        "OR": p or q,
        "IMP": (not p) or q,
    }

    st.markdown(
        f"### p = {'T' if p else 'F'} "
        f"และ q = {'T' if q else 'F'}"
    )

    st.markdown(
        f"จงหาค่าความจริงของ "
        f"**p {symbols[operator]} q**"
    )

    answer = st.radio(
        "เลือกคำตอบ",
        ["T", "F"],
        index=None,
        key="game_answer",
    )

    col1, col2 = st.columns(2)

    if col1.button("ตรวจคำตอบ"):
        expected = "T" if answers[operator] else "F"

        if answer is None:
            st.warning("กรุณาเลือกคำตอบ")
        elif answer == expected:
            st.success("ถูกต้อง!")
        else:
            st.error(f"คำตอบที่ถูกคือ {expected}")

    if col2.button("สุ่มโจทย์ใหม่"):
        st.session_state.game_question = {
            "p": random.choice([True, False]),
            "q": random.choice([True, False]),
            "operator": random.choice(["AND", "OR", "IMP"]),
        }

        st.session_state.pop("game_answer", None)
        st.rerun()


# =========================================================
# 12. แบบทดสอบ
# =========================================================

elif selected_main == QUIZ:
    st.title("📊 แบบทดสอบตรรกศาสตร์")

    if "quiz_scores" not in st.session_state:
        st.session_state.quiz_scores = {}

    st.subheader("บทเรียนที่เปิดให้ทดสอบ")

    for i, chapter in enumerate(LESSONS.keys()):
        score = st.session_state.quiz_scores.get(chapter, None)
        status = " (ทำแล้ว)" if score is not None else ""

        if st.button(chapter + status, key=f"quiz_chapter_{i}"):
            st.session_state.selected_chapter_quiz = chapter
            st.rerun()

    if "selected_chapter_quiz" in st.session_state:
        chapter = st.session_state.selected_chapter_quiz

        st.divider()
        st.header("📊 แบบทดสอบ: " + chapter)

        topics = LESSONS[chapter]

        quiz_form = st.form(key="quiz_form")
        user_answers = {}

        for i, (title, description, example) in enumerate(topics):
            question = f"{title}: {description} " f"(ตัวอย่าง: {example})"
            quiz_form.markdown(f"**ข้อ {i+1}.** {question}")

            options = ["T (จริง)", "F (เท็จ)"]
            user_answers[i] = quiz_form.radio(
                "คำตอบของคุณ",
                options,
                key=f"quiz_{chapter}_{i}",
                index=None,
                label_visibility="collapsed",
            )

        submit_button = quiz_form.form_submit_button("ส่งคำตอบ")

        if submit_button:
            score = 0
            for i in range(len(topics)):
                if user_answers[i] == "T (จริง)":
                    score += 1

            st.session_state.quiz_scores[chapter] = score

            st.success(
                f"คุณทำได้ทั้งหมด {score} เต็ม {len(topics)} คะแนน"
            )

            del st.session_state.selected_chapter_quiz
            st.rerun()


# =========================================================
# 13. เกี่ยวกับเว็บไซต์
# =========================================================

elif selected_main == ABOUT:
    st.title("ℹ️ เกี่ยวกับ Math Logic")

    col1, col2 = st.columns([1, 2])

    col1.markdown("### เป้าหมาย")
    col1.write(
        "เพื่อให้ทุกคนสามารถเรียนรู้ตรรกศาสตร์ "
        "ได้อย่างเข้าใจ สนุก และสามารถ "
        "นำความรู้ไปประยุกต์ใช้ได้"
    )

    col1.markdown("### ผู้พัฒนา")
    col1.write(
        "พัฒนาโดยใช้ภาษางาน Python และไลบรารี Streamlit "
        "โดยอ้างอิงเนื้อหาจากตำราเรียนและแหล่งข้อมูล "
        "ทางคณิตศาสตร์ที่เชื่อถือได้"
    )

    col2.markdown("### การประยุกต์ใช้ตรรกศาสตร์")
    col2.write(
        "ตรรกศาสตร์เป็นพื้นฐานของศาสตร์หลายด้าน ได้แก่:"
    )

    applications = {
        "คณิตศาสตร์": "การพิสูจน์ทฤษฎีบท",
        "วิทยาการคอมพิวเตอร์": "การเขียนโปรแกรม ปัญญาประดิษฐ์",
        "ปรัชญา": "การวิเคราะห์การให้เหตุผล",
        "กฎหมาย": "การตีความข้อกฎหมาย",
        "การตัดสินใจ": "การประเมินสถานการณ์",
    }

    for app, desc in applications.items():
        st.write(f"• **{app}**: {desc}")

    st.divider()

    st.markdown("## คำชี้แจงด้านลิขสิทธิ์")
    st.write(
        "เนื้อหาและตัวอย่างในเว็บไซต์นี้มีวัตถุประสงค์เพื่อการศึกษาเท่านั้น"
    )
    st.caption("สงวนลิขสิทธิ์ © 2024 Math Logic Project")
