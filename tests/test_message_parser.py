"""测试消息解析器"""
import pytest
from src.facebook.message_parser import FacebookMessageParser
from src.database.models import MessageType


def test_parse_messaging_event():
    """测试解析私信事件"""
    parser = FacebookMessageParser()
    
    event = {
        "sender": {"id": "123456"},
        "recipient": {"id": "789012"},
        "message": {
            "mid": "msg_123",
            "text": "你好，我想咨询一下"
        },
        "timestamp": 1234567890
    }
    
    result = parser._parse_messaging_event(event, "page_123")
    
    assert result is not None
    assert result["message_type"] == MessageType.MESSAGE
    assert result["sender_id"] == "123456"
    assert result["content"] == "你好，我想咨询一下"


def test_parse_comment_event():
    """测试解析评论事件"""
    parser = FacebookMessageParser()
    
    change = {
        "field": "feed",
        "value": {
            "verb": "add",
            "post_id": "post_123",
            "from": {"id": "user_456"},
            "comment": {
                "id": "comment_789",
                "message": "这是一个评论"
            },
            "created_time": 1234567890
        }
    }
    
    result = parser._parse_comment_event(change, "page_123")
    
    assert result is not None
    assert result["message_type"] == MessageType.COMMENT
    assert result["post_id"] == "post_123"
    assert result["content"] == "这是一个评论"


def test_parse_webhook_event():
    """测试解析 Webhook 事件"""
    parser = FacebookMessageParser()
    
    event = {
        "object": "page",
        "entry": [
            {
                "id": "page_123",
                "messaging": [
                    {
                        "sender": {"id": "123456"},
                        "recipient": {"id": "789012"},
                        "message": {
                            "mid": "msg_123",
                            "text": "测试消息"
                        },
                        "timestamp": 1234567890
                    }
                ]
            }
        ]
    }
    
    result = parser.parse_webhook_event(event)
    
    assert result is not None
    assert len(result) == 1
    assert result[0]["message_type"] == MessageType.MESSAGE


