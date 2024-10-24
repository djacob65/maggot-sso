FROM quay.io/keycloak/keycloak:23.0.7

# Environment for Apache
ENV \
    KC_HOSTNAME_PORT=8080 \
    KC_HTTP_ENABLED=true \
    KC_HOSTNAME_STRICT_BACKCHANNEL=false \
    KC_HOSTNAME_STRICT=false \
    KC_HOSTNAME_STRICT_HTTPS=false \
    KC_HEALTH_ENABLED=true \
    KC_DB=postgres \
    KC_DB_URL=jdbc:postgresql://postgres/keycloak \
    KC_DB_USERNAME=keycloak \
    KC_DB_PASSWORD=kcpass01 \
    KEYCLOAK_ADMIN=admin \
    KEYCLOAK_ADMIN_PASSWORD=admin,2024

EXPOSE 8080

ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]
