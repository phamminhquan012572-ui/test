import subprocess
import os
import sys
import ast
import unicodedata

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(CURRENT_DIR)
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from test_de1 import tests

def normalize(s):
    return s.lower().replace(" ", "").replace(":", "").replace("=", "").replace(".", "").replace(",", "").strip()

def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').replace('đ', 'd').replace('Đ', 'D')

def run_code(file, input_data):
    try:
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        result = subprocess.run(
            [sys.executable, file],
            input=input_data.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5,
            env=env
        )
        output = result.stdout.decode("utf-8", errors="replace").strip().splitlines()
        return [line.strip() for line in output if line.strip()]
    except subprocess.TimeoutExpired:
        return ["loiquathoigian"]

def is_dict_expected(expected):
    return isinstance(expected, dict)

def test_dict_output(output, expected_dict):
    for line in output:
        try:
            d = ast.literal_eval(line)
            if isinstance(d, dict) and d == expected_dict:
                return True
        except:
            continue
    return False

def test_normal_output(output, expected):
    # Try structural matching for set, list, tuple, dict
    try:
        exp_val = ast.literal_eval(expected) if isinstance(expected, str) else expected
        if isinstance(exp_val, (dict, set, list, tuple)):
            for line in output:
                try:
                    out_val = ast.literal_eval(line)
                    if out_val == exp_val:
                        return True
                except:
                    pass
    except:
        pass

    # Fallback to string matching
    expected_norm = normalize(str(expected))
    expected_no_accents = strip_accents(expected_norm)
    for out in output:
        out_norm = normalize(out)
        out_no_accents = strip_accents(out_norm)
        if expected_norm in out_norm or expected_no_accents in out_no_accents:
            return True
    return False

def grade(student_id="unknown", base_dir="submissions_de1"):
    if not os.path.isabs(base_dir):
        base_dir = os.path.join(CURRENT_DIR, base_dir)
    total_score = 0
    max_score = 0
    print(f"📋 Bắt đầu chấm điểm cho {student_id}\n")
    for bai, testcases in tests.items():
        file_path = os.path.join(base_dir, f"{bai}.py")
        if not os.path.exists(file_path):
            print(f"❌ Không tìm thấy file: {file_path}")
            continue

        print(f"🔹 {bai.upper()}")
        case_list = testcases if isinstance(testcases, list) else [testcases]
        case_right = 0
        for idx, test in enumerate(case_list, 1):
            output = run_code(file_path, test["input"])
            this_ok = False
            raw_exp = test["expected"]
            exp_list = [raw_exp] if isinstance(raw_exp, (str, dict)) else list(raw_exp)
            for expected in exp_list:
                if is_dict_expected(expected):
                    if test_dict_output(output, expected):
                        this_ok = True
                        break
                else:
                    if test_normal_output(output, expected):
                        this_ok = True
                        break
            if this_ok:
                print(f"  ✅ Test {idx}: Input {repr(test['input'].strip())} → Đúng")
                case_right += 1
            else:
                print(f"  ❌ Test {idx}: Input {repr(test['input'].strip())} → Sai")
        bai_score = round(case_right / len(case_list), 2)
        total_score += bai_score
        max_score += 1
        print(f"    Kết quả: {case_right}/{len(case_list)} test đúng → {bai_score} điểm\n")

    print(f"""
    ╔══════════════════════════════════╗
    ║ 🎯 Tổng điểm: {total_score}/10              
    ║ 👤 Sinh viên: Nguyễn Văn A -MSSV:...        
    ║ 🖥️  Máy số : 10                  
    ║ 📄  Đề số  : 01                  ║
    ╚══════════════════════════════════╝
    """)


if __name__ == "__main__":
    grade("sv001")
