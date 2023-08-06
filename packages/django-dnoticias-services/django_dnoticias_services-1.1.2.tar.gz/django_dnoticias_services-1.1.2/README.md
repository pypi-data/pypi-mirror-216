# dnoticias_services

## Import:

`from dnoticias_services.<module> import <function_name>`

`eg:`

`from dnoticias_services.communications import send_email`


## Modules:
* mail
* authentication
* payments
* utils
* subscriptions
* editions

## Methods:
* Authentication
  - create_user: Creates a new user in keycloak

    `create_user(email, first_name='', last_name='', enabled=True, email_verified=False, password=None, temporary_password=True, is_staff=False, is_superuser=False, max_sessions=2, send_email_to_user=False)`
  - update_user: Updates an existing user in keycloak and backends

    `update_user(email, first_name='', last_name='', enabled=True, is_staff=False, is_superuser=False, max_sessions=2, update_attributes=True)`
  - update_password: Updates an user password. Can send notification emails too.

    `update_password(email, password, temporary=False, send_email_to_user=False)`
  - get_token: Gets an user token.

    `get_token(email, password)`
  - refresh_token: Refresh an user token.

    `refresh_token(refresh_token)`
  - logout_user: Logouts an user using his refresh token.

    `logout_user(refresh_token)`
  - send_update_account: Sends an update action to the given account. I.e: UPDATE_PASSWORD

    `send_update_account(email, action)`

  - keycloak_user_exists: Checks if a given email address exists on keycloak

    `keycloak_user_exists(email)`

* Mail
  - create_campaign

    `create_campaign(template_uuid, brand_group_uuid, newsletter_uuid, title, subject, context=dict(), from_email=None, from_name=None, track_opens=True, track_clicks=True, api_key=None, timeout=None)`
  - send_campaign

    `send_campaign(template_uuid, brand_group_uuid, newsletter_uuid, title, subject, context=dict(), from_email=None, from_name=None, track_opens=True, track_clicks=True, api_key=None, timeout=None)`
  - send_email

    `send_email(email, template_uuid, brand_group_uuid, subject, context=dict(), from_email=None, from_name=None, attachments=[], track_opens=True, track_clicks=True, api_key=None, timeout=None)`
  - send_email_bulk

    `send_email_bulk(emails=[], template_uuid=None, brand_group_uuid=None, subject="", context=list(), from_email=None, from_name=None, attachments=[], track_opens=True, track_clicks=True, api_key=None, timeout=None)`

* Payments
  * Items
    - create_item Creates an item from dnoticias-payments via API

      `create_item(name, slug, price, active=True, extra_attrs=dict(), description="", images=dict(), shippable=False, interval=None, interval_count=None, trial_interval=None, trial_interval_count=None, offers=[], category=None, api_key=None, timeout=None)`
    - update_item: Updates an item from dnoticias-payments via API

      `update_item(uuid, name=None, slug=None, extra_attrs=None, description=None, price=None, active=None, images=None, shippable=None, interval=None, interval_count=None, trial_interval=None, trial_interval_count=None, offers=None, category=None, api_key=None, timeout=None)`
    - delete_item: Deletes an item from dnoticias-payments via API

      `delete_item(uuid, api_key=None, timeout=None)`
    - get_item: Gets an item by its slug or accounting id

      `get_item(slug=None, accounting_id=None, api_key=None, timeout=None)`

  * Orders
    - get_user_order_datatable: Gets all the user orders from dnoticias-payments. Works only with datatables.

      `get_user_order_datatable(request, user_email, api_key=None)`

    - get_user_orders: Gets all the user orders from dnoticias-payments.

      `get_user_orders(user_email, api_key=None)`

    - get_order_detail: Gets all the info for a given order.

      `get_order_detail(order_id, api_key=None)`

  * Subscriptions
    - get_subscription: Get the subscription data for an user.

      `get_subscription(email, status, api_key=None, timeout=None)`

  * Payments
    - setup_payment_intent: Setup a intent to add payment details to the customer or to the subscription

      `setup_payment_intent(email=None, subscription_id=None, api_key=None)`
    
    - change_subscription_payment_method : Changes the default payment method of a subscription
    
      `change_subscription_payment_method(subscription_id, payment_method, api_key=None)`
    
    - generate_payment_details : Generate a payment from email, item and the method

      `generate_payment_details(email, payment_provider_id, item_id=None, amount=None, api_key=None)`

    - create_order: Creates a new order for a given user

      `create_order(context, api_key=None)`
  
  * Coupons
    - get_coupon: Get a coupon information from payments.
      `get_coupon(coupon_remote_id, api_key=None)`
    - get_suitable_coupons: Gets all the suitables coupons for an item (no expiration time, unlimited uses, etc).
      `get_suitable_coupons(item_remote_id, api_key=None)`

  * Providers
    - get_payment_providers: Gets all the payment providers with status active created in dnoticias-payments.

      `get_payment_providers(request, api_key=None)`

