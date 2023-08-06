from __future__ import annotations

import typing

import yaml
from pydantic import ValidationError

from slingshot import schemas
from slingshot.sdk.config import client_settings
from slingshot.sdk.errors import SlingshotException


def load_slingshot_project_config() -> schemas.ProjectManifest:
    try:
        text = client_settings.slingshot_config_path.read_text()
    except FileNotFoundError as e:
        raise SlingshotException(
            f"Could not find slingshot.yaml at {client_settings.slingshot_config_path}.\n"
            f"You can add one by running 'slingshot init'"
        ) from e
    try:
        d = yaml.safe_load(text)
    except yaml.YAMLError as e:
        raise SlingshotException(f"Could not parse slingshot.yaml in {client_settings.slingshot_config_path}") from e
    if not d:
        raise SlingshotException(
            f"Empty slingshot.yaml in {client_settings.slingshot_config_path}. Please run 'slingshot init'"
        )
    try:
        return schemas.ProjectManifest.parse_obj(d)
    except Exception as e:
        raise _beautify_project_manifest_parsing_exception(d, e) from e


def _beautify_project_manifest_parsing_exception(d: dict[typing.Any, typing.Any], e: Exception) -> SlingshotException:
    if (isinstance(e, ValidationError) or isinstance(e, KeyError)) and "environments" in str(e):
        for env in d["environments"].values():
            try:
                # Try to parse each environment individually to get a more helpful error message,
                #  if it's one of them that's failing.
                schemas.EnvironmentSpec.parse_obj(env)
            except ValidationError as e2:
                model = e2.model.__name__
                errs = e2.errors()
                if len(errs) > 0:
                    message = None
                    # noinspection PyBroadException
                    try:
                        given = errs[0]["ctx"]["given"]
                        permitted = ', '.join(list(errs[0]["ctx"]["permitted"]))
                        message = (
                            f"Invalid slingshot.yaml: [yellow]{model}[/yellow] has \"{given}\" (must be one of "
                            f"{permitted}). Contact slingshot support for assistance."
                        )
                    except Exception:
                        # If we fail to produce a valid friendly error, prefer to fall back to the generic error.
                        pass
                    if message:
                        return SlingshotException(message)

    return SlingshotException(f"Invalid slingshot.yaml: {e=}")


T = typing.TypeVar("T")


class ResponseProtocol(typing.Protocol[T]):
    data: typing.Optional[T]
    error: typing.Optional[schemas.SlingshotLogicalError]


def get_data_or_raise(resp: ResponseProtocol[T]) -> T:
    if resp.error:
        raise SlingshotException(resp.error.message)
    if resp.data is None:
        raise SlingshotException("No data returned from server")
    return resp.data
