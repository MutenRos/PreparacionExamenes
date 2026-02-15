sudo apt update
sudo apt install -y python3-venv git
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
pip install diffusers transformers accelerate safetensors pillow

