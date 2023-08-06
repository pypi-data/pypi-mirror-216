import typing

import httpx
import typer

from neosctl import constant, util
from neosctl.services.iam import schema
from neosctl.util import process_response

app = typer.Typer()


def _iam_url(iam_api_url: str, postfix: str = "") -> str:
    return "{}/{}".format(iam_api_url.rstrip("/"), postfix)


@app.command(name="list")
def list_policies(
    ctx: typer.Context,
    page: int = typer.Option(1, help="Page number."),
    page_size: int = typer.Option(10, help="Page size number."),
    resource: typing.Optional[str] = typer.Option(None, help="Resource nrn.", callback=util.sanitize),
) -> None:
    """List existing policies."""

    @util.ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        params: typing.Dict[str, typing.Union[int, str]] = {"page": page, "page_size": page_size}  # noqa: FA100
        if resource:
            params["resource"] = resource

        return util.get(
            ctx,
            _iam_url(ctx.obj.get_iam_api_url(), "policy/users"),
            params=params,
        )

    r = _request(ctx)
    process_response(r)


@app.command(name="create")
def create_from_json(
    ctx: typer.Context,
    filepath: str = typer.Argument(..., help="Filepath of the user policy json payload", callback=util.sanitize),
) -> None:
    """Create an IAM policy."""

    @util.ensure_login
    def _request(ctx: typer.Context, user_policy: schema.UserPolicy) -> httpx.Response:
        return util.post(
            ctx,
            "{iam_url}".format(iam_url=_iam_url(ctx.obj.get_iam_api_url(), "policy/user")),
            json=user_policy.dict(),
        )

    fp = util.get_file_location(filepath)
    user_policy_payload = util.load_json_file(fp, "policy")

    user_policy = schema.UserPolicy(**user_policy_payload)  # type: ignore[reportGeneralTypeIssues]

    r = _request(ctx, user_policy)
    process_response(r)


@app.command(name="update")
def update_from_json(
    ctx: typer.Context,
    principal: str = typer.Argument(..., help="Principal uuid", callback=util.sanitize),
    filepath: str = typer.Argument(..., help="Filepath of the user policy json payload", callback=util.sanitize),
) -> None:
    """Update an existing IAM policy."""

    @util.ensure_login
    def _request(ctx: typer.Context, user_policy: schema.UserPolicy) -> httpx.Response:
        return util.put(
            ctx,
            "{iam_url}".format(iam_url=_iam_url(ctx.obj.get_iam_api_url(), "policy/user")),
            params={"user_nrn": principal},
            json=user_policy.dict(),
        )

    fp = util.get_file_location(filepath)
    user_policy_payload = util.load_json_file(fp, "policy")

    user_policy = schema.UserPolicy(**user_policy_payload)  # type: ignore[reportGeneralTypeIssues]

    r = _request(ctx, user_policy)
    process_response(r)


@app.command()
def delete(
    ctx: typer.Context,
    user_nrn: str = typer.Argument(..., callback=util.sanitize),
) -> None:
    """Delete an existing IAM policy."""

    @util.ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.delete(
            ctx,
            "{iam_url}".format(iam_url=_iam_url(ctx.obj.get_iam_api_url(), "policy/user")),
            params={"user_nrn": user_nrn},
        )

    r = _request(ctx)
    process_response(r)


@app.command()
def get(
    ctx: typer.Context,
    user_nrn: str = typer.Argument(..., callback=util.sanitize),
) -> None:
    """Get an existing IAM policy."""

    @util.ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.get(
            ctx,
            "{iam_url}".format(iam_url=_iam_url(ctx.obj.get_iam_api_url(), "policy/user")),
            params={"user_nrn": user_nrn},
        )

    r = _request(ctx)
    process_response(r)


@app.command(name="list-users")
def list_users(
    ctx: typer.Context,
    search: str = typer.Option(None, help="Search term", callback=util.sanitize),
) -> None:
    """List existing keycloak users.

    Filter by search term on username, first_name, last_name, or email.
    """

    @util.ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.get(
            ctx,
            _iam_url(ctx.obj.get_iam_api_url(), "users"),
            params={"search": search} if search else None,
        )

    r = _request(ctx)
    process_response(r)


@app.command(name="user-permissions")
def user_permissions(
    ctx: typer.Context,
    username: str = typer.Argument(..., help="Keycloak username", callback=util.sanitize),
) -> None:
    """List existing keycloak user permissions."""

    @util.ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        r = util.get(
            ctx,
            _iam_url(ctx.obj.get_iam_api_url(), "users"),
            params={"search": username},
        )
        if r.status_code >= constant.BAD_REQUEST_CODE:
            process_response(r)

        data = r.json()
        # In case search term matches email/name of another user, filter for specific username
        user_id = next((user["id"] for user in data["users"] if user["username"] == username), None)

        if user_id is None:
            typer.echo("User not found.")
            raise typer.Exit(code=1)

        return util.get(
            ctx,
            "{iam_url}".format(iam_url=_iam_url(ctx.obj.get_iam_api_url(), "policy/user")),
            params={"user_nrn": user_id},
        )

    r = _request(ctx)
    process_response(r)
