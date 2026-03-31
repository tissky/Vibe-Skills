#!/usr/bin/env python3

import json
import pathlib
import socket
import sys
import time


def main() -> int:
    if len(sys.argv) != 5:
        print(
            "usage: send-qmp-boot-keys.py <qmp-socket> <key[,key]> <rounds> <interval-ms>",
            file=sys.stderr,
        )
        return 2

    qmp_socket = pathlib.Path(sys.argv[1])
    boot_keys = [key for key in sys.argv[2].split(",") if key]
    rounds = int(sys.argv[3])
    interval_ms = int(sys.argv[4])

    if not boot_keys or rounds <= 0:
        return 0

    for _ in range(120):
        if qmp_socket.exists():
            break
        time.sleep(0.25)
    else:
        return 0

    for _ in range(rounds):
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect(str(qmp_socket))
            sock.recv(4096)
            sock.sendall(b'{"execute":"qmp_capabilities"}\r\n')
            sock.recv(4096)

            for boot_key in boot_keys:
                wire = json.dumps(
                    {
                        "execute": "input-send-event",
                        "arguments": {
                            "events": [
                                {
                                    "type": "key",
                                    "data": {
                                        "down": True,
                                        "key": {"type": "qcode", "data": boot_key},
                                    },
                                },
                                {
                                    "type": "key",
                                    "data": {
                                        "down": False,
                                        "key": {"type": "qcode", "data": boot_key},
                                    },
                                },
                            ]
                        },
                    }
                ).encode() + b"\r\n"
                sock.sendall(wire)
                sock.recv(4096)

            sock.close()
        except Exception:
            pass

        time.sleep(interval_ms / 1000.0)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
