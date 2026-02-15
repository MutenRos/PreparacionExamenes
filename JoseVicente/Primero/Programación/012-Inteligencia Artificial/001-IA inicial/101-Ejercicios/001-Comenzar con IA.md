1.-Instalar un contenedor de modelos "fácil"
2.-Os recomiendo usar Ubuntu
3.-Os recomiendo usar ollama

4.- Ejecutar este comando
curl -fsSL https://ollama.com/install.sh | sh

5.-Descargar uno o varios modelos de IA a nuestro equipo

ollama pull [nombre]

Modelos que tengo descargados ahora mismo:
ollama list

josevicente@josevicenteportatil:~$ ollama list
NAME                         ID              SIZE      MODIFIED     
nomic-embed-text:latest      0a109f422b47    274 MB    4 weeks ago     
llama3:latest                365c0bd3c000    4.7 GB    4 weeks ago     
llava:latest                 8dd30f6b0cb1    4.7 GB    6 weeks ago     
qwen2.5:3b-instruct          357c53fb659c    1.9 GB    2 months ago    
deepseek-r1:8b               6995872bfe4c    5.2 GB    2 months ago    
gemma2:9b-instruct-q4_0      ff02c3702f32    5.4 GB    3 months ago    
qwen2.5:7b-instruct-q4_0     2e92ac0dd3a8    4.4 GB    3 months ago    
llama3.1:8b-instruct-q4_0    42182419e950    4.7 GB    3 months ago    
qwen2.5-coder:7b             dae161e27b0e    4.7 GB    4 months ago    
josevicente@josevicenteportatil:~$ 

6.-Probar el modelo de descargado (terminal)
ollama run qwen2.5-coder:7b


/exit para salir



