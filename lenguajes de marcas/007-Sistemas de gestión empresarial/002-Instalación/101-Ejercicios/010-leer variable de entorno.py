# En el shell (terminal):
# echo 'export NOMBRE="Jose Vicente"' >> ~/.bashrc
# source ~/.bashrc
import os

print(os.environ.get("NOMBRE"))