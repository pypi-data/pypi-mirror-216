"""
Flask-friendly plugin for automatically adding login-related endpoints.
"""

import os
from typing import Callable, List, Union
from flask import session, abort, redirect, request, url_for
from google_auth_oauthlib.flow import Flow


class SimpleFlaskGoogleLogin:
    DEFAULT_SCOPES = [
        'https://www.googleapis.com/auth/userinfo.email',
        'openid',
        'https://www.googleapis.com/auth/userinfo.profile',
    ]

    def __init__(
        self,
        app,

        # Google login configuration
        client_secrets_path: str='./client_secrets.json',
        scopes: List[str]=DEFAULT_SCOPES,
        redirect_uri: Union[str, None]=None,

        # View configuration
        authorization_url_handler: Union[Callable, None]=None,
        login_callback_handler: Union[Callable, None]=None,
        logout_handler: Union[Callable, None]=None,
    ):
        """
        Register with the Flask application if passed.

        :param client_secrets_path: Path to client secrets downloaded from
            Google developer console. Contains client ID and secret.
        :param scopes: List of scopes to request
        :param redirect_uri: This is the URI that Google will be asked to send
            the login code to.
        :param authorization_url_handler: Handles the authorization URL. The 
            returned value is the view that will be used for the initial login
            redirect. This is used to replace the redirect with a browser open,
            for example.
        :param login_callback_handler: Handles the newly-initialized google
            session. This is used to initialize login sessions, for example.
        """
        self.client_secrets_path = client_secrets_path
        self.scopes = scopes
        self.redirect_uri = redirect_uri
        
        self.authorization_url_handler = authorization_url_handler or redirect
        self.login_callback_handler = login_callback_handler \
            or self.default_login_handler
        self.logout_handler = logout_handler or self.default_logout_handler

        if app is not None:
            self.init_app(app)

    def init_app(
        self,
        app,
        login_endpoint: Union[str, None] = '/login',
        callback_endpoint: Union[str, None] = '/login/callback',
        logout_endpoint: Union[str, None] = '/logout',
        force_https: bool = True,
    ):
        """
        Register views with the Flask app.

        :param login_endpoint: Path to send users to, to login
        :param callback_endpoint: Path to send users to, to finish authorization
            using the Google-provided token
        :param logout_endpoint: Path to send users to, to logout
        """
        assert app is not None, 'Flask application must not be None'
        if login_endpoint is not None:
            app.add_url_rule(login_endpoint, view_func=self.login)
        if callback_endpoint is not None:
            app.add_url_rule(callback_endpoint, view_func=self.callback)
        if logout_endpoint is not None:
            app.add_url_rule(logout_endpoint, view_func=self.logout)
        if force_https:
            app.before_request(self.before_request)

    @property
    def flow(self):
        """
        Get or create a new flow instance for this client.
        """
        if not hasattr(self, '_flow'):
            redirect_uri = os.path.join(
                request.host_url, url_for('callback')[1:])
            self._flow = Flow.from_client_secrets_file(
                client_secrets_file=self.client_secrets_path,
                scopes=self.scopes,
                redirect_uri=self.redirect_uri or redirect_uri,
            )
        return self._flow

    def login(self):
        """
        Save a randomly-generated state to prevent prevent CSRF attacks:
        https://auth0.com/docs/secure/attack-protection/state-parameters

        Additionally, redirect users to the authorization URL.
        """
        authorization_url, state = self.flow.authorization_url()
        session['state'] = state
        return self.authorization_url_handler(authorization_url)

    def callback(self):
        """
        Exchange the code into a proper authorization token. Then, initialize
        a session that we can use to make calls to the Google API for user
        information.
        """
        if not session['state'] == request.args['state']:  # state as nonce
            abort(500)

        self.flow.fetch_token(authorization_response=request.url)
        google = self.flow.authorized_session()

        return self.login_callback_handler(google)

    def default_login_handler(self, google):
        """
        By default, after login, add the user's basic information to the
        server-side session. Redirect to the homepage.
        """
        user = google.get('https://www.googleapis.com/userinfo/v2/me').json()
        session.update(user)
        return redirect('/')

    def logout(self):
        """
        Logout the user by clearing the server-side session.
        """
        session.clear()
        return self.logout_handler()
    
    def default_logout_handler(self):
        """
        By default, after logout, simply redirect back to the homepage.
        """
        return redirect('/')
    
    def before_request(self):
        """
        NOTE: Hacking this in as we're forcing SSL below. Without this, all
        request.{url,base_url} calls will use http incorrectly when assembling
        oauth redirect URLs.
        """
        request.scheme = 'https'
