"""Реализация многопоточного HTTP-сервера."""

import gzip
import os
import socket
from concurrent.futures import ThreadPoolExecutor

from pyhttpd.config import DOCUMENT_ROOT, HOST, MAX_WORKERS, PORT
from pyhttpd.logger import logger


def gzip_compress(data: bytes) -> bytes:
    """Сжатие данных с помощью Gzip перед отправкой."""
    return gzip.compress(data)


file_cache: dict[str, bytes] = {}


def get_file_content(file_path: str) -> bytes:
    """Caches and returns file contents to optimize file reads."""
    if file_path not in file_cache:
        try:
            with open(file_path, 'rb') as f:
                file_cache[file_path] = f.read()
        except FileNotFoundError:
            return b''
    return file_cache[file_path]


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
            content = get_file_content(file_path)
            compressed_content = gzip_compress(content)

            response_headers = (
                f'HTTP/1.1 200 OK\r\nContent-Length: {len(compressed_content)}\r\nContent-Encoding: gzip\r\n\r\n'
            )

            if method == 'GET':
                client_socket.sendall(response_headers.encode() + compressed_content)
            else:
                client_socket.sendall(response_headers.encode())
        else:
            content = get_file_content(os.path.join(DOCUMENT_ROOT, '404.html'))
            compressed_content = gzip_compress(content)

            response_headers = (
                f'HTTP/1.1 404 Not Found\r\nContent-Length: {len(compressed_content)}\r\nContent-Encoding: gzip\r\n\r\n'
            )
            client_socket.sendall(response_headers.encode() + compressed_content)

        logger.info(f'{method} {path} - 200 OK' if os.path.exists(file_path) else f'{method} {path} - 404 Not Found')

    except Exception as e:
        logger.error(f'Error handling request: {e}')
    finally:
        client_socket.close()


def start_server() -> None:
    """Запускает многопоточный HTTP-сервер."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(1000)

        logger.info(f'Server running on {HOST}:{PORT}')

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            while True:
                client_socket, _ = server_socket.accept()
                executor.submit(handle_request, client_socket)


if __name__ == '__main__':
    start_server()
