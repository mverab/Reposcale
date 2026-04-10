from workers.executor import execute_task


def test_process_data_succeeds():
    assert execute_task("process_data", {}) is True


def test_send_email_needs_recipient():
    assert execute_task("send_email", {}) is False
    assert execute_task("send_email", {"to": "a@b.com"}) is True
