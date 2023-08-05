from aiokafka.helpers import create_ssl_context


async def gather(hub, profiles):
    """
    Create an ssl context for the connection based on sls parameters

    Example:
    .. code-block:: yaml

        kafka:
          profile_name:
            topics:
              - topic1
            connection:
              bootstrap_servers:
                - 'localhost:9092'
            ssl:
              ca_file: <path to the Certificate Authority file containing certificates used to sign broker certificates>
              cert_file: <optional: path to the file in PEM format containing the client certificate>
              key_file: <optional: path to the file containing the client private key>
              password: <optional: password to be used when loading the certificate chain>
    """

    for profile in profiles.get("kafka", {}):
        # create the ssl context
        ctx = profiles["kafka"][profile]
        if "ssl" in ctx:
            ssl = ctx["ssl"]
            try:
                ca_file = ssl["ca_file"]
                cert_file = ssl["cert_file"]
                key_file = ssl["key_file"]
                password = ssl["password"]
                context = create_ssl_context(
                    cafile=ca_file,
                    certfile=cert_file,
                    keyfile=key_file,
                    password=password,
                )
                ctx["connection"]["ssl_context"] = context
                ctx["connection"]["ssl_context"].check_hostname = False
                ctx["connection"]["ssl_context"].hostname_checks_common_name = False
                ctx["connection"]["security_protocol"] = "SSL"
            except KeyError:
                hub.log.error("Failed to generate ssl context")

    return {}
