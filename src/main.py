#!/usr/bin/python3
# coding=utf-8

import ollama


# 智能体对象
class AgentClass:
    def __init__(self, model="llama3.2"):
        self.model = model
        self.history = []

    # 与模型进行对话
    def chat(self, message):

        context = "\n".join(
            [f"用户：{h['user']}\n助手：{h['agent']}" for h in self.history[-3:]]
        )

        prompt = f"""
        对话历史：
        {context}
        
        用户：{message}
        助手：
        """

        result = ollama.generate(
            model=self.model, prompt=prompt  # 模型名称  # 提示文本
        )

        # 历史记录起来
        self.add_to_history(message, result.response)

        return result.response

    # 添加到对话历史
    def add_to_history(self, user_msg, agent_msg):
        self.history.append({"user": user_msg, "agent": agent_msg})


# 回答对象
def doAsk(agent):
    task = input("请输入任务：")

    if task == "exit":
        print("再见")
    else:
        result = agent.chat(task)
        print(result)
        doAsk(agent)


# 运行
if __name__ == "__main__":
    agent = AgentClass()
    doAsk(agent)
