import grpc
from concurrent import futures
import logging
import sys
import os

# Ensure the parent directory is in sys.path when running independently
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import intent_service_pb2
import intent_service_pb2_grpc
from app.nodes.intent_node import IntentNode
from app.core.settings import settings

class IntentService(intent_service_pb2_grpc.IntentServiceServicer):
    def __init__(self):
        self.intent_node = IntentNode()

    def IntentRecognizer(self, request, context):
        logging.info(f"Received predict request for message: {request.message}")
        result = self.intent_node.predict_intent(request.message)
        
        return intent_service_pb2.IntentResponse(
            intent=result.intent,
            confidence=result.confidence,
            reason=result.reason
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    intent_service_pb2_grpc.add_IntentServiceServicer_to_server(IntentService(), server)
    
    port = settings.GRPC_PORT
    server.add_insecure_port(f'[::]:{port}')
    
    logging.info(f"Starting gRPC server on port {port}...")
    server.start()
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logging.info("Shutting down server...")
        server.stop(0)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()
