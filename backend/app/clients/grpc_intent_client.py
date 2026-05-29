import grpc
import logging
from app.clients.base import BaseClient
from app.core.settings import settings
import app.clients.intent_grpc.intent_service_pb2 as pb2
import app.clients.intent_grpc.intent_service_pb2_grpc as pb2_grpc

class GrpcIntentClient(BaseClient):
    def __init__(self):
        host = settings.INTENT_SERVICE_HOST
        port = settings.INTENT_SERVICE_PORT
        self.channel_target = f"{host}:{port}"
        
    def predict_intent(self, message: str) -> dict:
        try:
            with grpc.insecure_channel(self.channel_target) as channel:
                stub = pb2_grpc.IntentServiceStub(channel)
                req = pb2.IntentRequest(message=message)
                resp = stub.IntentRecognizer(req, timeout=10.0)
                
                return {
                    "intent": resp.intent,
                    "confidence": resp.confidence,
                    "reason": resp.reason,
                    "error": None
                }
        except Exception as e:
            logging.error(f"gRPC call failed: {e}")
            return {
                "intent": "general_inquiry",
                "confidence": 0.0,
                "reason": "Error connecting to intent service",
                "error": str(e)
            }