* Utils
  - request_object: Replicates the request object from django. Used to datatables.

    `Same methods/attrs as the original request. Used to provide the request information to datatables because the original one is inmutable.`

* Subscriptions
  - get_user_notifications: Gets all the non-opened notifications for an specific user by its email
    `get_user_notifications(email, api_key=None)`
  - get_user_components: Gets all the components for an specific user by its email. The response contain paper components and digital components with its roles.
    `get_user_components(email, api_key=None)`
  - get_subscriptions: Gets the user subscriptions.
    `get_subscriptions(api_key=None)`
  - get_roles_select2: Gets all the roles from subscriptions. Only works with select2.
    `get_roles_select2(api_key=None)`
  - get_roles: Gets all the roles from subscriptions.
    `get_roles(api_key=None)`
  - delete_subscription_coupon: Delete a coupon (clear field) for all the items that had used it.
    `delete_subscription_coupon(remote_id, api_key=None)`


## Settings
* Authentication
    - KEYCLOAK_SERVER_URL
    - KEYCLOAK_ADMIN_REALM_NAME
    - KEYCLOAK_USER_REALM_NAME
    - KEYCLOAK_ADMIN_USERNAME
    - KEYCLOAK_ADMIN_PASSWORD
    - KEYCLOAK_CLIENT_ID
    - KEYCLOAK_CLIENT_SECRET_KEY
    - DEFAULT_FROM_EMAIL
    - MAIL_USER_PASSWORD_NOTIFICATION_TEMPLATE_UUID
    - EMAIL_BRAND_GROUP_UUID
    - MAIL_USER_PASSWORD_NOTIFICATION_SUBJECT
    - MAIL_USER_CREATION_SUBJECT

* Mail
    - MAIL_SERVICE_ACCOUNT_API_KEY
    - MAIL_SERVICE_REQUEST_TIMEOUT
    - SEND_EMAIL_API_URL (https://comunicacao.dnoticias.pt/api/send/mail/)
    - SEND_EMAIL_BULK_API_URL (https://comunicacao.dnoticias.pt/api/send/mail/bulk/)
    - SEND_CAMPAIGN_API_URL (https://comunicacao.dnoticias.pt/api/send/campaign/)
    - CREATE_CAMPAIGN_API_URL (https://comunicacao.dnoticias.pt/api/send/create/campaign/)
    - EMAIL_USER_DATATABLE_LIST_API_URL (http://xyz.dnoticias.pt/api/user/{}/mails/datatable/)

* Payments
    - PAYMENT_SERVICE_ACCOUNT_API_KEY
    - PAYMENT_SERVICE_REQUEST_TIMEOUT
    - ITEM_API_URL (https://xyz.dnoticias.pt/api/items/)
    - ORDER_USER_DATATABLE_LIST_API_URL (https://payments.dnoticias.pt/api/user/{}/orders/datatable/)
    - PAYMENT_PROVIDERS_SELECT2VIEW_API_URL (https://payments.dnoticias.pt/api/payment/providers/select2/{}/)
    - ORDER_USER_LIST_API_URL (https://payments.dnoticias.pt/api/user/{}/orders/)
    - ORDER_DETAIL_API_URL (https://payments.dnoticias.pt/api/order/{}/)
    - ORDER_CREATE_API_URL (https://payments.dnoticias.pt/api/order/create/)
    - PAYMENTS_GET_SINGLE_COUPON_API_URL (https://payments.dnoticias.pt/api/coupon/{}/)
    - PAYMENTS_GET_COUPONS_API_URL (https://payments.dnoticias.pt/api/coupons/select2/)
    - PAYMENTS_GET_REMOTE_ID_API_URL (https://payments.dnoticias.pt/api/items/get/remote_id/)
    - PAYMENTS_GET_SUBSCRIPTION_API_URL (https://payments.dnoticias.pt/api/subscriptions/get/)

* Subscriptions
    - SUBSCRIPTION_SERVICE_ACCOUNT_API_KEY
    - SUBSCRIPTION_SERVICE_REQUEST_TIMEOUT
    - USER_NOTIFICATION_API_URL (http://xyz.dnoticias.pt/api/user-notifications/{}/)
    - USER_COMPONENTS_API_URL (http://xyz.dnoticias.pt/api/user-components/{}/)
    - BILLING_API_URL
    - ADDRESS_API_URL
    - ROLES_API_URL
    - ROLES_SELECT2_API_URL
    - USER_ROLES_API_URL
    - USER_SUBSCRIPTIONS_API_URL
    - SUBSCRIPTION_DELETE_COUPON_API_URL

* Editions
    - EDITIONS_USER_CONSUMABLES_API_URL (https://edicao.dnoticias.pt/api/1_0/user/{}/consumables/)
