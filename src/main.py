#!/usr/bin/python3
# coding=utf-8

import ollama
import json
import os
from datetime import datetime


# 智能体对象
class AgentClass:
    def __init__(self, model="llama3.2", memory_file="memory.json"):
        self.model = model
        self.memory_file = memory_file

        self.history = []  # 短期记忆：当前对话的上下文
        self.long_term_memory = []  # 长期记忆：用户偏好、个人信息等重要数据

        self.load_memory()

    # 与模型进行对话
    def chat(self, message):

        # 搜索相关记忆
        relevant_memories = self.search_memory(message)

        # 构建提示词
        memory_context = ""
        if relevant_memories:
            memory_context = (
                "相关记忆：\n"
                + "\n".join([f"- {m['content']}" for m in relevant_memories[-3:]])
                + "\n\n"
            )

        # 添加短期记忆（对话历史）
        history_context = self.get_recent_history()

        prompt = f"""
        {memory_context}
        当前对话历史：
        {history_context}
        
        用户：{message}
        助手：
        """

        result = ollama.generate(
            model=self.model, prompt=prompt  # 模型名称  # 提示文本
        )
        response = result.response

        # 历史记录起来
        self.add_to_history(message, response)

        # 如果用户提到了个人信息，添加到长期记忆
        if any(
            word in message.lower()
            for word in ["我的名字是", "我喜欢", "我住在", "我的工作是", "我是"]
        ):
            self.add_to_long_term_memory(message, "user_info")

        return response

    # 添加到对话历史
    def add_to_history(self, user_msg, agent_msg):
        self.history.append({"user": user_msg, "agent": agent_msg})

    # 获取最近的对话历史
    def get_recent_history(self):
        return "\n".join(
            [f"用户：{h['user']}\n助手：{h['agent']}" for h in self.history[-3:]]
        )

    # 添加到长期记忆
    # 把数据添加到long_term_memory + 保存长期记忆
    def add_to_long_term_memory(self, key_info, memory_type):
        memory_item = {
            "content": key_info,
            "timestamp": datetime.now().isoformat(),
            "type": memory_type,
        }
        self.long_term_memory.append(memory_item)
        self.save_memory()

    # 保存长期记忆
    # 把long_term_memory写入到磁盘中
    def save_memory(self):
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.long_term_memory, f, ensure_ascii=False, indent=2)

    # 加载长期记忆
    # 把磁盘中的数据加载到long_term_memory
    def load_memory(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    self.long_term_memory = json.load(f)
            except:
                self.long_term_memory = []

    # 搜索相关记忆
    def search_memory(self, query):
        relevant_memories = []
        for memory in self.long_term_memory:
            # if any(
            #     keyword in memory["content"].lower()
            #     for keyword in query.lower().split()
            # ):
            #     relevant_memories.append(memory)
            relevant_memories.append(memory)
        return relevant_memories


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
