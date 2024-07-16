from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai.chat_models import ChatOpenAI

# 保持する会話履歴数
DEFAULT_MAX_MESSAGES = 4

# 会話履歴のストア
store = {}

# 会話履歴数をmax_lengthに制限するLimitedChatMessageHistoryクラス
class LimitedChatMessageHistory(ChatMessageHistory):

    # 会話履歴の保持数
    max_messages: int = DEFAULT_MAX_MESSAGES

    def __init__(self, max_messages=DEFAULT_MAX_MESSAGES):
        super().__init__()
        self.max_messages = max_messages

    def add_message(self, message):
        super().add_message(message)
        # 会話履歴数を制限
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def get_messages(self):
        return self.messages


# セッションIDごとの会話履歴の取得
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = LimitedChatMessageHistory()
    return store[session_id]


# プロンプトテンプレートで会話履歴を追加
prompt_template = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="history"),  # 会話履歴の追加
        ("human", "{input}"),
    ]
)

# 応答生成モデル（例としてchat_model）
chat_model = ChatOpenAI(model="gpt-3.5-turbo")

# Runnableの準備
runnable = prompt_template | chat_model

# RunnableをRunnableWithMessageHistoryでラップ
runnable_with_history = RunnableWithMessageHistory(
    runnable=runnable,
    get_session_history=get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

# 実際の応答生成の例
def chat_with_bot(session_id: str):
    count = 0
    while True:
        print("---")
        input_message = input(f"[{count}]あなた: ")
        if input_message.lower() == "終了":
            break

        # プロンプトテンプレートに基づいて応答を生成
        response = runnable_with_history.invoke(
            {"input": input_message},
            config={"configurable": {"session_id": session_id}}
        )
        
        print(f"AI: {response.content}")
        print(f"\n会話履歴:\n{store[session_id]}")
        count += 1


if __name__ == "__main__":

    # チャットセッションの開始
    session_id = "example_session"
    chat_with_bot(session_id)
