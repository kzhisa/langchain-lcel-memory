## memory_runnable.py

このファイルは、LangChainを用いて、会話履歴を保持するチャットボットの例です。

### 概要

- LangChainの`RunnableWithMessageHistory`を使って、会話履歴を保持するチャットボットを作成します。
- 会話履歴は、`ChatMessageHistory`オブジェクトに格納されます。
- 会話履歴は、セッションIDごとに管理されます。

### コードの説明

1. **会話履歴のストア**
   - `store`という辞書型変数に、セッションIDをキー、会話履歴を値として格納します。

2. **セッションIDごとの会話履歴の取得**
   - `get_session_history`関数は、セッションIDを受け取り、対応する会話履歴を返します。
   - セッションIDが`store`に存在しない場合は、新しい`ChatMessageHistory`オブジェクトを作成して`store`に格納します。

3. **プロンプトテンプレート**
   - `prompt_template`は、会話履歴とユーザー入力を受け取るプロンプトテンプレートです。
   - `MessagesPlaceholder`を使って、会話履歴をプロンプトに埋め込みます。

4. **応答生成モデル**
   - `chat_model`は、OpenAIの`ChatOpenAI`モデルを使用します。
   - `model`パラメータに、使用するモデル名（例：`gpt-3.5-turbo`）を指定します。

5. **Runnableの準備**
   - `runnable`は、プロンプトテンプレートと応答生成モデルを組み合わせたRunnableです。

6. **RunnableをRunnableWithMessageHistoryでラップ**
   - `runnable_with_history`は、`RunnableWithMessageHistory`を使って、`runnable`をラップしたオブジェクトです。
   - `get_session_history`、`input_messages_key`、`history_messages_key`を指定することで、会話履歴を管理します。

7. **実際の応答生成**
   - `chat_with_bot`関数は、セッションIDを受け取り、チャットボットとの会話を開始します。
   - ユーザー入力を受け取り、`runnable_with_history`を使って応答を生成します。
   - 応答をコンソールに出力します。

8. **メイン関数**
   - メイン関数では、セッションIDを指定して`chat_with_bot`関数を呼び出し、チャットセッションを開始します。

### 実行方法

1. Python 3.8以降をインストールします。
2. `pip install -r requirements.txt`で必要なパッケージをインストールします。
3. `python memory_runnable1.py`を実行します。

### 注意点

- OpenAI APIキーを設定する必要があります。
- `ChatOpenAI`モデルを使用する場合は、OpenAIの利用規約に従ってください。
- 会話履歴は、`store`に格納されます。プログラム終了時にデータは失われます。

### その他

- このコードは、LangChainの簡単な例です。
- LangChainには、他にも多くの機能があります。
- LangChainのドキュメントを参照して、詳細を確認してください。
