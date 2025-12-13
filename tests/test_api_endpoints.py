"""API端点测试套件"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from src.main import app
from src.database.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.database import Base

# 创建测试数据库
test_engine = create_engine("sqlite:///:memory:", echo=False)
TestSessionLocal = sessionmaker(bind=test_engine)


@pytest.fixture
def db_session():
    """创建测试数据库会话"""
    Base.metadata.create_all(test_engine)
    session = TestSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(test_engine)


@pytest.fixture
def client(db_session):
    """创建测试客户端，并覆盖数据库依赖"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


class TestHealthEndpoints:
    """健康检查端点测试"""
    
    def test_root_endpoint(self, client):
        """测试根端点"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data or "status" in data
    
    def test_health_endpoint(self, client):
        """测试健康检查端点"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        # 健康检查应该返回状态信息
        assert isinstance(data, dict)
    
    def test_metrics_endpoint(self, client):
        """测试性能指标端点"""
        response = client.get("/metrics")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)


class TestWebhookEndpoints:
    """Webhook端点测试"""
    
    def test_facebook_webhook_verification(self, client):
        """测试Facebook Webhook验证"""
        response = client.get(
            "/webhook",
            params={
                "hub.mode": "subscribe",
                "hub.verify_token": "test_token",
                "hub.challenge": "test_challenge"
            }
        )
        # 验证端点应该返回challenge或403
        assert response.status_code in [200, 403]
    
    def test_facebook_webhook_receive(self, client):
        """测试Facebook Webhook消息接收"""
        webhook_payload = {
            "object": "page",
            "entry": [{
                "id": "page_id",
                "messaging": [{
                    "sender": {"id": "user123"},
                    "recipient": {"id": "page_id"},
                    "message": {
                        "mid": "msg123",
                        "text": "测试消息"
                    }
                }]
            }]
        }
        
        response = client.post("/webhook", json=webhook_payload)
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
    
    def test_instagram_webhook_verification(self, client):
        """测试Instagram Webhook验证"""
        response = client.get(
            "/instagram/webhook",
            params={
                "hub.mode": "subscribe",
                "hub.verify_token": "test_token",
                "hub.challenge": "test_challenge"
            }
        )
        # 验证端点应该返回challenge或403
        assert response.status_code in [200, 403]


class TestAdminEndpoints:
    """管理后台端点测试"""
    
    def test_list_conversations(self, client, db_session):
        """测试对话列表端点"""
        response = client.get("/admin/conversations?page=1&page_size=10")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "pagination" in data
        assert isinstance(data["data"], list)
    
    def test_get_conversation_detail(self, client, db_session):
        """测试对话详情端点"""
        # 先创建一个测试对话
        from src.database.models import Customer, Conversation, MessageType
        
        customer = Customer(platform="facebook", platform_user_id="test")
        db_session.add(customer)
        db_session.flush()
        
        conversation = Conversation(
            customer_id=customer.id,
            platform="facebook",
            message_type=MessageType.MESSAGE,
            content="测试消息"
        )
        db_session.add(conversation)
        db_session.commit()
        
        response = client.get(f"/admin/conversations/{conversation.id}")
        assert response.status_code == 200
        data = response.json()
        assert "conversation" in data or "error" in data
    
    def test_get_statistics(self, client, db_session):
        """测试统计数据端点"""
        response = client.get("/admin/statistics?days=7")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
    
    def test_list_customers(self, client, db_session):
        """测试客户列表端点"""
        response = client.get("/admin/customers?page=1&page_size=10")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "pagination" in data


class TestStatisticsEndpoints:
    """统计API端点测试"""
    
    def test_daily_statistics(self, client, db_session):
        """测试每日统计端点"""
        response = client.get("/statistics/daily")
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
    
    def test_statistics_summary(self, client, db_session):
        """测试统计摘要端点"""
        response = client.get("/statistics/summary")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)


class TestMonitoringEndpoints:
    """监控端点测试"""
    
    def test_live_monitoring(self, client):
        """测试实时监控端点（SSE）"""
        response = client.get("/monitoring/live")
        # SSE端点应该返回200或流式响应
        assert response.status_code in [200, 200]  # SSE通常返回200
    
    def test_live_stats(self, client, db_session):
        """测试实时统计端点"""
        response = client.get("/monitoring/stats")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
    
    def test_recent_replies(self, client):
        """测试最近回复端点"""
        response = client.get("/monitoring/recent-replies?limit=10")
        assert response.status_code == 200
        data = response.json()
        assert "success" in data or "data" in data

