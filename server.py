# import socket
# import cv2
# import struct

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host_name = socket.gethostname()
# print("host name", host_name)
# host_ip = socket.gethostbyname(host_name)
# print('HOST IP:', host_ip)
# port = 9999
# socket_address = (host_ip, port)
# server_socket.bind(socket_address)
# server_socket.listen(5)
# print("LISTENING AT:", socket_address)

# def send_video(client_socket, vid):
#     while vid.isOpened():
#         ret, frame = vid.read()
#         if not ret:
#             break
#         encoded_frame = cv2.imencode('.jpg', frame)[1]
#         frame_size = struct.pack("L", len(encoded_frame))
#         client_socket.sendall(frame_size + encoded_frame.tobytes())

# while True:
#     client_socket, addr = server_socket.accept()
#     print('GOT CONNECTION FROM:', addr)
#     if client_socket:
#         vid = cv2.VideoCapture(r"I:\MODELS\Backend2\WeaponeDetection\videos\pistol.mp4")
#         send_video(client_socket, vid)
#         vid.release()
#         client_socket.close()
#         break  # Break after streaming to one client, remove this line for continuous streaming


import asyncio
import cv2
import websockets
import base64

async def transmit(websocket, path):
    print("Client Connected !")
    try:
        cap = cv2.VideoCapture(r"I:\MODELS\Backend2\WeaponeDetection\videos\videoplayback_7.mp4")
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convert the frame to JPEG format
            _, buffer = cv2.imencode('.jpg', frame)
            
            # Convert the frame to base64 string
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')
            
            # Send the frame to the client
            await websocket.send(jpg_as_text)
            
            # Display the frame locally (optional)
            cv2.imshow("Transmission", frame)
            
            # Check for 'q' key press to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except websockets.exceptions.ConnectionClosedError:
        print("Client Disconnected !")
    finally:
        cap.release()
        cv2.destroyAllWindows()

port = 9999
print("Started server on port:", port)

start_server = websockets.serve(transmit, port=port)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()