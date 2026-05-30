from celonis_support_utils.cli import main


def test_cli_route_command_default_strategy():
    result = main(["route", "T-001"])
    assert result == 0


def test_cli_route_command_escalation_strategy():
    result = main(["route", "T-002", "--strategy", "escalation"])
    assert result == 1
