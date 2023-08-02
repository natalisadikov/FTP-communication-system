# Server-Client Communication Project

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Description

This project focuses on server-client communication starting from the computer turning on and involves the implementation of DHCP, DNS, and an FTP server. The communication process begins with the computer sending a DHCP broadcast message to obtain an IP address. Once the computer acquires an IP address, it contacts the DNS server to resolve domain addresses. After receiving the desired IP address, the computer attempts to connect to the custom FTP server, which facilitates file transfer over the Internet. The project is written in Python and requires root privileges to capture and analyze network packets using the Scapy library.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Installation

1. Clone the repository to your local machine using:
2. Change into the project directory:
3. To run each part of the project (DHCP, DNS, Client, FTP server), open separate terminal windows and navigate to the project folder using the `cd` command. Run each part using Python, and when required, use `sudo` to grant root privileges for packet analysis.

## Usage

- DHCP: Run the DHCP server to facilitate IP address allocation to the clients.
- DNS: Start the DNS server to resolve domain addresses and provide the desired IP addresses to clients.
- Client: Execute the client code to establish communication with the DNS server and FTP server.
- FTP Server: Launch the custom FTP server to facilitate file transfers between clients.

**Note:** Each part of the project should be run in a separate terminal window.

## Contributing

We welcome contributions to improve the project. If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch with a descriptive name: `git checkout -b feature/your-feature-name`.
3. Make your changes and commit them with clear commit messages.
4. Push the changes to your fork: `git push origin feature/your-feature-name`.
5. Create a pull request, and our team will review your changes.


## Contact

For any questions or support, feel free to reach out:

- Email: natalisadikov2318@gmail.com
- GitHub https://github.com/natalisadikov

---
This README provides an overview of the project and includes information on how to install, use, contribute, and contact the developers. Feel free to modify it as needed to match your project's specific details.
