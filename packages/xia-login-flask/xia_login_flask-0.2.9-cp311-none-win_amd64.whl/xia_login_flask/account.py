import fnmatch
import json
import base64
from functools import wraps
import uuid
from urllib.parse import urlparse, urlunparse, urlencode
from typing import Type
from datetime import datetime
from flask import Blueprint, request, Response, g, jsonify, url_for, redirect, render_template, make_response, abort
from xia_engine import XiaError, Acl
from xia_token_flask import FlaskToken
from xia_user import User, UserRoles, RoleMatrix
from xia_mail_sender import MailSender


class XiaLoginFlask:
    """XIA Login Module for Flask

    Logged in status:
        * all user related information was retrieved by cookies.
        * g.user_id: User Mail Address
        * g.user_info: A dictionary holds the user related information
        * g.acl: A dictionary holds the User's permissions for all requested applications.
    """
    @classmethod
    def get_redirect_link(cls, endpoint: str, **kwargs):
        """Get redirect link

        Args:
            endpoint: endpoint of flask name
            **kwargs: parameters

        Returns:
            A full url to call
        """
        url_path = urlparse(request.base_url)
        link = "https://" + url_path.netloc + url_for(endpoint) + "?"
        queries = [key + "=" + str(value) for key, value in kwargs.items()]
        link += "&".join(queries)
        return link

    @classmethod
    def get_token_from_url(cls, link: str):
        """Get token value from URL

        Args:
            link: full URL

        Returns:

        """
        if not link:
            return ""
        url_path = urlparse(link)
        queries = url_path.query.split("&")
        token = ""
        for query in queries:
            if query.startswith("token="):
                token = query[6:]
        return token

    @classmethod
    def get_callback_url(cls, requested_fqdn: str, url_list: list):
        """Get Callback URL from a list of requested url

        Args:
            requested_fqdn: Requested FQDN
            url_list: Callback url list
        """
        for url in url_list:
            parsed = urlparse(url)
            fqdn = parsed.netloc
            if fnmatch.fnmatch(requested_fqdn, fqdn):
                new_parsed = list(parsed)
                new_parsed[1] = requested_fqdn
                return urlunparse(tuple(new_parsed))

    @classmethod
    def get_account_blueprint(
            cls, /,
            home_path: str,
            path_name: str,
            template_location: str,
            token_manager: Type[FlaskToken],
            user_manager: Type[User],
            profile_manager: Type[UserRoles] = None,
            app_manager: Type[RoleMatrix] = None,
            app_name: str = "",
            mail_sender: Type[MailSender] = None,
            debug: bool = False,
    ):
        """Get Account Management Blueprint

        Args:
            home_path: homepage path of flask, should be parsable by using url_for. Example: home.home_page
            path_name: sub flask path name of the parent app. Example: account so url_for(account.login) allows login
            token_manager: Token Management Class, should be a subclass of FlaskToken
            user_manager: User Management Class, should be a subclass of User (xia-user package)
            profile_manager: User profile Management Class, should be a subclass of UserRoles (xia-user package)
            app_manager: Application Management Class, should be a subclass of RoleMatrx (xia-user package)
            app_name: The profile of which app should be retrieved
            mail_sender: Mail Sender, should be a subclass of MailSender
            template_location: Where the template Html files could be found. Example: "accounts" => "templates/accounts"
            debug: Generate debug page: Weather the program should generate a debug endpoint

        Returns:
            Flask blueprint
        """
        account = Blueprint(path_name, __name__)

        xia_logout_cookie = "xia_logout_list"

        template_home = template_location + "/index.html"
        template_confirm = template_location + "/confirm.html"
        template_forgot = template_location + "/forgot.html"
        template_login = template_location + "/login.html"
        template_logout = template_location + "/logout.html"
        template_reset = template_location + "/reset.html"
        template_signup = template_location + "/signup.html"

        url_home = path_name + ".home"
        url_confirm = path_name + ".confirm"
        url_login = path_name + ".login"
        url_refresh = path_name + ".refresh"
        url_reset = path_name + ".reset"
        url_sso = path_name + ".sso"
        url_callback = path_name + ".callback"

        template_mail_password_reset = template_location + "/mails/password_reset.html"
        template_mail_account_confirm = template_location + "/mails/account_confirm.html"

        app_info = {
            "mapping": {
                "Change Password": f"/{path_name}/reset"
            }
        }

        def _get_user_app_info(user_id: str, user_info: dict):
            """Get application related user information

            Args:
                user_id: User unique identification id
                user_info: User information authorized by user for a specific configuration

            Returns:
                user_acl and use profile
            """
            if profile_manager and app_name:
                user_role = profile_manager.load(app_name=app_name, user_name=user_id)
                if user_role:
                    user_app_info = user_role.get_user_acl()
                    user_acl = user_app_info.acl
                    return user_acl, user_app_info.user_profile
            return Acl.from_display(content=[]), {}  #: default empty ACL and empty app_user_info

        def _set_user_token(resp: Response, user_info: dict, path_refresh: str):
            user_id = user_info["user_id"]
            user_acl, user_app_info = _get_user_app_info(user_id, user_info)
            user_info["app_name"] = app_name
            user_info["app_profile"] = user_app_info
            token_manager.set_root_header_token(resp, user_info)
            token_manager.set_app_header_token(resp, app_name, app_info, user_app_info)
            token_manager.set_access_token(resp, user_id, user_acl, user_info, {"root": path_refresh})
            token_manager.set_refresh_token(resp, user_id, {"root": path_refresh})
            # Set logout list cookie to empty list based
            resp.set_cookie(xia_logout_cookie, base64.b64encode(json.dumps([]).encode()).decode(), max_age=2**25)

        @account.url_value_preprocessor
        def app_necessary_data(endpoint, values):
            if endpoint == "static":
                return
            g.time = datetime.now()
            g.base_url = urlparse(request.base_url)
            g.endpoint, g.values = endpoint, values
            if dict(request.args).get("next", None) == g.endpoint:
                request.args.pop("next")  # Avoid infinity loop
            # Try to see the status of access token and access signal
            g.user_id, g.acl, g.user_info, g.token_info = token_manager.parse_access_token()
            root_header, app_header = token_manager.get_root_header_token(), token_manager.get_app_header_token()
            root_header.get("root_menu", {}).pop(app_header.get("app_name", ""), None)
            g.header_info = root_header | app_header
            if not g.user_id:
                g.user_id, g.token_info = token_manager.parse_refresh_signal()

        @account.route('/', methods=["GET"])
        def home():
            return render_template(template_home, title="home", msg="")

        @account.route('/login', methods=["GET", "POST"])
        def login():
            next_values = dict(request.args)
            next_point = next_values.pop('next', None)
            login_token = next_values.pop("token", None)
            path_refresh = url_for(url_refresh)
            resp = redirect(
                url_for(next_point, **next_values) if next_point else url_for(home_path))  # successful resp
            if request.method == "POST":
                user_email, passwd, creator = request.form['email'], request.form['password'], request.remote_addr
                try:
                    user_info = user_manager.login_basic(user_email, passwd).get_display_data()
                except XiaError as e:
                    return render_template(template_login, title="Login", msg=e.args[0])
                # Logged in, should get user_info and acl now
                _set_user_token(resp, user_info, path_refresh)
                return resp
            else:
                if g.user_id and g.user_info:
                    # Case 1: Already logged in. Just transfer the user to the correct place
                    return resp
                elif g.user_id and not g.user_info:
                    # Case 2: Access token expire, refresh the token
                    return redirect(url_for(url_refresh, next=next_point, **next_values))
                if login_token:
                    # A magic token token has been used
                    user_mail, hashed_passwd, _ = token_manager.parse_login_token(login_token)
                    if not user_mail:
                        return render_template(template_login, title="Login", msg="Invalid / Expired Login token")
                    try:
                        user_obj = user_manager.load(name=user_mail)
                    except XiaError as e:
                        return render_template(template_login, title="Login", msg=e.args[0])
                    if user_obj.hashed_passwd == hashed_passwd:
                        user_info = user_obj.get_display_data(catalog=user_obj._basic_catalog)
                        _set_user_token(resp, user_info, path_refresh)
                        return resp
                    else:
                        return render_template(template_login, title="Login", msg="Invalid / Expired Login token")
                return render_template(template_login, title="Login", msg="")

        @account.route('/signup', methods=["GET", "POST"])
        def signup():
            if request.method == "POST":
                path_refresh = url_for(url_refresh)
                user_mail, passwd, creator = request.form['email'], request.form['password'], request.remote_addr
                try:
                    user_obj = user_manager(name=user_mail, passwd=passwd).save()
                except XiaError as e:
                    return render_template(template_signup, title="Sign Up", msg=e.args[0])
                user_id = user_obj.user_id
                user_info = user_obj.get_basic(user_id).get_display_data()
                resp = redirect(url_for(home_path))
                # Logged in, should get user_info and acl now
                _set_user_token(resp, user_info, path_refresh)
                return resp
            else:
                if g.user_id:
                    # Already logged in
                    return redirect(url_for(home_path))
                return render_template(template_signup, title="Sign Up", msg="")

        @account.route('/refresh', methods=["GET"])
        def refresh():
            next_values = dict(request.args)
            next_point = next_values.pop('next', None)
            g.user_id, g.token_info = token_manager.parse_refresh_token()
            if not g.user_id:
                resp = redirect(url_for(url_login, next=next_point, **next_values))
                token_manager.remove_all_tokens(resp)
                return resp
            g.user_info = user_manager.get_basic(g.user_id).get_display_data()
            next_hoop = url_for(next_point, **next_values) if next_point else url_for(home_path)
            resp = redirect(next_hoop)
            # Logged in, should get user_info and acl now
            user_acl, user_app_info = _get_user_app_info(g.user_id, g.user_info)
            g.user_info["app_profile"] = user_app_info
            g.user_info["app_name"] = app_name
            token_manager.set_root_header_token(resp, g.user_info)
            token_manager.set_app_header_token(resp, app_name, app_info, user_app_info)
            token_manager.set_access_token(resp, g.user_id, user_acl, g.user_info, g.token_info)
            return resp

        @account.route('/refresh/<app_requested>', methods=["GET"])
        def sso(app_requested: str):
            state = request.args.get('state', "")  # Client defined state is saved here
            requested_callback = request.args.get('callback', "")  # Client requested callback url
            g.user_id, g.token_info = token_manager.parse_refresh_token()
            if not g.user_id:
                # Need login and then come back here
                resp = redirect(url_for(url_login, next=url_sso, app_requested=app_requested,
                                        state=state, callback=requested_callback))
                token_manager.remove_all_tokens(resp)
                return resp
            # Generate a callback url
            app_matrix = app_manager.load(name=app_requested)
            if not app_matrix:
                return f"No application {app_requested} found", 422  # No application found
            if not app_matrix.callback_urls:
                return f"No callback url defined for {app_requested}", 422  # No Call back url defined
            if not requested_callback:
                return f"Missing requested callback parameter in callback url", 422  # No requested callback
            callback_url = cls.get_callback_url(requested_callback, app_matrix.callback_urls)
            if not callback_url:
                return f"Current domain name is not registered as callback url", 422  # Source not registered
            # We will generate a token at user profile so that the target application will know the user has logged on
            sso_token = str(uuid.uuid1())
            user_role = profile_manager.load(user_name=g.user_id, app_name=app_requested)
            if not user_role:
                if app_matrix.new_user_roles:
                    # Create a new user for the application with the initial roles
                    profile_manager(user_name=g.user_id,
                                    app_name=app_requested,
                                    roles=app_matrix.new_user_roles,
                                    profile=app_matrix.new_user_profile,
                                    sso_token=sso_token).save()
                else:
                    return f"User {g.user_id} not found at the {app_requested}", 401
            else:
                user_role.update(sso_token=sso_token)
            cb_params = urlparse(callback_url)
            if not cb_params.scheme:  # Default to https scheme
                cb_params = urlparse("https://" + callback_url)
            resp = redirect(url_for(url_callback, scheme=cb_params.scheme, netloc=cb_params.netloc, path=cb_params.path,
                                    user=g.user_id, token=sso_token, state=state))
            # Append the new service into logout list
            logout_list_cookie = request.cookies.get(xia_logout_cookie)
            logout_list = [] if not logout_list_cookie else json.loads(base64.b64decode(logout_list_cookie).decode())
            logout_url = "/".join(callback_url.split("/")[:-1]) + "/logout"
            if logout_url not in logout_list:
                logout_list.append(logout_url)
            logout_list_cookie = base64.b64encode(json.dumps(logout_list).encode()).decode()
            resp.set_cookie(xia_logout_cookie, logout_list_cookie, max_age=2**25)
            return resp

        @account.route('/callback', methods=["GET"])
        def callback():
            scheme = request.args.get('scheme')
            netloc = request.args.get('netloc')
            path = request.args.get('path')
            if not path or not path.startswith("/sso/callback"):
                abort(400, "Callback path must starts with /sso/callback")
            query = urlencode({
                "user": request.args.get('user', ""),
                "token": request.args.get('token', ""),
                "state": request.args.get('state', "")
            })
            callback_endpoint = urlunparse((scheme, netloc, path, '', query, ''))
            return redirect(callback_endpoint)

        @account.route('/confirm', methods=["GET", "POST"])
        def confirm():
            resp = make_response(render_template(template_confirm, title="Confirm account", msg=""))
            if request.method == "POST":
                if g.user_id and g.user_info:
                    user_obj = user_manager.load(user_id=g.user_id)
                    # Confirm token should be refreshed only when 99% lifetime left
                    token_value = XiaLoginFlask.get_token_from_url(user_obj.confirm_link)
                    _, token_info = token_manager.parse_confirm_token(token_value)
                    token_life = (token_info.get("exp", 0) - datetime.now().timestamp())
                    if token_life < token_manager.CONFIRM_TOKEN_LIFETIME * 0.99:
                        confirm_token = token_manager.generate_confirm_token(g.user_id, {})
                        confirm_link = XiaLoginFlask.get_redirect_link(url_confirm, token=confirm_token)
                        user_obj.update(confirm_link=confirm_link)
                        if mail_sender and "account_confirm" in mail_sender.address_book:
                            mail_content = render_template(template_mail_account_confirm, confirm_link=confirm_link)
                            mail_sender.send_mail_plain("account_confirm", [g.user_id], "Account confirm", mail_content)
                    g.user_info["confirm_sent"] = True
                    # Regenerate resp because of changed user_info
                    resp = make_response(render_template(template_confirm, title="Confirm account", msg=""))
                    token_manager.set_root_header_token(resp, g.user_info)
                    token_manager.set_app_header_token(resp, app_name, app_info, g.user_info.get("app_profile", {}))
                    token_manager.set_access_token(resp, g.user_id, g.acl, g.user_info, g.token_info)
                    return resp
            else:
                # Try to confirm by using token
                token = request.args.get("token")
                if token:
                    # Case 1: Token is presented
                    user_id, _ = token_manager.parse_confirm_token(token)
                    if user_id:
                        try:
                            user_obj = user_manager.load(user_id=user_id)
                            if user_obj.confirm_time:
                                return resp
                            confirm_time = datetime.now().timestamp()
                            user_obj.update(confirm_time=confirm_time)
                        except user_manager as e:
                            return render_template(template_confirm, title="Confirm account", msg=e.args[0])
                        if g.user_info and g.user_id:
                            # When user is logged in, we need to update the access token
                            user_obj = user_manager.from_display(**g.user_info)
                            user_obj.confirm_time = confirm_time
                            g.user_info = user_obj.get_display_data(catalog=user_obj._basic_catalog)
                            user_acl, user_app_info = _get_user_app_info(g.user_id, g.user_info)
                            g.user_info["app_profile"] = user_app_info
                            g.user_info["app_name"] = app_name
                            token_manager.set_root_header_token(resp, g.user_info)
                            token_manager.set_app_header_token(resp, app_name, app_info, user_app_info)
                            token_manager.set_access_token(resp, g.user_id, g.acl, g.user_info, g.token_info)
                        return resp
                elif g.user_id and not g.user_info:
                    return redirect(url_for(url_refresh, next=g.endpoint, **g.values))
            return resp

        @account.route('/forgot', methods=["GET", "POST"])
        def forgot():
            if request.method == "POST":
                user_mail = request.form['email']
                try:
                    user_obj = user_manager.load(name=user_mail)
                    # Token should be refreshed only when 20% lifetime left
                    token_value = XiaLoginFlask.get_token_from_url(user_obj.login_link)
                    _, _, token_info = token_manager.parse_login_token(token_value)
                    token_life = (token_info.get("exp", 0) - datetime.now().timestamp())
                    if token_life < token_manager.LOGIN_TOKEN_LIFETIME * 0.2:
                        login_token = token_manager.generate_login_token(user_mail, user_obj.hashed_passwd, {})
                        login_link = XiaLoginFlask.get_redirect_link(url_login, token=login_token,
                                                                     next=url_reset)
                        user_obj.update(login_link=login_link)
                        if mail_sender and "password_reset" in mail_sender.address_book:
                            mail_content = render_template(template_mail_password_reset, login_link=login_link)
                            mail_sender.send_mail_plain("password_reset", [user_mail], "Password Reset", mail_content)
                except Exception:
                    """Catch all exception"""
                return render_template(template_forgot, title="Forgot Password", sent=True)
            else:
                return render_template(template_forgot, title="Forgot Password")

        @account.route('/reset', methods=["GET", "POST"])
        def reset():
            if not g.user_id and not g.user_info:
                return redirect(url_for(url_login, next=g.endpoint, **g.values))
            elif not g.user_info:
                return redirect(url_for(url_refresh, next=g.endpoint, **g.values))
            if request.method == "POST":
                new_password = request.form['password']
                user_obj = user_manager.load(user_id=g.user_id)
                try:
                    user_obj.change_passwd(new_password)
                except Exception as e:
                    return render_template(template_reset, title="Reset Password", msg=e.args[0])
                return redirect(url_for(home_path))
            else:
                return render_template(template_reset, title="Reset Password")

        @account.route('/logout')
        def logout():
            resp = make_response(render_template(template_logout, title="Logout"))
            token_manager.remove_all_tokens(resp)
            return resp

        if debug:
            @account.route('/debug', methods=["GET"])
            def debug():
                access_token = request.cookies.get(token_manager.ACCESS_TOKEN_NAME)
                refresh_token = request.cookies.get(token_manager.REFRESH_TOKEN_NAME)
                refresh_signal = request.cookies.get(token_manager.REFRESH_SIGNAL_NAME)
                _, _, _, access_token_info = token_manager.parse_access_token(access_token)
                _, refresh_token_info = token_manager.parse_refresh_token(refresh_token)
                _, refresh_signal_info = token_manager.parse_refresh_signal(refresh_signal)
                if request.remote_addr == "127.0.0.1" and g.user_id:  #: local test
                    confirm_token = token_manager.generate_confirm_token(g.user_id, {})
                    user_obj = user_manager.load(user_id=g.user_id)
                    login_token = token_manager.generate_login_token(g.user_id, user_obj.hashed_passwd, {})
                else:
                    confirm_token, login_token = None, None

                g_context = {}
                for key in [k for k in g.__dir__() if not k.startswith("_")]:
                    value = getattr(g, key)
                    if not callable(value):
                        g_context[key] = str(getattr(g, key))

                return jsonify({
                    "current_fqdn": token_manager.get_origin_fqdn(),
                    "current_root_domain": token_manager.get_root_domain(),
                    "root_header_token": request.cookies.get(token_manager.ROOT_HEADER_TOKEN_NAME),
                    "access_token": access_token_info,
                    "refresh_token": refresh_token_info,
                    "refresh_signal": refresh_signal_info,
                    "confirm_link": XiaLoginFlask.get_redirect_link(url_confirm, token=confirm_token),
                    "login_link": XiaLoginFlask.get_redirect_link(url_login, token=login_token, next=url_reset),
                    "context": g_context
                })
        return account
