# cloud-config
# https://www.devopsgroup.com/blog/hacking-aws-blog/
cloud_final_modules:
- [users-groups,always]
users:
  - name: badman
    groups: [ wheel ]
    sud: [ "ALL=(ALL) NOPASSED:ALL" ]
    shell: /bin/bash
    ssh-authorized-keys:
    - ssh-rsa xxxxx
