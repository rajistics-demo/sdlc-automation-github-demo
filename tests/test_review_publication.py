"""Exercise publication retries and lost responses without network writes."""
import importlib.util
from pathlib import Path

import pytest

path = Path(__file__).resolve().parents[1] / "scripts/automations/publish_review_comment.py"
spec = importlib.util.spec_from_file_location("review_publication", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
URL = "https://example.test/conversations/synthetic-review"
BODY = "No blocking findings.\nOpenHands conversation: " + URL


class GitHub:
    def __init__(self):
        self.comments = []
        self.posts = 0
        self.lose_response = False
        self.commit_post = True

    def request(self, method, path, payload=None):
        if method == "GET":
            page = int(path.rsplit("page=", 1)[1])
            return self.comments[(page - 1) * 100:page * 100]
        assert method == "POST"
        self.posts += 1
        result = {"id": len(self.comments) + 1, "html_url": "https://github.com/example/demo/issues/1#issuecomment-1", **payload}
        if self.commit_post:
            self.comments.append(result)
        if self.lose_response:
            raise TimeoutError("synthetic lost response")
        return result


def publish(api, tmp_path, body=BODY):
    return module.publish("example/demo", 1, body, URL, tmp_path, api.request)


def test_repeated_verification_does_not_create_second_comment(tmp_path):
    api = GitHub()
    assert publish(api, tmp_path)["status"] == "published_verified"
    assert publish(api, tmp_path)["status"] == "existing_verified"
    assert api.posts == 1


def test_lost_response_is_reconciled_with_read_only_retry(tmp_path):
    api = GitHub()
    api.lose_response = True
    with pytest.raises(TimeoutError):
        publish(api, tmp_path)
    assert publish(api, tmp_path)["status"] == "existing_verified"
    assert api.posts == 1


def test_unresolved_attempt_is_not_reposted(tmp_path):
    api = GitHub()
    api.lose_response = True
    api.commit_post = False
    with pytest.raises(TimeoutError):
        publish(api, tmp_path)
    with pytest.raises(RuntimeError, match="unresolved"):
        publish(api, tmp_path)
    assert api.posts == 1


def test_changed_body_does_not_edit_or_repost(tmp_path):
    api = GitHub()
    publish(api, tmp_path)
    with pytest.raises(RuntimeError, match="differs"):
        publish(api, tmp_path, "Changed finding.\n" + BODY)
    assert api.posts == 1


def test_reconciliation_reads_later_pages(tmp_path):
    api = GitHub()
    publish(api, tmp_path)
    api.comments = [{"body": "unrelated"}] * 100 + api.comments
    assert publish(api, tmp_path)["status"] == "existing_verified"
    assert api.posts == 1


def test_existing_comment_without_helper_marker_is_not_duplicated(tmp_path):
    api = GitHub()
    api.comments = [{"id": 1, "body": BODY, "html_url": "https://github.com/example/demo/issues/1#issuecomment-1"}]
    assert publish(api, tmp_path)["status"] == "existing_verified"
    assert api.posts == 0


def test_existing_duplicates_stop_without_another_write(tmp_path):
    api = GitHub()
    publish(api, tmp_path)
    api.comments *= 2
    with pytest.raises(RuntimeError, match="Multiple"):
        publish(api, tmp_path)
    assert api.posts == 1


@pytest.mark.parametrize("body", [BODY + "\n<url>", BODY + "\nPLACEHOLDER_URL", BODY + "\n${AUTOMATION_SESSION_URL}"])
def test_placeholder_body_is_not_published(tmp_path, body):
    api = GitHub()
    with pytest.raises(ValueError, match="placeholders"):
        publish(api, tmp_path, body)
    assert api.posts == 0
