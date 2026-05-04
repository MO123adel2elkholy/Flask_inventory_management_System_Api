from Ecommerce.utils.jwt_handller import jwt

print("DEBUG: JWT_callback module imported, jwt id:", id(jwt))


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    print("🔥 LOADER CALLED; jwt id:", id(jwt))
    jti = jwt_payload["jti"]

    # Lazy imports to avoid circular import / import-timing issues
    from Ecommerce.apps import database as db
    from Ecommerce.apps.models.inventory_models import TokenBlocklist

    return db.session.query(TokenBlocklist.id).filter_by(jti=jti).first() is not None
