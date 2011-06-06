from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'id.clarosnet.org:8000', 'voyager.urls.id', name='id'),
    host(r'data.clarosnet.org:8000', 'voyager.urls.data', name='data'),
    host(r'$x^', 'voyager.urls.empty', name='empty'),
)
