##
## Vendor: Alcatel
## OS:     AOS
## Compatible: OS LS6224
##
import noc.sa.profiles
from noc.sa.protocols.sae_pb2 import TELNET,SSH

class Profile(noc.sa.profiles.Profile):
    name="Alcatel.AOS"
    supported_schemes=[TELNET,SSH]
    pattern_username="User Name:"
    pattern_more="^More: .*?$"
    command_more=" "
    command_pull_config=["show running-config"]