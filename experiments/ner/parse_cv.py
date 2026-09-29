# -*- coding: utf-8 -*-
"""
parse_cv.py - Doc CV that: ket hop NER (spaCy da train) + Dictionary (skill_matcher.py)

Trien khai:
    - Dictionary luon la nguon CHINH (do chinh xac cao, da kiem chung 52 test case).
    - NER chi bo sung THEM cac ung vien ma Dictionary bo sot (chua co trong tu dien),
      duoc gan nhan "goi_y_ai" de nguoi dung/QTV xac nhan truoc khi dua vao thong ke chinh thuc.
    - Day chinh la kien truc hybrid da giai thich: NER + chuan hoa qua taxonomy.

Cach dung:
    python parse_cv.py duong_dan_file.pdf
"""
import sys
import json
import spacy
from skill_matcher import SkillMatcher

NER_MODEL_PATH = "model/model-last"
DICT_PATH = "skills_dictionary.json"


def extract_text(path):
    """Doc noi dung tho tu file CV. Ho tro .txt/.pdf/.docx."""
    if path.endswith(".txt"):
        return open(path, encoding="utf-8", errors="ignore").read()
    if path.endswith(".pdf"):
        import pypdf
        reader = pypdf.PdfReader(path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if path.endswith(".docx"):
        import docx
        d = docx.Document(path)
        return "\n".join(p.text for p in d.paragraphs)
    raise ValueError(f"Chua ho tro dinh dang: {path}")


class HybridCVParser:
    def __init__(self, dict_path=DICT_PATH, ner_path=NER_MODEL_PATH):
        self.matcher = SkillMatcher(dict_path)
        try:
            self.nlp = spacy.load(ner_path)
        except (OSError, IOError):
            self.nlp = None  # cho phep chay chi voi dictionary neu chua co model

    def parse(self, text):
        # 1) Dictionary - nguon chinh, do tin cay cao
        dict_hits = self.matcher.extract(text)
        confirmed = {h["skill"] for h in dict_hits}
        occupied = [(h["start"], h["end"]) for h in dict_hits]

        # 2) NER - chi lay vung KHONG trung voi Dictionary, danh dau la goi y
        suggested = []
        if self.nlp is not None:
            doc = self.nlp(text)
            for ent in doc.ents:
                if any(ent.start_char < e and ent.end_char > s for s, e in occupied):
                    continue  # da duoc Dictionary bat, bo qua de tranh trung
                norm = self.matcher.skills(ent.text)  # thu chuan hoa ve ten skill chuan
                suggested.append({
                    "text": ent.text,
                    "canonical": sorted(norm) if norm else None,
                    "status": "khop_tu_dien_qua_ngu_canh" if norm else "chua_co_trong_tu_dien",
                })

        return {
            "skills_xac_nhan": sorted(confirmed),          # dua thang vao Match Rate / Skill Gap
            "goi_y_tu_ner": suggested,                      # hien thi rieng, can nguoi dung xac nhan
        }


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "demo.txt"
    text = extract_text(path)
    parser = HybridCVParser()
    result = parser.parse(text)
    print(json.dumps(result, ensure_ascii=False, indent=2))
