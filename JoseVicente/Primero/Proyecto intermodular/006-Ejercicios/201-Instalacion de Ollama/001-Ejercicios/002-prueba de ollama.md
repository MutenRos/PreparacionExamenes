ollama pull qwen2.5:7b

ollama run qwen2.5 "Hola, ¿qué puedes hacer?"

ollama list - listado de los modelos instalados

enguajes de marcas/004-Herramientas de creación y validación/101-Ejercicios$ ollama list
NAME                         ID              SIZE      MODIFIED     
qwen2.5:3b-instruct          357c53fb659c    1.9 GB    3 weeks ago     
deepseek-r1:8b               6995872bfe4c    5.2 GB    4 weeks ago     
gemma2:9b-instruct-q4_0      ff02c3702f32    5.4 GB    7 weeks ago     
qwen2.5:7b-instruct-q4_0     2e92ac0dd3a8    4.4 GB    7 weeks ago     
llama3.1:8b-instruct-q4_0    42182419e950    4.7 GB    8 weeks ago     
qwen2.5-coder:7b             dae161e27b0e    4.7 GB    2 months ago   


ollama run qwen2.5:3b-instruct "Hola, ¿qué puedes hacer?"

ollama run qwen2.5:3b-instruct "¿Qué es CSS?"

ollama run qwen2.5-coder:7b "Hazme una web html y css muy basica"


