"""IPv6 Frame interface module."""
from typing import Optional

from scapy.layers.inet6 import UDP, Ether, IPv6
from scapy.packet import Raw

from ..._endpoint.ipv6.port import IPv6Port  # for type hinting
from ..frame import (
    DEFAULT_FRAME_LENGTH,
    ETHERNET_HEADER_LENGTH,
    UDP_DYNAMIC_PORT_START,
    UDP_HEADER_LENGTH,
    Frame,
)

IPV6_HEADER_LENGTH: int = 40

IPV6_FULL_HEADER_LENGTH = (
    ETHERNET_HEADER_LENGTH +  # noqa: W504
    IPV6_HEADER_LENGTH + UDP_HEADER_LENGTH
)
assert IPV6_FULL_HEADER_LENGTH == 62, 'Incorrect IPv6 full header length'

DEFAULT_IPV6_TC: int = 0x00


class IPv6Frame(Frame):
    """Frame interface for IPv6."""

    __slots__ = ("_ip_tc", )

    def __init__(
        self,
        length: Optional[int] = None,
        udp_src: Optional[int] = None,
        udp_dest: Optional[int] = None,
        ip_tc: Optional[int] = None,
        latency_tag: bool = False
    ) -> None:
        """Create the interface to an IPv6 frame.

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
        :param ip_tc: IPv6 Traffic Class field, defaults to
           :const:`DEFAULT_IPV6_TC`
        :type ip_tc: Optional[int], optional
        :param latency_tag: Enable latency tag generation in the Frame,
           defaults to ``False``
        :type latency_tag: bool, optional
        :raises ValueError: When an invalid frame length is given.
        """
        super().__init__(
            IPV6_FULL_HEADER_LENGTH, length, udp_src, udp_dest, latency_tag
        )

        if ip_tc is None:
            self._ip_tc = DEFAULT_IPV6_TC
        else:
            self._ip_tc = ip_tc

    def _build_frame_content(
        self, source_port: IPv6Port, destination_port: IPv6Port
    ) -> Ether:
        udp_dest = self._udp_dest
        udp_src = self._udp_src
        # ip_dest = destination_port.layer3.IpDhcpGet()
        # ip_src = source_port.layer3.IpDhcpGet()
        ip_dest = str(destination_port.ip)
        ip_src = str(source_port.ip)
        ip_tc = self._ip_tc
        mac_src = source_port.mac
        mac_dst = source_port.layer3.Resolve(ip_dest)

        scapy_layer2_5_headers = self._build_layer2_5_headers(source_port)

        payload = self._build_payload(IPV6_FULL_HEADER_LENGTH)

        scapy_udp_payload = Raw(payload.encode('ascii', 'strict'))
        scapy_udp_header = UDP(dport=udp_dest, sport=udp_src)
        scapy_ip_header = IPv6(src=ip_src, dst=ip_dest, tc=ip_tc)
        scapy_ethernet_header = Ether(src=mac_src, dst=mac_dst)
        for scapy_layer2_5_header in scapy_layer2_5_headers:
            scapy_ethernet_header /= scapy_layer2_5_header
        scapy_frame = (
            scapy_ethernet_header / scapy_ip_header / scapy_udp_header /
            scapy_udp_payload
        )

        return scapy_frame
