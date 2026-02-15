sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080

Desde fuera accedemos por el puerto 80, pero internamente redirecciona al puerto 8080

NAT 
Network
Access 
Translation

Traducir un puerto a otro, es decir, desde fuera escucha en un puerto, y cuando la llamada entra, redirecciona a otro puerto interno


