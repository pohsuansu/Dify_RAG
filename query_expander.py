# query_expander.py
import json
import re

# 載入同義字表
with open("synonyms.json", "r", encoding="utf-8") as f:
    synonym_dict = json.load(f)

# 建立同義字反向對應（字詞 → 所屬代表詞）
reverse_index = {}
for key, group in synonym_dict.items():
    for term in group:
        reverse_index[term.lower()] = group  # 所有同義詞都指向 group（list）

# Main 函數（Dify 會呼叫這個）
def expand_query(query: str) -> str:
    # 找出 query 中出現的同義詞（大小寫不敏感）
    found_groups = {}
    query_lower = query.lower()

    for term in reverse_index:
        if re.search(r'\b' + re.escape(term) + r'\b', query_lower):
            key = ', '.join(sorted(set(reverse_index[term]), key=str.lower))
            found_groups[key] = True

    # 組合附註
    if found_groups:
        expanded = query.strip() + "\n" + "\n".join(found_groups.keys())
    else:
        expanded = query  # 沒找到就原樣返回

    return expanded
