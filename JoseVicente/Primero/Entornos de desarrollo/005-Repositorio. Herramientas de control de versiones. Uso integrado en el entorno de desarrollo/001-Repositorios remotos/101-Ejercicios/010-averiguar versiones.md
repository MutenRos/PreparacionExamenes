git fetch --tags

git config --global --add safe.directory /var/www/html/miweb

curl -s https://api.github.com/repos/jocarsa/miweb/tags

# Ver todas las versiones

sudo git log --oneline --graph --decorate --all

#Revertir a una versión anterior
git revert 68acb5f

# Si hay conflictos, forzar reversión

git add index.html
git revert --continue
