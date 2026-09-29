# -*- coding: utf-8 -*-
"""
skill_matcher.py - bo so khop ky nang dua tren skills_dictionary.json
Khong dung Deep Learning: chi Regex + tu dien + luat ngu canh.

Cach dung:
    from skill_matcher import SkillMatcher
    m = SkillMatcher("skills_dictionary.json")
    m.skills("Yeu cau: Python, C++, ReactJS, Spring Boot, tieng Anh")
    # -> {'Python', 'C++', 'React', 'Spring Boot', 'English'}
    m.extract(text)   # chi tiet: vi tri, alias khop, loai khop
"""
import json
import re
import unicodedata
from collections import defaultdict


def _nfc(s):
    return unicodedata.normalize("NFC", s)


def fold(s):
    """Bo dau tieng Viet: 'giao tiếp' -> 'giao tiep'."""
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.replace("đ", "d").replace("Đ", "D")


def _key(s):
    """Khoa tra cuu: bo khoang trang/gach noi de 'node js' == 'nodejs'."""
    return re.sub(r"[\s\-]+", "", s.lower())


# Bien ranh gioi thay cho \b (vi \b hong voi C++, C#, .NET):
#   trai : khong dung sau chu/so/_ /+/#/@ va khong nam trong 'ten.mien'
#   phai : khong duoc theo sau boi chu cai/_ /+/#/@  (cho phep chu so: Python3, Java8)
_LEFT_ALNUM = r"(?<![^\W_]|[_+#@])(?<!\w\.)"
_LEFT_SYMBOL = r"(?<![^\W_])"          # alias bat dau bang '.', vd '.net'
_RIGHT = r"(?![^\W\d_]|[_+#@])"
# dau phan cach / gioi tu duoc phep nam giua alias ngan va tu ngu canh lien ke
_SEP = r"(?:(?:[,;/&|•·+:()\[\]]|\b(?:and|or|và|hoặc)\b)\s*)?"
_PREP = r"in|using|with|on|of|for|by|via|trong|với|bằng"


def _alias_regex(alias):
    parts = re.split(r"[\s\-]+", alias)
    body = r"[\s\-]*".join(re.escape(p) for p in parts if p)
    return body


def _compile_group(aliases, ignore_case):
    """Tra ve 2 regex (alias bat dau bang chu/so, alias bat dau bang ky hieu)."""
    flags = re.IGNORECASE if ignore_case else 0
    a_list = sorted({a for a in aliases if a[0].isalnum()}, key=len, reverse=True)
    b_list = sorted({a for a in aliases if not a[0].isalnum()}, key=len, reverse=True)
    out = []
    if a_list:
        out.append(re.compile(_LEFT_ALNUM + "(?:" + "|".join(_alias_regex(a) for a in a_list) + ")" + _RIGHT, flags))
    if b_list:
        out.append(re.compile(_LEFT_SYMBOL + "(?:" + "|".join(_alias_regex(a) for a in b_list) + ")" + _RIGHT, flags))
    return out


