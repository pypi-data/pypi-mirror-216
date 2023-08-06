from xia_fields import StringField


class EmailField(StringField):
    """Email address field"""
    def __init__(self,
                 description="Email field",
                 sample="name@domain.com",
                 regex="(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                 **kwargs):
        super().__init__(description=description, sample=sample, regex=regex, **kwargs)


class IpField(StringField):
    """IP address (v4) field"""
    def __init__(self,
                 description="Ip Address field",
                 sample="123.45.67.89",
                 regex="^(?:(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])(\.(?!$)|$)){4}$",
                 **kwargs):
        super().__init__(description=description, sample=sample, regex=regex, **kwargs)


class IpV6Field(StringField):
    """IP address (v6) field"""
    def __init__(self,
                 description="Ip Address field",
                 sample="2404:6800:4003:c02::8a",
                 regex="(?:^|(?<=\s))(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]"
                       "{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]"
                       "{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}"
                       "|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4})"
                       "{1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}"
                       "|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]"
                       "|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9])"
                       "{0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))(?=\s|$)",
                 **kwargs):
        super().__init__(description=description, sample=sample, regex=regex, **kwargs)


class MacField(StringField):
    """Mac address (v4) field"""
    def __init__(self,
                 description="Ip Address field",
                 sample="01:23:45:67:89:AB",
                 regex="^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$",
                 **kwargs):
        super().__init__(description=description, sample=sample, regex=regex, **kwargs)
