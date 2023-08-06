python setup.py sdist bdist_wheel
pip install twine
twine check dist/*
twine upload dist/*

# OIDC Library

## Installation

Install the OIDC Library using pip:

```bash
pip install oidc_drf


Add `'oidc_drf'` to the `INSTALLED_APPS` list in your Django project's settings:

python3 manage.py makemigrations
python3 manage.py migrate

Configure the following settings in your Django project's settings module:

```python

# OIDC settings
OIDC_USE_NONCE = True #defalut true
OIDC_USE_PKCE = True #defalut true

OIDC_RP_SIGN_ALGO = 'RS256'
OIDC_RP_SCOPES = 'openid email'

OIDC_RP_CLIENT_ID = 'my_client_id' 
OIDC_RP_CLIENT_SECRET = '' # if the client is public you can leave it empty
OIDC_OP_JWKS_ENDPOINT = 'http://127.0.0.1:8080/realms/mol/protocol/openid-connect/certs'
OIDC_OP_AUTHORIZATION_ENDPOINT = 'http://127.0.0.1:8080/realms/mol/protocol/openid-connect/auth'
OIDC_OP_TOKEN_ENDPOINT = 'http://127.0.0.1:8080/realms/mol/protocol/openid-connect/token'
OIDC_OP_USER_ENDPOINT = 'http://127.0.0.1:8080/realms/mol/protocol/openid-connect/userinfo'
OIDC_OP_LOGOUT_ENDPOINT ='http://127.0.0.1:8080/realms/mol/protocol/openid-connect/logout'

OIDC_AUTHENTICATION_SSO_CALLBACK_URL = 'http://localhost:3000/callback' #identity provider (IDP) will redirect you to this url after login
OIDC_LOGOUT_REDIRECT_URL = 'http://localhost:3000' # identity provider (IDP) will redirect you to this url after logout

# example mapping
# 'field_in_my_user_model':'field_in_in_oidc'
OIDC_FIELD_MAPPING = {
    'email': 'email',
    'first_name': 'given_name',
    'last_name': 'family_name',
}

# Django Rest Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'oidc_drf.drf.CustomOIDCAuthentication',  # This is important to be the first one so it can wo
    ],
}

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'oidc_drf.backends.OIDCAuthenticationBackend',
]



Add routing to urls.py
Next, edit your urls.py and add the following:

from django.urls import path, include

urlpatterns = [
    # ...
    path('oidc/', include('oidc_drf.urls')),
    # ...
]



======================================================================================
# front end side

import axios from 'axios';

export const ssoAuthUriGenerator = async () => {
        try {
            let response = await axios.get(`http://localhost:8000/oidc/auth/`);
            let data = await response.data
            
            # if you are using PKCE or nonce these value will be returned to and you should save theme if localstorage or anywhere else as you will need them to be send in the callback function
            # data.oidc_states is
            # {
            # "nonce": "ipPsbJWiMigOKEI0qgN5HnHaPYsTvdGn",
            # "code_verifier": "FjD8cZ2t4JpWMsxc9Lo1dZGRze7Rogr9N8I6ulIewzMIIyffgI72GVtERuF7CeNE"
            # }

            localStorage.setItem("oidc_states", (JSON.stringify(data.oidc_states))); 
            window.location.href = data.redirect_url;

        } catch (error) {
            console.log(error)
        }
    };



export const ssoCallBack = async () => {
    # when user come to the callback page you should call this function which will take necessery param and send them to backend callback function + oidc_states object which we saved earlier


    const state = queryParams.get('state');
    const sessionState = queryParams.get('session_state');
    const code = queryParams.get('code');

        try {
            let payload = {}
            const storedStatesSting = localStorage.getItem("oidc_states");
            if (storedStatesSting) {
                payload =JSON.parse(storedStatesSting);
            }

            let response = await axios.post(`oidc/callback/?state=${state}&session_state=${sessionState}&code=${code}`, payload );
            let data = response.data;

            # you can use the access token to add it to the Authorization header as "Bearer" to call any portected api view by your DRF application

            # we will also need oidc_id_token 
            localStorage.setItem("oidc_id_token",data.oidc_id_token)
            localStorage.setItem("access",data.access)
            localStorage.setItem("refresh",data.refresh)

        } catch (error) {
            console.log(error)
        }
    };
