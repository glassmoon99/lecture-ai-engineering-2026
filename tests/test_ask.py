from types import SimpleNamespace

from app import ask


def test_main_reuses_chat_for_follow_up_questions(monkeypatch, capsys):
    class FakeChat:
        def __init__(self):
            self.questions = []

        def send_message(self, question):
            self.questions.append(question)
            return SimpleNamespace(
                usage_metadata=SimpleNamespace(
                    prompt_token_count=12, candidates_token_count=8
                ),
                text=f"回答: {question}",
            )

    chat = FakeChat()
    chat_creations = []

    class FakeClient:
        def __init__(self, api_key):
            self.chats = SimpleNamespace(
                create=lambda **kwargs: chat_creations.append(kwargs) or chat
            )

    monkeypatch.setattr(ask.genai, "Client", FakeClient)
    monkeypatch.setattr(ask, "get_api_key", lambda: "test-key")
    monkeypatch.setattr("sys.argv", ["app.ask", "最初の質問"])
    questions = iter(["続けて質問", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(questions))

    ask.main()

    output = capsys.readouterr().out
    assert chat_creations == [{"model": ask.MODEL}]
    assert chat.questions == ["最初の質問", "続けて質問"]
    assert "回答: 最初の質問" in output
    assert "回答: 続けて質問" in output
    assert output.count("[usage] 入力: 12 tokens / 出力: 8 tokens") == 2


def test_ask_prints_input_and_output_token_counts(monkeypatch, capsys):
    response = SimpleNamespace(
        usage_metadata=SimpleNamespace(prompt_token_count=12, candidates_token_count=8),
        text="回答",
    )

    class FakeClient:
        def __init__(self, api_key):
            self.models = SimpleNamespace(generate_content=lambda **kwargs: response)

    monkeypatch.setattr(ask.genai, "Client", FakeClient)
    monkeypatch.setattr(ask, "get_api_key", lambda: "test-key")

    assert ask.ask("質問") == "回答"
    assert "[usage] 入力: 12 tokens / 出力: 8 tokens" in capsys.readouterr().out