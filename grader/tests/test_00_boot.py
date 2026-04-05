from grader.conftest import reset_system, wait_for_system


def test_system_boot():
    wait_for_system()
    reset_system()
