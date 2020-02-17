from typing import List
from unittest.mock import Mock

from pipeliner.steps_factory import StepsFactory
from pipeliner.steps import CompareWithPrevious, Step, DoNothing, ProduceText, GetHtmlElement, GetHtmlElementText, HttpDownload, PickRandomText


class CompareWithPreviousStepsFactory(StepsFactory):
    def __init__(self):
        self.when_same = DoNothing()
        self.when_different = ProduceText("Hello test!")

    def create(self, steps_config: list) -> List[Step]:
        return []

    def create_step(self, step_config: dict) -> Step:
        if step_config["type"] == "when_same":
            return self.when_same
        elif step_config["type"] == "when_different":
            return self.when_different


def test_compare_with_previous(mocker):
    factory = CompareWithPreviousStepsFactory()
    when_same = mocker.spy(factory.when_same, "perform")
    when_different = mocker.spy(factory.when_different, "perform")

    step = CompareWithPrevious(factory, {"type": "when_same"}, {"type": "when_different"})
    step.perform("Hello test!")
    step.perform("Hello test!")
    step.perform("Hello test!")
    step.perform("Hello different!")
    step.perform("Hello different again!")

    when_same.assert_has_calls([
        mocker.call("Hello test!"),
        mocker.call("Hello test!")
    ])
    when_different.assert_has_calls([
        mocker.call("Hello different!"),
        mocker.call("Hello different again!")
    ])


def test_get_html_element():
    html = "<html><head></head><body><h1>Title with <a href=\"#url\">link</a></h1></body></html>"
    step = GetHtmlElement("//html/body/h1")
    element = step.perform(html)
    assert element == "<h1>Title with <a href=\"#url\">link</a>\n</h1>\n"


def test_get_html_element_text():
    html = "<html><head></head><body><h1>Title with <a href=\"#url\">link</a></h1></body></html>"
    step = GetHtmlElementText("//html/body/h1/a")
    element_text = step.perform(html)
    assert element_text == "link"


def test_http_download(mocker):
    requests_get = mocker.patch("requests.get")
    requests_get.return_value = Mock()
    requests_get.return_value.content = "Downloaded content"

    step = HttpDownload("http://whatever.com/", dict())
    assert step.perform(None) == "Downloaded content"


def test_make_text_data():
    step = ProduceText("Hello test!")
    assert step.perform(None) == "Hello test!"


def test_pick_random_text(mocker):
    mocker.patch("random.choice", lambda *args: "Hello there!")
    step = PickRandomText([])
    assert step.perform(None) == "Hello there!"
