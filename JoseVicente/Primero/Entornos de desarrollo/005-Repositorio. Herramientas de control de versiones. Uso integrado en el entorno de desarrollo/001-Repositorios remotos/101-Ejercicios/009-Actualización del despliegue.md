1.-Primero realizo un cambio en local

2.-Hago commit y push

Primera ventaja: tengo versiones
Tengo una memoria de todo lo que ha ocurrido, y eso quiere decir que podría volver atrás

3.-Pero ahora accedo al servidor y traigo esa nueva versión

josevicente@ubuntuserver:/var/www/html/miweb$ sudo git fetch
remote: Enumerating objects: 5, done.
remote: Counting objects: 100% (5/5), done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 3 (delta 0), reused 3 (delta 0), pack-reused 0 (from 0)
Unpacking objects: 100% (3/3), 363 bytes | 181.00 KiB/s, done.
From https://github.com/jocarsa/miweb
   68acb5f..92eefe7  main       -> origin/main
josevicente@ubuntuserver:/var/www/html/miweb$ 
josevicente@ubuntuserver:/var/www/html/miweb$ sudo git pull origin main

josevicente@ubuntuserver:/var/www/html/miweb$ sudo git pull origin main
From https://github.com/jocarsa/miweb
 * branch            main       -> FETCH_HEAD
Updating 68acb5f..92eefe7
Fast-forward
 index.html | 1 +
 1 file changed, 1 insertion(+)
josevicente@ubuntuserver:/var/www/html/miweb$ 
