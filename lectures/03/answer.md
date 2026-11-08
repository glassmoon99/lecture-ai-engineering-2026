# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：
    第1回の回答では、正確な回答が得られず、一般的な回答が行われたのに対し、エージェントの回答は正確な回答が参照され
    またトークン数も抑制する事が出来た。
- `--trace` で見えたツール呼び出し（ツール名と引数）：
　　--- trace ---
	[tool call]   search_glossary({'query': 'LoRA'})
	[tool call]   search_glossary({'query': 'QLoRA'})
	[tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
	[tool return] search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…
	[usage] RunUsage(cost=Decimal('0.0008063'), details={'text_prompt_tokens': 1196}, input_text_tokens=1196, input_tokens=1196, output_tokens=179, requests=2, tool_calls=2)

- 1つの質問での LLM 呼び出し回数（`requests`）：2回
    [usage] RunUsage(cost=Decimal('0.0008063'), details={'text_prompt_tokens': 1196}, input_text_tokens=1196, input_tokens=1196, output_tokens=179, requests=2, tool_calls=2)

- 追加したツールと、docstring に書いた説明：
	def make_quiz(lecture: int) -> str:
		"""指定した回の用語から 1つを選び、
		確認問題と答えを返す。
		「第2回の確認問題を出して」のように、
		復習用の問題を求められたときに使う。
		"""
## 宿題

- 取り組んだレベル：基礎/実装
- やったこと：
	基礎：
		app/agent.py の INSTRUCTIONSの追加
		追加内容：「ヒントは、中学生レベルでも理解できるような説明文にする」
		app/tools.py のツールの make_quiz関数のdocstringの追加
		追加内容：「問題文を記載した後に、ヒントも記載する。」
- 結果：
	基礎：
		指示通りに問題文の後に専門的な用語の利用を控えたヒントが出力された。
		またToolのコール数の変更はなかったが、モデルのリクエストが変更前が2回に対し、変更後は3回となった。
	実装：
		Agentに対して学習内容の記録を指示する事により当該フォルダ上にmd形式のファイルが作成される事を確認。

- 気づき・疑問：
	基礎：
		エージェントを作成する上で、モデルそのものよりもハーネスの重要性を体験出来たと考える。これからは、モデル選定やハーネス設計が重要になると感じた。
		また結果に関しては、モデルの呼び出し回数が2回から3回へ増加した。ヒントの解説で中学生レベルので回答を指示した影響かと考えたが、断定できず疑問に残った。
	実装：
		ツールを利用する事により多くの変更作業が実現できることが分かった。
		試しに２度、保存を試したが、ログの内容が統一されていないため、改善が必要な点があると考える。
		これからエージェントを作成する際にモデル選定とハーネスの実装の仕方についてどちらを変更すれば改善に繋がるのか？という点が疑問として残った。

- ログ詳細（基礎）
	 <変更前>
	@glassmoon99 ➜ /workspaces/lecture-ai-engineering-2026 (lec03) $ uv run python -m app.agent --trace " 第3回の内容から確認問題を2問出して" 
	[model] gemini-3.5-flash-lite
	第3回（エージェント）の内容から、理解度を確かめる確認問題を2問出題します！

	---

	### 第1問
	「ハーネス」とはどのようなものを指すでしょうか？（ヒント：LLMの周りを…）

	### 第2問
	ターミナルで動くオープンソース（MITライセンス）のコーディングエージェントで、最小限の機能とシステムプロンプトで構成されているものは何でしょうか？

	---

	（関連する回：第3回）

	--- trace ---
	[tool call]   make_quiz({'lecture': 3})
	[tool call]   make_quiz({'lecture': 3})
	[tool return] make_quiz -> {"question": "「ハーネス」とは何ですか？", "answer": "LLMの周りを、ループ・ツール・画面（UI）などで包み、実際に作業できるようにするプログラム。Claude CodeやPiはハーネスの例。Piは組み込みツール…
	[tool return] make_quiz -> {"question": "「Pi」とは何ですか？", "answer": "ターミナルで動くオープンソース（MITライセンス）のコーディングエージェント。最小限の機能とシステムプロンプトで構成し、利用者が拡張して使う設計。2026年10月…
	[usage] RunUsage(cost=Decimal('0.0006545'), details={'text_prompt_tokens': 1040}, input_text_tokens=1040, input_tokens=1040, output_tokens=137, requests=2, tool_calls=2)
	@glassmoon99 ➜ /workspaces/lecture-ai-engineering-2026 (lec03) $ 

 <変更後>
	@glassmoon99 ➜ /workspaces/lecture-ai-engineering-2026 (lec03) $ uv run python -m app.agent --trace " 第3回の内容から確認問題を2問出して" 
	[model] gemini-3.5-flash-lite
	$第3回$の内容から、確認問題を2問出しますね！

	---

	### 第1問
	**「Pydantic AI」とは何ですか？**
	* **ヒント:** PythonでAIの便利なお手伝いさん（エージェント）を作るための道具箱（フレームワーク）の名前だよ。

	---

	### 第2問
	**「エージェントループ」とは何ですか？**
	* **ヒント:** AIに質問してから答えが出るまでの間に、AIが「自分で道具を使って、その結果を見て、また考える」という作業を、答えが出るまでクルクルと何度も繰り返す仕組みのことだよ。

	---

	関係する回：第3回

	--- trace ---
	[tool call]   make_quiz({'lecture': 3})
	[tool return] make_quiz -> {"question": "「Pydantic AI」とは何ですか？", "answer": "Pythonでエージェントを作るためのフレームワーク。Pydanticの型を使ってツールの引数や出力を定義でき、GeminiやOpenAIなど多…
	[tool call]   make_quiz({'lecture': 3})
	[tool return] make_quiz -> {"question": "「エージェントループ」とは何ですか？", "answer": "モデルに入力を渡す→モデルがツール呼び出しを返したら実行する→結果をモデルに戻す、をモデルが最終回答を返すまで繰り返す処理。1つの質問でLLMを複数…
	[usage] RunUsage(cost=Decimal('0.0009256'), details={'text_prompt_tokens': 1652}, input_text_tokens=1652, input_tokens=1652, output_tokens=172, requests=3, tool_calls=2)
	@glassmoon99 ➜ /workspaces/lecture-ai-engineering-2026 (lec03) $ 

- ログ詳細（実装）
	@glassmoon99 ➜ /workspaces/lecture-ai-engineering-2026 (lec03) $ uv run python -m app.agent --list-tools
	モデルに見えているツール: 4 個

	[search_glossary]
	講座の用語集から用語を検索し、定義と、どの回で扱うかを返す。
	
	AIエンジニアリングの用語や、この講座（AIE2026）に固有の言葉について
	答える前に使うこと。query には調べたい用語を1つだけ入れる（例: "LoRA"）。
	引数: {"query": {"type": "string"}}

	[get_lecture_summary]
	指定した回（1始まりの整数）の講義の要点を返す。
	
	「第3回では何を学ぶ？」のように、回の内容や関係を聞かれたときに使う。
	引数: {"lecture": {"type": "integer"}}

	[make_quiz]
	指定した回の用語から 1つを選び、確認問題と答えを返す。
	「第2回の確認問題を出して」のように、復習用の問題を求められたときに使う。
	問題文を記載した後に、ヒントも記載する。
	引数: {"lecture": {"type": "integer"}}

	[save_learning_log]
	利用者が学習内容の保存を求めたとき、learning_log/ に Markdown で保存する。
	引数: {"content": {"type": "string"}}
	@glassmoon99 ➜ /workspaces/lecture-ai-engineering-2026 (lec03) $ 
	@glassmoon99 ➜ /workspaces/lecture-ai-engineering-2026 (lec03) $ 
	@glassmoon99 ➜ /workspaces/lecture-ai-engineering-2026 (lec03) $ 
	@glassmoon99 ➜ /workspaces/lecture-ai-engineering-2026 (lec03) $ uv run python -m app.agent --trace "これまでの学習内容を記録"
	[model] gemini-3.5-flash-lite
	保存内容: {'content': '# 学習記録\nこれまでの学習内容のログです。'}
	この学習ログを保存しますか？ [y/N]: y
	これまでの学習内容を `learning_log/` に保存しました。

	これからもAIエンジニアリング講座（AIE2026）の学習をしっかりサポートしていきますので、分からない用語や回ごとの内容について、いつでも気軽に聞いてくださいね！

	--- trace ---
	[tool call]   save_learning_log({'content': '# 学習記録\nこれまでの学習内容のログです。'})
	[tool return] save_learning_log -> 学習ログを 20261108-053145-005730.md に保存しました。…
	[usage] RunUsage(cost=Decimal('0.0003002'), details={'text_prompt_tokens': 559}, input_text_tokens=559, input_tokens=559, output_tokens=53, requests=1, tool_calls=1)
	@glassmoon99 ➜ /workspaces/lecture-ai-engineering-2026 (lec03) $ 
	@glassmoon99 ➜ /workspaces/lecture-ai-engineering-2026 (lec03) $ 
	@glassmoon99 ➜ /workspaces/lecture-ai-engineering-2026 (lec03) $ ls -l learning_log/
	total 4
	-rw-rw-rw- 1 vscode vscode 61 Nov  8 05:31 20261108-053145-005730.md
	@glassmoon99 ➜ /workspaces/lecture-ai-engineering-2026 (lec03) $ 
	@glassmoon99 ➜ /workspaces/lecture-ai-engineering-2026 (lec03) $ uv run python -m app.agent --trace "学習内容を記録：第3回の復習と課題を実施"
	[model] gemini-3.5-flash-lite
	保存内容: {'content': '# 学習ログ\n\n- 日時: 2026年（または本日）\n- 内容: 第3回の復習と課題を実施'}
	この学習ログを保存しますか？ [y/N]: y
	学習内容を `learning_log/` に保存しました！

	第3回の復習と課題の実施、お疲れ様でした。引き続きこの調子で学習を進めていきましょう！

	（第3回）

	--- trace ---
	[tool call]   save_learning_log({'content': '# 学習ログ\n\n- 日時: 2026年（または本日）\n- 内容: 第3回の復習と課題を実施'})
	[tool return] save_learning_log -> 学習ログを 20261108-054210-748308.md に保存しました。…
	[usage] RunUsage(cost=Decimal('0.0002902'), details={'text_prompt_tokens': 584}, input_text_tokens=584, input_tokens=584, output_tokens=46, requests=1, tool_calls=1)
	@glassmoon99 ➜ /workspaces/lecture-ai-engineering-2026 (lec03) $ ls -la learning_log/
	total 16
	drwxrwxrwx+  2 vscode vscode 4096 Nov  8 05:42 .
	drwxrwxrwx+ 15 vscode root   4096 Nov  8 05:31 ..
	-rw-rw-rw-   1 vscode vscode   61 Nov  8 05:31 20261108-053145-005730.md
	-rw-rw-rw-   1 vscode vscode  100 Nov  8 05:42 20261108-054210-748308.md
	@glassmoon99 ➜ /workspaces/lecture-ai-engineering-2026 (lec03) $ cat learning_log/20261108-054210-748308.md 
	# 学習ログ

	- 日時: 2026年（または本日）
	- 内容: 第3回の復習と課題を実施

