def check_and_award_discount(user_id):
    user = users.get(user_id)
    if not user:
        return "User not found"
    
    awarded_codes = []
    for discount in discount_codes:
        if user["points"] >= discount["points_required"] and discount["code"] not in user["claimed_codes"]:
            user["claimed_codes"].append(discount["code"])
            awarded_codes.append(discount)
    return awarded_codes