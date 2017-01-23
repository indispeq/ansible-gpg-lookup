# ansible-gpg-lookup
Ansible gpg lookup plugin


Usage:
`rabbitmq_users: "{{ lookup('gpg', 'rabbitmq.yml.asc')['rabbitmq_users'] }}"`

Clone the repo, add the path to the `[defaults]` section of your `ansible.cfg`:

`lookup_plugins = ./lookup_plugins`

## GOTCHAS
- If you receive a 'number of arguments' error, please make sure that your encrypted
files have been encrypted with `--armor`, binary format files will not work
