import json, base64, pathlib, mimetypes, os
har = json.load(open('milady_layers.har'))
out = pathlib.Path('dump')
out.mkdir(exist_ok=True)
for e in har['log']['entries']:
    url = e['request']['url']
    mime = e['response']['content'].get('mimeType','')
    if 'image' not in mime:
        continue
    body = e['response']['content'].get('text','')
    if e['response']['content'].get('encoding') == 'base64':
        data = base64.b64decode(body)
    else:
        data = body.encode()
    fname = url.split('/')[-1].split('?')[0] or f"file_{os.urandom(4).hex()}" 
    (out/fname).write_bytes(data)
print('Done – files in', out)