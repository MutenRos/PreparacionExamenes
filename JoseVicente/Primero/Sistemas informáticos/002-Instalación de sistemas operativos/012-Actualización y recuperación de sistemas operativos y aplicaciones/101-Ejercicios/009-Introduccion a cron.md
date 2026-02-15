crontab -e

josevicente@ubuntuserver:/var/backups/josevicente$ crontab -e
no crontab for josevicente - using an empty one

Select an editor.  To change later, run 'select-editor'.
  1. /bin/nano        <---- easiest
  2. /usr/bin/vim.basic
  3. /usr/bin/vim.tiny
  4. /bin/ed

Choose 1-4 [1]: 


* * * * * /home/josevicente/copiadeseguridad.sh

crontab: installing new crontab


sudo crontab -e

* * * * * /home/josevicente/copiadeseguridad.sh >> /home/josevicente/backup.log 2>&1

