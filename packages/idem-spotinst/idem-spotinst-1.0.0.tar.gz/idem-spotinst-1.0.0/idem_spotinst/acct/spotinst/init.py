async def gather(hub, profiles):
    """
    load profiles from unencrypted spotinst credential files

    Example:
    .. code-block:: yaml

        spotinst:

          default:
            account_id: act-d60b6ecd
            token: XXXXXXXX
          test_development_idem_spotinst:
            use_ssl: True
            account_id: act-d60b6ecd
            token: XXXXXXXXXXXX

    """
    sub_profiles = {}
    for profile, ctx in profiles.get("spotinst", {}).items():
        sub_profiles[profile] = ctx

    return sub_profiles
