# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[('templates', 'templates'), ('static', 'static')],
    hiddenimports=['dns', 'dns._asyncbackend', 'dns._asyncio_backend', 'dns._ddr', 'dns._features', 'dns._immutable_ctx', 'dns._no_ssl', 'dns._tls_util', 'dns._trio_backend', 'dns.asyncbackend', 'dns.asyncquery', 'dns.asyncresolver', 'dns.btree', 'dns.btreezone', 'dns.dnssec', 'dns.dnssecalgs', 'dns.dnssecalgs.base', 'dns.dnssecalgs.cryptography', 'dns.dnssecalgs.dsa', 'dns.dnssecalgs.ecdsa', 'dns.dnssecalgs.eddsa', 'dns.dnssecalgs.rsa', 'dns.dnssectypes', 'dns.e164', 'dns.edns', 'dns.entropy', 'dns.enum', 'dns.exception', 'dns.flags', 'dns.grange', 'dns.immutable', 'dns.inet', 'dns.ipv4', 'dns.ipv6', 'dns.message', 'dns.name', 'dns.namedict', 'dns.nameserver', 'dns.node', 'dns.opcode', 'dns.query', 'dns.quic', 'dns.quic._asyncio', 'dns.quic._common', 'dns.quic._sync', 'dns.quic._trio', 'dns.rcode', 'dns.rdata', 'dns.rdataclass', 'dns.rdataset', 'dns.rdatatype', 'dns.rdtypes', 'dns.rdtypes.ANY', 'dns.rdtypes.ANY.AFSDB', 'dns.rdtypes.ANY.AMTRELAY', 'dns.rdtypes.ANY.AVC', 'dns.rdtypes.ANY.CAA', 'dns.rdtypes.ANY.CDNSKEY', 'dns.rdtypes.ANY.CDS', 'dns.rdtypes.ANY.CERT', 'dns.rdtypes.ANY.CNAME', 'dns.rdtypes.ANY.CSYNC', 'dns.rdtypes.ANY.DLV', 'dns.rdtypes.ANY.DNAME', 'dns.rdtypes.ANY.DNSKEY', 'dns.rdtypes.ANY.DS', 'dns.rdtypes.ANY.DSYNC', 'dns.rdtypes.ANY.EUI48', 'dns.rdtypes.ANY.EUI64', 'dns.rdtypes.ANY.GPOS', 'dns.rdtypes.ANY.HINFO', 'dns.rdtypes.ANY.HIP', 'dns.rdtypes.ANY.ISDN', 'dns.rdtypes.ANY.L32', 'dns.rdtypes.ANY.L64', 'dns.rdtypes.ANY.LOC', 'dns.rdtypes.ANY.LP', 'dns.rdtypes.ANY.MX', 'dns.rdtypes.ANY.NID', 'dns.rdtypes.ANY.NINFO', 'dns.rdtypes.ANY.NS', 'dns.rdtypes.ANY.NSEC', 'dns.rdtypes.ANY.NSEC3', 'dns.rdtypes.ANY.NSEC3PARAM', 'dns.rdtypes.ANY.OPENPGPKEY', 'dns.rdtypes.ANY.OPT', 'dns.rdtypes.ANY.PTR', 'dns.rdtypes.ANY.RESINFO', 'dns.rdtypes.ANY.RP', 'dns.rdtypes.ANY.RRSIG', 'dns.rdtypes.ANY.RT', 'dns.rdtypes.ANY.SMIMEA', 'dns.rdtypes.ANY.SOA', 'dns.rdtypes.ANY.SPF', 'dns.rdtypes.ANY.SSHFP', 'dns.rdtypes.ANY.TKEY', 'dns.rdtypes.ANY.TLSA', 'dns.rdtypes.ANY.TSIG', 'dns.rdtypes.ANY.TXT', 'dns.rdtypes.ANY.URI', 'dns.rdtypes.ANY.WALLET', 'dns.rdtypes.ANY.X25', 'dns.rdtypes.ANY.ZONEMD', 'dns.rdtypes.CH', 'dns.rdtypes.CH.A', 'dns.rdtypes.IN', 'dns.rdtypes.IN.A', 'dns.rdtypes.IN.AAAA', 'dns.rdtypes.IN.APL', 'dns.rdtypes.IN.DHCID', 'dns.rdtypes.IN.HTTPS', 'dns.rdtypes.IN.IPSECKEY', 'dns.rdtypes.IN.KX', 'dns.rdtypes.IN.NAPTR', 'dns.rdtypes.IN.NSAP', 'dns.rdtypes.IN.NSAP_PTR', 'dns.rdtypes.IN.PX', 'dns.rdtypes.IN.SRV', 'dns.rdtypes.IN.SVCB', 'dns.rdtypes.IN.WKS', 'dns.rdtypes.dnskeybase', 'dns.rdtypes.dsbase', 'dns.rdtypes.euibase', 'dns.rdtypes.mxbase', 'dns.rdtypes.nsbase', 'dns.rdtypes.svcbbase', 'dns.rdtypes.tlsabase', 'dns.rdtypes.txtbase', 'dns.rdtypes.util', 'dns.renderer', 'dns.resolver', 'dns.reversename', 'dns.rrset', 'dns.serial', 'dns.set', 'dns.tokenizer', 'dns.transaction', 'dns.tsig', 'dns.tsigkeyring', 'dns.ttl', 'dns.update', 'dns.version', 'dns.versioned', 'dns.win32util', 'dns.wire', 'dns.xfr', 'dns.zone', 'dns.zonefile', 'dns.zonetypes', 'eventlet', 'eventlet._version', 'eventlet.asyncio', 'eventlet.backdoor', 'eventlet.convenience', 'eventlet.corolocal', 'eventlet.coros', 'eventlet.dagpool', 'eventlet.db_pool', 'eventlet.debug', 'eventlet.event', 'eventlet.green', 'eventlet.green.BaseHTTPServer', 'eventlet.green.CGIHTTPServer', 'eventlet.green.MySQLdb', 'eventlet.green.Queue', 'eventlet.green.SimpleHTTPServer', 'eventlet.green.SocketServer', 'eventlet.green._socket_nodns', 'eventlet.green.asynchat', 'eventlet.green.asyncore', 'eventlet.green.builtin', 'eventlet.green.ftplib', 'eventlet.green.http', 'eventlet.green.http.client', 'eventlet.green.http.cookiejar', 'eventlet.green.http.cookies', 'eventlet.green.http.server', 'eventlet.green.httplib', 'eventlet.green.os', 'eventlet.green.profile', 'eventlet.green.select', 'eventlet.green.selectors', 'eventlet.green.socket', 'eventlet.green.ssl', 'eventlet.green.subprocess', 'eventlet.green.thread', 'eventlet.green.threading', 'eventlet.green.time', 'eventlet.green.urllib', 'eventlet.green.urllib.error', 'eventlet.green.urllib.parse', 'eventlet.green.urllib.request', 'eventlet.green.urllib.response', 'eventlet.green.urllib2', 'eventlet.green.zmq', 'eventlet.greenio', 'eventlet.greenio.base', 'eventlet.greenio.py3', 'eventlet.greenpool', 'eventlet.greenthread', 'eventlet.hubs', 'eventlet.hubs.asyncio', 'eventlet.hubs.epolls', 'eventlet.hubs.hub', 'eventlet.hubs.kqueue', 'eventlet.hubs.poll', 'eventlet.hubs.pyevent', 'eventlet.hubs.selects', 'eventlet.hubs.timer', 'eventlet.lock', 'eventlet.patcher', 'eventlet.pools', 'eventlet.queue', 'eventlet.semaphore', 'eventlet.support', 'eventlet.support.greendns', 'eventlet.support.greenlets', 'eventlet.support.psycopg2_patcher', 'eventlet.support.pylib', 'eventlet.support.stacklesspypys', 'eventlet.support.stacklesss', 'eventlet.timeout', 'eventlet.tpool', 'eventlet.websocket', 'eventlet.wsgi', 'eventlet.zipkin', 'eventlet.zipkin._thrift', 'eventlet.zipkin._thrift.zipkinCore', 'eventlet.zipkin._thrift.zipkinCore.constants', 'eventlet.zipkin._thrift.zipkinCore.ttypes', 'eventlet.zipkin.api', 'eventlet.zipkin.client', 'eventlet.zipkin.greenthread', 'eventlet.zipkin.http', 'eventlet.zipkin.log', 'eventlet.zipkin.patcher', 'eventlet.zipkin.wsgi', 'engineio', 'engineio.async_client', 'engineio.async_drivers', 'engineio.async_drivers._websocket_wsgi', 'engineio.async_drivers.aiohttp', 'engineio.async_drivers.asgi', 'engineio.async_drivers.eventlet', 'engineio.async_drivers.gevent', 'engineio.async_drivers.gevent_uwsgi', 'engineio.async_drivers.sanic', 'engineio.async_drivers.threading', 'engineio.async_drivers.tornado', 'engineio.async_server', 'engineio.async_socket', 'engineio.base_client', 'engineio.base_server', 'engineio.base_socket', 'engineio.client', 'engineio.exceptions', 'engineio.json', 'engineio.middleware', 'engineio.packet', 'engineio.payload', 'engineio.server', 'engineio.socket', 'engineio.static_files'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='MapleChatroom',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
