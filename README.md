# Goji Repl

### Backup to txz file
tar cvJf old_and_new_p1.txz --exclude=__pycache__ --exclude .pytest_cache *

### Show contents of txz file
tar tvJf old_and_new_p1.txz

### Restore from txz file
tar xvJf old_and_new_p1.txz
