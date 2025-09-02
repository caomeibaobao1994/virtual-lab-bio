"""智谱AI客户端包装器，兼容OpenAI接口"""

import os
import json
import uuid
import time
from typing import Any, Dict, List, Optional
from zhipuai import ZhipuAI


class MockRun:
    """模拟OpenAI Run对象"""
    def __init__(self, status: str = "completed", required_action: Optional[Dict] = None):
        self.id = str(uuid.uuid4())
        self.status = status
        self.required_action = required_action


class MockMessage:
    """模拟OpenAI Message对象"""
    def __init__(self, role: str, content: str, message_id: str = None, assistant_id: str = None):
        self.id = message_id or str(uuid.uuid4())
        self.role = role
        self.content = [{"type": "text", "text": {"value": content}}]
        self.created_at = int(time.time())
        self.assistant_id = assistant_id
    
    def to_dict(self):
        return {
            "id": self.id,
            "role": self.role,
            "content": self.content,
            "created_at": self.created_at,
            "assistant_id": self.assistant_id
        }


class MockMessagesAPI:
    """模拟OpenAI Messages API"""
    def __init__(self, client):
        self.client = client
    
    def create(self, thread_id: str, role: str, content: str, **kwargs):
        """创建消息"""
        if thread_id not in self.client._threads:
            self.client._threads[thread_id] = []
        
        message = MockMessage(role, content)
        self.client._threads[thread_id].append(message)
        return message
    
    def list(self, thread_id: str, limit: int = 100, order: str = "asc", after: str = None, **kwargs):
        """列出消息"""
        if thread_id not in self.client._threads:
            return []
        
        messages = self.client._threads[thread_id]
        
        # 处理after参数
        if after:
            after_idx = next((i for i, msg in enumerate(messages) if msg.id == after), -1)
            if after_idx >= 0:
                messages = messages[after_idx + 1:]
        
        # 处理order参数
        if order == "desc":
            messages = list(reversed(messages))
        
        # 处理limit参数
        messages = messages[:limit]
        
        return messages


class MockRunsAPI:
    """模拟OpenAI Runs API"""
    def __init__(self, client):
        self.client = client
    
    def create_and_poll(self, thread_id: str, assistant_id: str, model: str = None, 
                       temperature: float = 0.7, tools: List = None, **kwargs):
        """创建并轮询运行"""
        if thread_id not in self.client._threads:
            return MockRun("failed")
        
        messages = self.client._threads[thread_id]
        if not messages:
            return MockRun("failed")
        
        # 获取对话历史
        conversation = []
        for msg in messages:
            if msg.content and len(msg.content) > 0:
                conversation.append({
                    "role": msg.role,
                    "content": msg.content[0]["text"]["value"]
                })
        
        # 调用智谱AI
        try:
            response = self.client.zhipu_client.chat.completions.create(
                model=model or "glm-4-plus",
                messages=conversation,
                temperature=temperature
            )
            
            # 添加助手回复
            assistant_content = response.choices[0].message.content
            assistant_message = MockMessage("assistant", assistant_content, assistant_id=assistant_id)
            self.client._threads[thread_id].append(assistant_message)
            
            return MockRun("completed")
            
        except Exception as e:
            print(f"智谱AI调用失败: {e}")
            return MockRun("failed")
    
    def submit_tool_outputs_and_poll(self, thread_id: str, run_id: str, tool_outputs: List, **kwargs):
        """提交工具输出并轮询"""
        # 简单实现，直接返回完成状态
        return MockRun("completed")


class MockAssistant:
    """模拟OpenAI Assistant对象"""
    def __init__(self, name: str, instructions: str, model: str, **kwargs):
        self.id = str(uuid.uuid4())
        self.name = name
        self.instructions = instructions
        self.model = model
        self.created_at = int(time.time())


class MockAssistantsAPI:
    """模拟OpenAI Assistants API"""
    def __init__(self, client):
        self.client = client
    
    def create(self, name: str, instructions: str, model: str, **kwargs):
        """创建助手"""
        return MockAssistant(name, instructions, model, **kwargs)


class MockThread:
    """模拟OpenAI Thread对象"""
    def __init__(self, thread_id: str):
        self.id = thread_id
        self.created_at = int(time.time())


class MockThreadsAPI:
    """模拟OpenAI Threads API"""
    def __init__(self, client):
        self.client = client
        self.messages = MockMessagesAPI(client)
        self.runs = MockRunsAPI(client)
    
    def create(self, **kwargs):
        """创建线程"""
        thread_id = str(uuid.uuid4())
        self.client._threads[thread_id] = []
        return MockThread(thread_id)


class MockBetaAPI:
    """模拟OpenAI Beta API"""
    def __init__(self, client):
        self.threads = MockThreadsAPI(client)
        self.assistants = MockAssistantsAPI(client)


class ZhipuAIWrapper:
    """智谱AI客户端包装器，兼容OpenAI接口"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("ZHIPUAI_API_KEY")
        if not self.api_key:
            raise ValueError("需要设置ZHIPUAI_API_KEY环境变量")
        
        self.zhipu_client = ZhipuAI(api_key=self.api_key)
        self._threads = {}  # 存储线程消息
        self.beta = MockBetaAPI(self)
    
    def chat_completions_create(self, model: str, messages: List[Dict], 
                               temperature: float = 0.7, **kwargs):
        """直接调用chat completion"""
        return self.zhipu_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            **kwargs
        ) 