import uuid
import json
import base64
from urllib.parse import urlparse
from typing import Type
from datetime import datetime
from flask import Blueprint, Response, request, g, jsonify, url_for, redirect, render_template, make_response, abort
from xia_engine import XiaError, Acl
from xia_token_flask import FlaskToken
from xia_engine_rest import RestEngine
from xia_user import User, UserRoles, RoleMatrix


class XiaSsoFlask:
    """XIA Login SSO Module for Flask

    Logged in status:
        * all user related information was retrieved by cookies.
        * g.user_id: User Mail Address
        * g.user_info: A dictionary holds the user related information
        * g.acl: A dictionary holds the User's permissions for all requested applications.
    """
    @classmethod
    def get_sso_blueprint(
            cls, /,
            home_path: str,
            token_manager: Type[FlaskToken],
            refresh_path: str,
            role_manager: Type[UserRoles],
            matrix_manager: Type[RoleMatrix],
            user_manager: Type[User] = None,
            app_name: str = "",
            sso_provider_url: str = "",
            token_life: int = 120,
            debug: bool = False,
    ):
        """Get SSO Management Blueprint

        Args:
            home_path: homepage path of flask, like "/"
            token_manager: Token Management Class, should be a subclass of FlaskToken
            refresh_path: From which path could the access token be refreshed
            role_manager: Role Management
            matrix_manager: Role Matrix Management, will be used for permission detail
            user_manager: User Management, only need to be assigned if want to get user's other information
            app_name: The profile of which app should be retrieved
            sso_provider_url: The XIA sso provider location
            token_life: SSO token will expire in specified seconds
            debug: Generate debug page: Weather the program should generate a debug endpoint

        Returns:
            Flask blueprint
        """
        sso = Blueprint('sso', __name__)

        def get_sso_url(next_point: str, **kwargs):
            kwargs["next"] = next_point
            state = base64.urlsafe_b64encode(json.dumps(kwargs).encode()).decode()
            return sso_provider_url + "?state=" + state + "&callback=" + token_manager.get_origin_fqdn()

        @sso.route('/provider', methods=["GET"])
        def provider():
            state = request.args.get("state", "")
            sso_url = sso_provider_url + "?state=" + state + "&callback=" + token_manager.get_origin_fqdn()
            resp = redirect(sso_url)
            return resp

        @sso.route('/refresh', methods=["GET"])
        def refresh():
            next_values = dict(request.args)
            next_point = next_values.pop('next', None)
            g.user_id, g.token_info = token_manager.parse_refresh_token()
            if not g.user_id:
                # Go for SSO process
                resp = redirect(get_sso_url(next_point, **next_values))
                return resp
            # Find refresh token so refresh locally access token
            g.user_info = {"user_name": g.user_id}
            next_hoop = url_for(next_point, **next_values) if next_point else home_path
            resp = redirect(next_hoop)
            # Logged in, should get user_info and acl now
            user_role = role_manager.load(user_name=g.user_id, app_name=app_name)
            user_app_info = user_role.get_user_acl()
            user_acl = user_app_info.acl
            g.user_info["app_name"] = app_name
            g.user_info["app_profile"] = user_app_info.user_profile
            token_manager.set_app_header_token(resp, app_name, {}, g.user_info.get("app_profile", {}))
            token_manager.set_access_token(resp, g.user_id, user_acl, g.user_info, g.token_info)
            return resp

        @sso.route('/callback', methods=["GET", "POST"])
        def callback():
            user_id = request.args.get("user", "")
            token = request.args.get("token", "")
            state = request.args.get("state", "")
            if not user_id or not token:
                return "Missing User ID or SSO Token in callback request", 400
            try:
                id_content = uuid.UUID(token)
            except AttributeError:
                return "Wrong SSO Token Format", 400
            if (uuid.uuid1().time - id_content.time) / 10 ** 7 > token_life:
                return "Token has expired", 400
            user_role = role_manager.load(user_name=user_id, app_name=app_name, sso_token=token)
            if not user_role:
                return "Invalid Token", 400
            user_app_info = user_role.get_user_acl()
            user_acl = user_app_info.acl
            if user_manager:
                user_obj = user_manager.load(user_id=user_id)
                if not user_obj:
                    return "Application has no authorization to retrieve your personal data", 500
                user_info = {k: v for k, v in user_obj.get_display_data().items() if k in user_role.user_fields}
                user_info.update(user_app_info.user_profile)   # Application specific user data overwrite user data
                user_app_info.user_profile.update(user_info)   # Integrate user info into user profile
            user_info = {"user_name": user_id, "app_name": app_name, "app_profile": user_app_info.user_profile}
            resp = redirect(home_path)
            token_manager.active_root_header_token(resp)
            token_manager.set_app_header_token(resp, app_name, {}, user_app_info.user_profile)
            token_manager.set_access_token(resp, user_id, user_acl, user_info, {"root": refresh_path})
            token_manager.set_refresh_token(resp, user_id, {"root": refresh_path})
            return resp

        @sso.route('/logout')
        def logout():
            resp = make_response("Logged out")
            token_manager.remove_all_tokens(resp)
            return resp

        if debug:
            @sso.route('/debug', methods=["GET"])
            def debug():
                access_token = request.cookies.get(token_manager.ACCESS_TOKEN_NAME)
                refresh_token = request.cookies.get(token_manager.REFRESH_TOKEN_NAME)
                refresh_signal = request.cookies.get(token_manager.REFRESH_SIGNAL_NAME)
                _, _, _, access_token_info = token_manager.parse_access_token(access_token)
                _, refresh_token_info = token_manager.parse_refresh_token(refresh_token)
                _, refresh_signal_info = token_manager.parse_refresh_signal(refresh_signal)
                return jsonify({
                    "current_fqdn": token_manager.get_origin_fqdn(),
                    "current_root_domain": token_manager.get_root_domain(),
                    "root_header_token": request.cookies.get(token_manager.ROOT_HEADER_TOKEN_NAME),
                    "app_header_token": request.cookies.get(token_manager.APP_HEADER_TOKEN_NAME),
                    "request_header": dict(request.headers),
                    "sso_provider_url": sso_provider_url,
                    "request_url_root": request.headers.get("X-Forwarded-Host", token_manager.get_origin_fqdn()),
                    "request_host_header": request.headers.get("Host", ""),
                    "access_token": access_token_info,
                    "refresh_token": refresh_token_info,
                    "refresh_signal": refresh_signal_info,
                })

        return sso
