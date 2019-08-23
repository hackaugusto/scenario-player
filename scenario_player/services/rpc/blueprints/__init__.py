import pluggy

from scenario_player.constants import HOST_NAMESPACE
from scenario_player.services.rpc.blueprints.instances import instances_blueprint
from scenario_player.services.rpc.blueprints.tokens import tokens_blueprint
from scenario_player.services.rpc.blueprints.transactions import transactions_blueprint
from scenario_player.services.rpc.utils import RPCRegistry

__all__ = ["transactions_blueprint", "instances_blueprint", "tokens_blueprint"]


HOOK_IMPL = pluggy.HookimplMarker(HOST_NAMESPACE)


@HOOK_IMPL
def register_blueprints(app):
    app.config["rpc-client"] = RPCRegistry()
    for bp in (transactions_blueprint, instances_blueprint, tokens_blueprint):
        app.register_blueprint(bp)
