# # import socket
# # import cv2
# # import numpy as np
# # import struct

# # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # host_ip = '192.168.1.7'  # Update with the server's IP address
# # port = 9999
# # client_socket.connect((host_ip, port))

# # def recvall(sock, count):
# #     buf = b''
# #     while count:
# #         new_buf = sock.recv(count)
# #         if not new_buf:
# #             return None
# #         buf += new_buf
# #         count -= len(new_buf)
# #     return buf

# # while True:
# #     # Receive the size of the frame
# #     frame_size_data = recvall(client_socket, struct.calcsize("L"))
# #     if not frame_size_data:
# #         break
# #     frame_size = struct.unpack("L", frame_size_data)[0]

# #     # Receive the frame data
# #     frame_data = recvall(client_socket, frame_size)
# #     if not frame_data:
# #         break

# #     # Decode the frame and display it
# #     frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)
# #     cv2.imshow("RECEIVING VIDEO", frame)
# #     if cv2.waitKey(1) & 0xFF == ord('q'):
# #         break

# # client_socket.close()

# import asyncio
# import websockets
# import cv2
# import numpy as np
# import base64

# async def receive_frames():
#     uri = "ws://192.168.1.7:9999"  # Update with your server's URI
#     async with websockets.connect(uri) as websocket:
#         print("Connected to server")
#         try:
#             while True:
#                 # Receive frame from server
#                 jpg_as_text = await websocket.recv()
                
#                 # Convert base64 string to numpy array
#                 jpg_original = base64.b64decode(jpg_as_text)
#                 jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
                
#                 # Decode the JPEG buffer to get the frame
#                 frame = cv2.imdecode(jpg_as_np, flags=1)
                
#                 # Display the received frame
#                 cv2.imshow("Received Frame", frame)
                
#                 # Check for 'q' key press to quit
#                 if cv2.waitKey(1) & 0xFF == ord('q'):
#                     break
#         except websockets.exceptions.ConnectionClosedError:
#             print("Server disconnected")
#         finally:
#             cv2.destroyAllWindows()

# asyncio.get_event_loop().run_until_complete(receive_frames())