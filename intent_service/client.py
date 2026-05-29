import grpc
import intent_service_pb2
import intent_service_pb2_grpc
import sys

def run():
    # Connect to the grpc server
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = intent_service_pb2_grpc.IntentServiceStub(channel)
        
        message = "I lost my credit card today, can you help me?"
        if len(sys.argv) > 1:
            message = " ".join(sys.argv[1:])
            
        print(f"Sending message: '{message}'")
        
        request = intent_service_pb2.IntentRequest(message=message)
        response = stub.IntentRecognizer(request)
        
        print("\nResponse:")
        print(f"Intent: {response.intent}")
        print(f"Confidence: {response.confidence}")
        print(f"Reason: {response.reason}")

if __name__ == '__main__':
    run()