class SkillMatcher:
    def __init__(self, path, context_window=60):
        with open(path, encoding="utf-8") as f:
            self.data = json.load(f)
        self.window = context_window
        self.ci_map, self.cs_map = {}, {}
        self.amb_ci, self.amb_cs = {}, {}          # key -> (skill, ctx_regex)
        self.neg = defaultdict(list)
        ci_aliases, cs_aliases, amb_ci_aliases, amb_cs_aliases = [], [], [], []

        for skill, spec in self.data.items():
            cs_list = set(_nfc(a) for a in spec.get("case_sensitive_aliases", []))
            amb = {_nfc(k): v for k, v in spec.get("ambiguous_aliases", {}).items()}

            for a in spec.get("aliases", []):
                a = _nfc(a).lower()
                if a in amb:
                    continue
                variants = [a]
                f = fold(a)
                if f != a and (" " in a or len(a) >= 6):   # them ban khong dau cho alias tieng Viet
                    variants.append(f)
                for v in variants:
                    self.ci_map.setdefault(_key(v), skill)
                    ci_aliases.append(v)

            for a in cs_list:
                if a in amb:
                    continue
                self.cs_map.setdefault(a, skill)
                cs_aliases.append(a)

            for a, words in amb.items():
                alt = "|".join(re.escape(w.lower()) for w in sorted(words, key=len, reverse=True))
                ctx = re.compile(r"(?<![^\W_])(?:" + alt + r")(?![^\W_])", re.IGNORECASE)
                if len(a) <= 2:      # alias 1-2 ky tu: bat buoc tu ngu canh LIEN KE
                    ctx = (
                        re.compile(r"^\s*" + _SEP + r"(?:" + alt + r")(?![^\W_])", re.IGNORECASE),
                        re.compile(r"(?<![^\W_])(?:" + alt + r")\s*(?:" + _PREP + r")?\s*" + _SEP + r"$", re.IGNORECASE),
                    )
                if a in cs_list:
                    self.amb_cs[a] = (skill, ctx)
                    amb_cs_aliases.append(a)
                else:
                    self.amb_ci[_key(a)] = (skill, ctx)
                    amb_ci_aliases.append(a.lower())

            for pat in spec.get("negative_patterns", []):
                self.neg[skill].append(re.compile(pat))

        self.re_ci = _compile_group(ci_aliases, True)
        self.re_cs = _compile_group(cs_aliases, False)
        self.re_amb_ci = _compile_group(amb_ci_aliases, True)
        self.re_amb_cs = _compile_group(amb_cs_aliases, False)

    # ------------------------------------------------------------------
    def _context_ok(self, text, s, e, ctx):
        if isinstance(ctx, tuple):                     # alias ngan: chi xet tu lien ke
            right, left = ctx
            return bool(right.match(text[e:e + 40]) or left.search(text[max(0, s - 40):s]))
        w = self.window
        around = text[max(0, s - w):s] + " " + text[e:e + w]
        return ctx.search(around) is not None

    def extract(self, text):
        text = _nfc(text)
        cands = []                                   # (start, end, skill, matched, kind)

        for rx in self.re_ci:
            for m in rx.finditer(text):
                cands.append((m.start(), m.end(), self.ci_map[_key(m.group(0))], m.group(0), "exact"))
        for rx in self.re_cs:
            for m in rx.finditer(text):
                cands.append((m.start(), m.end(), self.cs_map[m.group(0)], m.group(0), "exact_case"))
        for rx in self.re_amb_ci:
            for m in rx.finditer(text):
                skill, ctx = self.amb_ci[_key(m.group(0))]
                if self._context_ok(text, m.start(), m.end(), ctx):
                    cands.append((m.start(), m.end(), skill, m.group(0), "context"))
        for rx in self.re_amb_cs:
            for m in rx.finditer(text):
                skill, ctx = self.amb_cs[m.group(0)]
                if self._context_ok(text, m.start(), m.end(), ctx):
                    cands.append((m.start(), m.end(), skill, m.group(0), "context"))

        veto = defaultdict(list)                     # skill -> [(s, e)] vung bi loai
        for skill, pats in self.neg.items():
            for p in pats:
                for m in p.finditer(text):
                    veto[skill].append((m.start(), m.end()))

        # Uu tien khop dai nhat; khong cho 2 khop chong len nhau
        cands.sort(key=lambda c: (-(c[1] - c[0]), c[0]))
        occupied = bytearray(len(text))
        out = []
        for s, e, skill, matched, kind in cands:
            if any(occupied[s:e]):
                continue
            if any(s < ve and e > vs for vs, ve in veto.get(skill, [])):
                continue
            for i in range(s, e):
                occupied[i] = 1
            out.append({"skill": skill, "start": s, "end": e, "matched": matched, "kind": kind})
        out.sort(key=lambda d: d["start"])
        return out

    def skills(self, text):
        return {d["skill"] for d in self.extract(text)}


if __name__ == "__main__":
    import sys
    m = SkillMatcher(sys.argv[1] if len(sys.argv) > 1 else "skills_dictionary.json")
    demo = "Yêu cầu: Java, JavaScript, C++, C#.NET, ReactJS, Spring Boot, MySQL, Git. Giao tiếp tiếng Anh tốt, làm việc nhóm."
    for d in m.extract(demo):
        print(d["skill"], "<-", repr(d["matched"]), d["kind"])
