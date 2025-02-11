

def normalize_menu(name):
    name = str(name)

    keyword_map = {
            "덮밥": ["덮밥"],
            "자장면" : ["자장면", "짜장면"],
            "볶음밥": ["볶음밥"],
            "스파게티": ["스파게티", "파스타"],
            "닭개장": ["닭개장"],
            "찜닭": ["찜닭", "불닭로제찜닭"],
            "도시락": ["한솥", "도시락"],
            "김치찌개": ["김치찌개", "김치찌게", "김치 찌개", "김치 찌게"],
            "된장찌개": ["된장찌개", "된장찌게", "된장 찌개", "된장 찌게"],
            "돈까스": ["돈가스", "까스", "돈까스", "가츠", "돈카츠"],
            "라면": ["라면"],
            "카레": ["카레", "커리"],
            "모다기": ["모다기"],
            "순두부찌개": ["순두부 찌개", "순두부찌개"],
            "쉐이크": ["쉐이크"],
            "순대국밥": ["순대국밥", "순대국"],
            "설렁탕": ["설렁탕"],
            "간짜장": ["간짜장"],
            "짬뽕": ["짬뽕"]
            }

    matched_categories = []

    for category, keywords in keyword_map.items():
        if any(keyword in name for keyword in keywords):
            matched_categories.append(category)

    if len(matched_categories)==1:
        return matched_categories[0]
    elif len(matched_categories)>1:
        return matched_categories[0]
    return name





