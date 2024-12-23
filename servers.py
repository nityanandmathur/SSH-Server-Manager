import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget, QListWidget, QListWidgetItem
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QSize


class ServerManagerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SSH Server Manager")
        self.setGeometry(100, 100, 600, 330)
        self.servers = []  # Store server names
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #2E3440;
                color: #D8DEE9;
                font-family: Arial, sans-serif;
            }
            QVBoxLayout {
                spacing: 20px;
            }
            QLabel {
                color: #88C0D0;
            }
            QPushButton {
                background-color: #4C566A;
                border: none;
                padding: 10px;
                color: #D8DEE9;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5E81AC;
            }
            QListWidget {
                background-color: #3B4252;
                border: none;
            }
        """)

        layout = QVBoxLayout()

        # Title
        title_label = QLabel("List of SSH Servers")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        layout.addWidget(title_label)

        # Server List
        self.server_list = QListWidget()
        layout.addWidget(self.server_list)

        # Load Servers
        self.load_servers()

        # Set Layout
        self.setLayout(layout)

    def load_servers(self):
        """Load SSH servers from ~/.ssh/config and populate the list."""
        ssh_config_path = os.path.expanduser("~/.ssh/config")
        if not os.path.exists(ssh_config_path):
            self.server_list.addItem("No ~/.ssh/config file found.")
            return

        # Efficiently read and parse the SSH config file
        with open(ssh_config_path, "r") as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if line.startswith("Host ") and not line.startswith("Host *"):  # Exclude wildcard hosts
                host = line.split()[1]
                self.servers.append(host)

        # Populate the list with servers
        self.populate_server_list()
        self.adjustSize()

    def populate_server_list(self):
        """Populate the QListWidget with server items."""
        for host in self.servers:
            self.add_server_to_list(host)

    def add_server_to_list(self, host):
        """Add a server to the QListWidget."""
        # Create a horizontal layout for the item
        item_widget = QWidget()
        item_layout = QHBoxLayout()
        item_layout.setContentsMargins(10, 5, 10, 5)

        # Host Label
        host_label = QLabel(host)
        host_label.setFont(QFont("Arial", 14))
        item_layout.addWidget(host_label)

        # Open Terminal Button
        terminal_button = QPushButton("Open Terminal")
        terminal_font = QFont("Arial", 10)  # Reduced font size
        terminal_button.setFont(terminal_font)
        terminal_button.setIcon(QIcon.fromTheme("utilities-terminal"))
        terminal_button.setIconSize(QSize(20, 20))
        terminal_button.setToolTip("Open Terminal")
        terminal_button.setStyleSheet("""
            QPushButton {
                padding: 5px 10px;
            }
        """)
        terminal_button.clicked.connect(lambda _, h=host: self.open_terminal(h))
        item_layout.addWidget(terminal_button)

        # Open VS Code Button
        vscode_button = QPushButton("Open VS Code")
        vscode_font = QFont("Arial", 10)  # Reduced font size
        vscode_button.setFont(vscode_font)
        vscode_button.setIcon(QIcon.fromTheme("code"))
        vscode_button.setIconSize(QSize(20, 20))
        vscode_button.setToolTip("Open VS Code")
        vscode_button.setStyleSheet("""
            QPushButton {
                padding: 5px 10px;
            }
        """)
        vscode_button.clicked.connect(lambda _, h=host: self.open_vscode(h))
        item_layout.addWidget(vscode_button)

        # Finalize Layout
        item_widget.setLayout(item_layout)
        list_item = QListWidgetItem(self.server_list)
        list_item.setSizeHint(item_widget.sizeHint())
        self.server_list.addItem(list_item)
        self.server_list.setItemWidget(list_item, item_widget)

    def open_terminal(self, host):
        """Open a terminal session for the given host."""
        subprocess.Popen(["osascript", "-e", f'tell application "Terminal" to do script "ssh {host}"'])

    def open_vscode(self, host):
        """Open VS Code remote session for the given host in a new window."""
        try:
            subprocess.Popen([
                "code",
                "--new-window",  # Ensures a new VS Code window is opened
                "--remote", f"ssh-remote+{host}"  # Connects to the correct server
            ])
        except FileNotFoundError:
            print("VS Code CLI not found. Please ensure it is installed and added to the PATH.")


if __name__ == "__main__":
    app = QApplication([])
    window = ServerManagerApp()
    window.show()
    app.exec_()