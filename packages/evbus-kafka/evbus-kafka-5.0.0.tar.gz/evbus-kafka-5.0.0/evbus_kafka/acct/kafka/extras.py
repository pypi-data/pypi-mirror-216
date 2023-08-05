async def gather(hub, profiles):
    """
    Non-secret values are allowed in a config file:

    .. code-block:: YAML

        acct:
          extras:
            kafka:
              key: my_key
              partition: my_partition
              topics:
                - my_topic1
                - my_topic2
                - my_topic3

    They can also be specified on the cli in json format:

    .. code-block:: bash

        $ my_program --extras="{'kafka':{{'key': 'my_key', 'partition': 'my_partition', 'topics': ['my_topic1', 'my_topic2', 'my_topic3']}}}"
    """
    # Get non-secret values from the config
    extras = hub.OPT.acct.get("extras") or {}
    extra_profile_data = extras.get("kafka", {})

    for profile in profiles.get("kafka", {}):
        # Modify an existing profile
        ctx_acct = profiles["kafka"][profile]
        ctx_acct["key"] = ctx_acct.get("key") or extra_profile_data.get("key")
        ctx_acct["partition"] = ctx_acct.get("partition") or extra_profile_data.get(
            "partition"
        )
        ctx_acct["topics"] = ctx_acct.get("topics") or extra_profile_data.get("topics")

    return {}
