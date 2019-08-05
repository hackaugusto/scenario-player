from unittest import mock

import pytest

from scenario_player.constants import GAS_STRATEGIES
from scenario_player.services.rpc.utils import RPCRegistry, generate_hash_key
from scenario_player.services.utils.factories import construct_flask_app


@pytest.fixture
def default_create_rpc_instance_request_parameters():
    return {
        "chain_url": "https://test.net",
        "privkey": "my-private-key",
        "gas_price_strategy": "fast",
    }


@pytest.fixture
def deserialized_create_rpc_instance_request_parameters(
    default_create_rpc_instance_request_parameters
):
    deserialized = dict(default_create_rpc_instance_request_parameters)
    deserialized["privkey"] = deserialized["privkey"].encode("UTF-8")
    return deserialized


@pytest.fixture
def default_send_tx_request_parameters(rpc_client_id):
    """Default required request parameters for a POST request to /transactions."""
    parameters = {"client_id": rpc_client_id, "to": "someaddress", "value": 123.0, "startgas": 2.0}
    return parameters


@pytest.fixture
def deserialized_send_tx_request_parameters(
    default_send_tx_request_parameters, transaction_service_app
):
    deserialized = dict(default_send_tx_request_parameters)
    deserialized["to"] = deserialized["to"].encode("UTF-8")
    deserialized["client"] = transaction_service_app.config["rpc-client"][
        default_send_tx_request_parameters["client_id"]
    ]
    return deserialized


@pytest.fixture
def default_send_tx_func_parameters(deserialized_send_tx_request_parameters):
    args = dict(deserialized_send_tx_request_parameters)
    args.pop("client_id", None), args.pop("client", None)
    return args


@pytest.fixture
def rpc_client_id(deserialized_create_rpc_instance_request_parameters):
    params = deserialized_create_rpc_instance_request_parameters
    return generate_hash_key(params["chain_url"], params["privkey"], GAS_STRATEGIES["FAST"])


@pytest.fixture
def transaction_service_app(rpc_client_id):
    app = construct_flask_app()
    app.config["TESTING"] = True
    app.config["rpc-client"] = RPCRegistry()
    app.config["rpc-client"].dict = {
        rpc_client_id: mock.Mock(
            client_id=rpc_client_id, **{"send_transaction.return_value": b"my_tx_hash"}
        )
    }
    return app


@pytest.fixture
def transaction_service_client(transaction_service_app):
    return transaction_service_app.test_client()
