from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'^id.clarosnet.org$', 'voyager.urls.id', name='id'),
    host(r'^data.clarosnet.org$', 'voyager.urls.data', name='data'),
    host(r'^admin.data.clarosnet.org$', 'voyager.urls.admin', name='admin'),
    host(r'$x^', 'voyager.urls.empty', name='empty'),
)
