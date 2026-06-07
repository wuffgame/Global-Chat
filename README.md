# Global-Chat

This project will be a global chat where everyone will be able to log in and chat with people from all over the world.

## **Installation Guide**

### **Requirements:**

- `python` (I use version 3.13)
- `docker compose` (if you want to follow this guide)

### **Linux (with docker)**

1. In the terminal, go to the directory where you want to copy the repository and run this command:

   ```
   git clone https://github.com/wuffgame/Global-Chat
   ```
2. Next, go to the folder with the `Dockerfile` and run this command to the server:

   ```
   docker compose up --build -d
   ```
3. Then, to turn on the client, run this command in the same folder (there are 2 client files for testing):

   ```
   python3 client.py
   ```
4. Ready, enjoy using it!!!

### **Notes**

Windows install guide will be added in the future. MacOs install guide will come someday when I get access to one.
