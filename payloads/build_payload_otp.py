def build_otp_payload(config, user_id, otp, transaction_id):
    return {
        "issuerName": config.get("issuer_name", "HDBank"),
        "userID": user_id,
        "otp": "00" + otp,
        "transactionID": transaction_id
    }

def build_otpcr_payload(config, user_id, otp, transaction_id):
    return {
        "issuerName": config.get("issuer_name", "HDBank"),
        "userID": user_id,
        "otp": "09" + otp,
        "transactionID": transaction_id
    }
