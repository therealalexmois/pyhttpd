"""Реализация многопоточного HTTP-сервера."""

import os
import socket
from concurrent.futures import ThreadPoolExecutor

from pyhttpd.config import DOCUMENT_ROOT, HOST, PORT
from pyhttpd.logger import logger


def handle_request(client_socket: socket.socket) -> None:
    """Обрабатывает входящий HTTP-запрос."""
    try:
        request: str = client_socket.recv(1024).decode()
        if not request:
            return

        lines: list[str] = request.split('\r\n')
        method, path, _ = lines[0].split(' ')

        if path == '/':
            path = '/index.html'

        file_path: str = os.path.join(DOCUMENT_ROOT, path.lstrip('/'))

        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                content: bytes = f.read()
            response: str = f'HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\n\r\n'
            if method == 'GET':
                client_socket.sendall(response.encode() + content)
            else:
                client_socket.sendall(response.encode())
        else:
            file_path = os.path.join(DOCUMENT_ROOT, '404.html')
            with open(file_path, 'rb') as f:
                content = f.read()
            response = f'HTTP/1.1 404 Not Found\r\nContent-Length: {len(content)}\r\n\r\n'
            client_socket.sendall(response.encode() + content)

        logger.info(f'{method} {path} - 200 OK' if os.path.exists(file_path) else f'{method} {path} - 404 Not Found')

    except Exception as e:
        logger.error(f'Error handling request: {e}')
    finally:
        client_socket.close()


def start_server() -> None:
    """Запускает многопоточный HTTP-сервер."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(10)

        logger.info(f'Server running on {HOST}:{PORT}')

        with ThreadPoolExecutor(max_workers=10) as executor:
            while True:
                client_socket, _ = server_socket.accept()
                executor.submit(handle_request, client_socket)


if __name__ == '__main__':
    start_server()
