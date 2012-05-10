def base_template_chooser(request):
    hosts = {'admin': 'hosts/admin.html',
             'data': 'hosts/data.html'}
    
    return {'base_template_name': hosts.get(request.host.name, hosts['data'])}
