"""IPv4 Frame interface module."""
import logging
from typing import Optional, Union  # for type hinting

# XXX - Causes circular import with scapy 2.4.5 on macOS Monterey:
# Similar to https://github.com/secdev/scapy/issues/3246
# from scapy.layers.inet import IP, UDP
# from scapy.layers.l2 import Ether
from scapy.all import IP, UDP, Ether
from scapy.packet import Raw

from ..._endpoint.ipv4.nat import NattedPort  # for type hinting
from ..._endpoint.ipv4.port import IPv4Port  # for type hinting
from ..frame import ETHERNET_HEADER_LENGTH, UDP_HEADER_LENGTH, Frame

IPV4_HEADER_LENGTH: int = 20

IPV4_FULL_HEADER_LENGTH: int = (
    ETHERNET_HEADER_LENGTH +  # noqa: W504
    IPV4_HEADER_LENGTH + UDP_HEADER_LENGTH
)
assert IPV4_FULL_HEADER_LENGTH == 42, 'Incorrect IPv4 full header length'

DEFAULT_IPV4_TOS: int = 0x00


class IPv4Frame(Frame):
    """Frame interface for IPv4."""

    __slots__ = ('_ip_tos', )

    def __init__(
        self,
        length: Optional[int] = None,
        udp_src: Optional[int] = None,
        udp_dest: Optional[int] = None,
        ip_tos: Optional[int] = None,
        latency_tag: bool = False
    ) -> None:
        """Create the interface to an IPv4 frame.

        :param length: Frame length. This is the layer 2 (Ethernet) frame length
           *excluding* Ethernet FCS and *excluding* VLAN tags,
           defaults to :const:`DEFAULT_FRAME_LENGTH`
        :type length: int, optional
        :param udp_src: UDP source port, defaults to
           :const:`UDP_DYNAMIC_PORT_START`
        :type udp_src: int, optional
        :param udp_dest: UDP destination port, defaults to
           :const:`UDP_DYNAMIC_PORT_START`
        :type udp_dest: int, optional
        :param ip_tos: IPv4 TOS field, defaults to :const:`DEFAULT_IPV4_TOS`
        :type ip_tos: Optional[int], optional
        :param latency_tag: Enable latency tag generation in the Frame,
           defaults to ``False``
        :type latency_tag: bool, optional
        :raises ValueError: When an invalid frame length is given.
        """
        super().__init__(
            IPV4_FULL_HEADER_LENGTH, length, udp_src, udp_dest, latency_tag
        )

        if ip_tos is None:
            self._ip_tos = DEFAULT_IPV4_TOS
        else:
            self._ip_tos = ip_tos

    def _build_frame_content(
        self, source_port: Union[IPv4Port, NattedPort],
        destination_port: Union[IPv4Port, NattedPort]
    ) -> Ether:
        udp_dest = self._udp_dest
        udp_src = self._udp_src
        ip_dest = destination_port.layer3.IpGet()
        ip_src = source_port.layer3.IpGet()
        ip_tos = self._ip_tos

        if destination_port.is_natted:
            nat_info = destination_port.nat_discover(
                source_port,
                public_udp_port=self._udp_src,
                nat_udp_port=self._udp_dest
            )
            logging.debug('NAT translation: %r', nat_info)
            ip_dest, udp_dest = nat_info

        mac_src = source_port.mac
        mac_dst = source_port.layer3.Resolve(ip_dest)

        scapy_layer2_5_headers = self._build_layer2_5_headers(source_port)

        payload = self._build_payload(IPV4_FULL_HEADER_LENGTH)

        scapy_udp_payload = Raw(payload.encode('ascii', 'strict'))
        scapy_udp_header = UDP(dport=udp_dest, sport=udp_src)
        scapy_ip_header = IP(src=ip_src, dst=ip_dest, tos=ip_tos)
        scapy_ethernet_header = Ether(src=mac_src, dst=mac_dst)
        for scapy_layer2_5_header in scapy_layer2_5_headers:
            scapy_ethernet_header /= scapy_layer2_5_header
        scapy_frame = (
            scapy_ethernet_header / scapy_ip_header / scapy_udp_header /
            scapy_udp_payload
        )

        return scapy_frame
