# Description

Tools for Making my Ansible Roles more Consistent

# How To Use

```bash
for r in `find . -iname "ansible-role-*" -and -not -iname "*skeleton*" -type d`; \
do \
  ../ansible-tools/venv/bin/python3 ../ansible-tools/generate.py -r "${r}" -a; \
done
```