# ansible-gpg-lookup
Ansible gpg lookup plugin


Usage:
`rabbitmq_users: "{{ lookup('gpg', 'rabbitmq.yml.asc')['rabbitmq_users'] }}"`

Clone the repo, add the path to the `[defaults]` section of your `ansible.cfg`:

`lookup_plugins = ./lookup_plugins`
