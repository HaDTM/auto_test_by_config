def build_activation_payload(config, user_id):
    return {
        "issuerName": config.get("issuer_name", "HDBank"),
        "userID": user_id,
        "userName": config.get("user_name", f"userName {user_id}"),
        "customerName": config.get("customer_name", f"customerName {user_id}"),
        "customerTypeID": config.get("customer_type_id", 1),
        "cifNumber": config.get("cif_number", "0000000000000002"),
        "phoneNumber": config.get("activation_phone", "0398448844"),
        "email": config.get("activation_email", "test1001@gmail.com"),
        "branchID": config.get("activation_branch", "001"),
        "aidVersion": config.get("aid_version", "99")
    }
