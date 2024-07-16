from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai.chat_models import ChatOpenAI

# 会話履歴のストア
store = {}

# セッションIDごとの会話履歴の取得
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# プロンプトテンプレートで会話履歴を追加
prompt_template = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="history"),
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
        count += 1


if __name__ == "__main__":

    # チャットセッションの開始
    session_id = "example_session"
    chat_with_bot(session_id)
