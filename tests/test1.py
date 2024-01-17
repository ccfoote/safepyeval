import safepyeval


code = '''
admin_user_ids = ['magland', 'admin']
max_num_cpus_for_admin = 8
max_num_cpus_for_privileged_users = 4
other_users = {
    'user3': {
        'max_num_cpus': 2
    },
    'user4': {
        'max_num_cpus': 1
    }
}
if userId in admin_user_ids and not userId == 'magland':
    if nCpus <= max_num_cpus_for_admin:
        return True
    else:
        return False
elif userId in ['user1', 'user2']:
    if nCpus <= max_num_cpus_for_privileged_users:
        return True
    else:
        return False
else:
    if userId in other_users:
        if nCpus <= other_users[userId]['max_num_cpus']:
            return True
        else:
            return False
    else:
        return False
'''

data = {
    'userId': 'user1',
    'nCpus': 4
}

result = safepyeval.evaluate(code, data)
print(result)
