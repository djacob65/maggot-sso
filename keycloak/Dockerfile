FROM quay.io/keycloak/keycloak:25.0.6

RUN mkdir /opt/keycloak/certs

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
    KEYCLOAK_ADMIN_PASSWORD=adminpass

EXPOSE 8080
EXPOSE 8443

ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]
