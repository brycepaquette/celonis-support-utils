from celonis_support_utils.notification_sender import SlackSender


def test_slack_sender_sends_message(mocker):
    mock_post = mocker.patch("celonis_support_utils.notification_sender.requests.post")
    sender = SlackSender(
        webhook_url="https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
    )
    sender.send(message="Test message")
    mock_post.assert_called_once_with(
        "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX",
        json={"text": "Test message"},
    )
