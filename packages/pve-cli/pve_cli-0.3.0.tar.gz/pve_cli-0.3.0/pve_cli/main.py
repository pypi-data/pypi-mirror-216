from pathlib import Path
from typing import Optional

import typer
from typing_extensions import Annotated

from . import __version__, __metadata__
from .guest_cmd import guest_cli
from .nodes_cmd import nodes_cli
from .proxmox import Proxmox
from .proxmox.exceptions import ProxmoxConnectionError
from .util.callbacks import config_callback, version_callback
from .util.exceptions import PVECLIError
from .util.validators import validate_cluster

HELP = f"""{__metadata__["Name"]} {__version__}

{__metadata__["Summary"]}
"""

cli = typer.Typer(help=HELP)
cli.add_typer(guest_cli, name='guest', help='Guest-agent commands')
cli.add_typer(nodes_cli, name='nodes', help='Node commands')


@cli.callback(context_settings={'help_option_names': ['-h', '--help'], 'max_content_width': 120})
def main(
        ctx: typer.Context,
        cluster: Annotated[str, typer.Option('--cluster', '-C', callback=validate_cluster,
                                             help='Cluster from config to connect to.')] = '',
        _version: Annotated[Optional[bool], typer.Option('--version', '-V', callback=version_callback, is_eager=True,
                                                         expose_value=False, help='Print version and exit')] = None,
        _configfile_path: Annotated[Path, typer.Option('--config', '-c', encoding='utf-8', callback=config_callback,
                                                       is_eager=True, expose_value=False, help='Config file path')]
        = Path(typer.get_app_dir('pve-cli')) / 'config.toml'
):
    ctx.obj['cluster'] = cluster
    config = ctx.obj['config']
    cluster_config = config['clusters'][cluster]

    try:
        proxmox_api = Proxmox(**cluster_config)
    except ProxmoxConnectionError as exc:
        raise PVECLIError(str(exc))

    ctx.ensure_object(dict)
    ctx.obj['proxmox_api'] = proxmox_api
