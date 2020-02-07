from .dns import *
from .dnsmaster import *
from .dnsslave import *
from .ftp import *
from .mail import *
from .mailforwarder import *
from .mailprimary import *
from .ipv6 import *
from .web import *


var_classes = [
    DNS,
    DNSMaster,
    DNSSlave,
    FTP,
    Mail,
    MailForwarder,
    MailPrimary,
    VIP6,
    Web,
]
