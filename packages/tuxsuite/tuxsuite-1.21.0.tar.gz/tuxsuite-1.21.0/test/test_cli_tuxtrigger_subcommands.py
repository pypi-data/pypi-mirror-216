# -*- coding: utf-8 -*-
import os
import sys
import pytest
import json
import yaml
import tuxsuite
from unittest.mock import patch


def test_load_yaml(plan_config, sample_plan_config, capsys):
    from tuxsuite.cli.tuxtrigger import load_yaml

    # try to load a yaml file
    _, data = load_yaml(plan_config)

    assert data == yaml.safe_load(sample_plan_config)

    # FileNotFoundError
    with pytest.raises(tuxsuite.exceptions.InvalidConfiguration):
        load_yaml("/tmp/path/test")

    # other exception
    with patch("yaml.safe_load", side_effect=Exception("error")):
        with pytest.raises(SystemExit):
            load_yaml(plan_config)
        output, error = capsys.readouterr()
        assert "Error: Invalid plan file: error" in error


def test_tuxtrigger_handle_add(
    mocker, config, response, monkeypatch, capsys, plan_config
):
    # without config and plan
    monkeypatch.setattr(sys, "argv", ["tuxsuite", "tuxtrigger", "add"])
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()

    output, error = capsys.readouterr()
    assert "Either config or plan must be provided" in error
    assert exc_info.value.code == 1

    # happy flow with config only
    mocker.resetall()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "tuxsuite",
            "tuxtrigger",
            "add",
            "--config",
            str(plan_config),
        ],
    )
    response.status_code = 201
    response._content = json.dumps({}).encode("utf-8")
    post_req = mocker.patch("requests.post", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "Tuxtrigger 'config/plan' files added\n" == output
    assert post_req.call_count == 1
    assert exc_info.value.code == 0

    # happy flow with plan only
    mocker.resetall()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "tuxsuite",
            "tuxtrigger",
            "add",
            "--plan",
            str(plan_config),
        ],
    )
    response.status_code = 201
    response._content = json.dumps({}).encode("utf-8")
    post_req = mocker.patch("requests.post", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "Tuxtrigger 'config/plan' files added\n" == output
    assert post_req.call_count == 1
    assert exc_info.value.code == 0

    # happy flow with plan directory
    plan_dir = os.path.dirname(str(plan_config))
    mocker.resetall()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "tuxsuite",
            "tuxtrigger",
            "add",
            "--plan",
            plan_dir,
        ],
    )
    response.status_code = 201
    response._content = json.dumps({}).encode("utf-8")
    post_req = mocker.patch("requests.post", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "Tuxtrigger 'config/plan' files added\n" == output
    assert post_req.call_count == 1
    assert exc_info.value.code == 0

    # failed request
    mocker.resetall()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "tuxsuite",
            "tuxtrigger",
            "add",
            "--config",
            str(plan_config),
            "--plan",
            str(plan_config),
        ],
    )
    response.status_code = 400
    response._content = json.dumps({}).encode("utf-8")
    post_req = mocker.patch("requests.post", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "Error: Failed to add tuxtrigger 'config/plan'\n" == error
    assert post_req.call_count == 1
    assert exc_info.value.code == 1


def test_tuxtrigger_handle_delete(
    mocker, plan_config, config, response, monkeypatch, capsys
):
    # without config and plan
    monkeypatch.setattr(sys, "argv", ["tuxsuite", "tuxtrigger", "delete"])
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()

    output, error = capsys.readouterr()
    assert "Either config or plan must be provided for deletion" in error
    assert exc_info.value.code == 1

    # happy flow with config only
    mocker.resetall()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "tuxsuite",
            "tuxtrigger",
            "delete",
            "--config",
        ],
    )
    response.status_code = 200
    response._content = {}
    post_req = mocker.patch("requests.delete", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "Config: config.yaml file deleted\n" == output
    assert post_req.call_count == 1
    assert exc_info.value.code == 0

    # happy flow with plan only
    mocker.resetall()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "tuxsuite",
            "tuxtrigger",
            "delete",
            "--plan",
            "test-plan-1",
            "--plan",
            "test-plan-2",
        ],
    )
    response.status_code = 200
    response._content = {}
    post_req = mocker.patch("requests.delete", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "Plan: test-plan-1,test-plan-2 file deleted\n" == output
    assert post_req.call_count == 1
    assert exc_info.value.code == 0

    # happy flow with config and plan
    mocker.resetall()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "tuxsuite",
            "tuxtrigger",
            "delete",
            "--config",
            "--plan",
            "test-plan",
        ],
    )
    response.status_code = 200
    response._content = {}
    post_req = mocker.patch("requests.delete", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "Config: config.yaml Plan: test-plan file deleted\n" == output
    assert post_req.call_count == 1
    assert exc_info.value.code == 0

    # failed request
    mocker.resetall()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "tuxsuite",
            "tuxtrigger",
            "delete",
            "--config",
            "--plan",
            "planv1.yaml",
        ],
    )
    response.status_code = 400
    response._content = {}
    post_req = mocker.patch("requests.delete", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert (
        "Error: Failed to delete Config: config.yaml Plan: planv1.yaml file\n" == error
    )
    assert post_req.call_count == 1
    assert exc_info.value.code == 1


def test_tuxtrigger_handle_get(
    mocker, sample_plan_config, config, response, monkeypatch, capsys
):
    # without config and plan
    monkeypatch.setattr(sys, "argv", ["tuxsuite", "tuxtrigger", "get"])
    response.status_code = 200
    ret = {"config": "config.yaml", "plans": ["plan1", "plan2"]}
    response._content = json.dumps(ret).encode("utf-8")
    get_req = mocker.patch("requests.get", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "Tuxtrigger config:" in output
    assert exc_info.value.code == 0
    assert get_req.call_count == 1

    # with config
    monkeypatch.setattr(sys, "argv", ["tuxsuite", "tuxtrigger", "get", "--config"])
    response.status_code = 200
    ret = {"config": sample_plan_config}
    response._content = json.dumps(ret).encode("utf-8")
    get_req = mocker.patch("requests.get", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "Tuxtrigger config: config.yaml" in output
    assert exc_info.value.code == 0
    assert get_req.call_count == 1

    # with plan
    monkeypatch.setattr(
        sys, "argv", ["tuxsuite", "tuxtrigger", "get", "--plan", "test-plan"]
    )
    response.status_code = 200
    ret = {"plan": sample_plan_config}
    response._content = json.dumps(ret).encode("utf-8")
    get_req = mocker.patch("requests.get", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "Tuxtrigger plan: test-plan" in output
    assert exc_info.value.code == 0
    assert get_req.call_count == 1

    # with config and plan
    monkeypatch.setattr(
        sys,
        "argv",
        ["tuxsuite", "tuxtrigger", "get", "--config", "--plan", "test-plan"],
    )
    response.status_code = 200
    ret = {"config": "config.yaml", "plans": ["plan1", "plan2"]}
    response._content = json.dumps(ret).encode("utf-8")
    get_req = mocker.patch("requests.get", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "--plan: not allowed with argument --config" in error
    assert exc_info.value.code == 2
    assert get_req.call_count == 0

    # Test failure case when the response is not 200
    monkeypatch.setattr(sys, "argv", ["tuxsuite", "tuxtrigger", "get"])
    response.status_code = 400
    response._content = {}
    get_req = mocker.patch("requests.get", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    assert get_req.call_count == 1
    assert exc_info.value.code == 1
    output, error = capsys.readouterr()
    assert (
        "Error: Failed to get the tuxtrigger config/plan. Is config/plan exists! ?\n"
        == error
    )
