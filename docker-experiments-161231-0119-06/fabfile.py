from fabric.api import local, run, settings

def gen_ssl_cert(cert_name="cryptic_labs_jovyan"):
  """
  Uses OpenSSL to generate self-signed SSL certificate with configuration given in cert.conf.
  """
  fmt="openssl req -x509 -nodes -days 365 -newkey rsa -config cert.conf -keyout {} -out {}"
  cert="{}.pem".format(cert_name);
  key="{}.key".format(cert_name);
  cmd=fmt.format(key, cert)
  local(cmd)

def 
