josevicente@ubuntuserver:/var/www/html/miweb$ sudo git revert --continue
Author identity unknown

*** Please tell me who you are.

Run

  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"

to set your account's default identity.
Omit --global to set the identity only in this repository.

fatal: unable to auto-detect email address (got 'root@ubuntuserver.(none)')
josevicente@ubuntuserver:/var/www/html/miweb$ git config --global user.email "info@josevicentecarratala.com"
josevicente@ubuntuserver:/var/www/html/miweb$ git config --global user.name "jocarsa"
warning: user.name has multiple values
error: cannot overwrite multiple values with a single value
       Use a regexp, --add or --replace-all to change user.name.
josevicente@ubuntuserver:/var/www/html/miweb$ git config --global --replace-all user.name "jocarsa"
josevicente@ubuntuserver:/var/www/html/miweb$ git config --global user.name
jocarsa
josevicente@ubuntuserver:/var/www/html/miweb$ git config --global user.email
info@josevicentecarratala.com
josevicente@ubuntuserver:/var/www/html/miweb$ sudo git revert --continue
Author identity unknown

*** Please tell me who you are.

Run

  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"

to set your account's default identity.
Omit --global to set the identity only in this repository.

fatal: unable to auto-detect email address (got 'root@ubuntuserver.(none)')
josevicente@ubuntuserver:/var/www/html/miweb$ 

