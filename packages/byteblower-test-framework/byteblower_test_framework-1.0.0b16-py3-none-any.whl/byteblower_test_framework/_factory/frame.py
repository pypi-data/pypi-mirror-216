"""Module for simplified Frame creation."""
from typing import Any, Mapping, Optional  # for type hinting

from .._endpoint.ipv4.port import IPv4Port
from .._endpoint.ipv6.port import IPv6Port
from .._endpoint.port import Port  # for type hinting
from .._traffic.frame import \
    DEFAULT_FRAME_LENGTH  # pylint: disable=unused-import; used in docstring
from .._traffic.frame import \
    UDP_DYNAMIC_PORT_START  # pylint: disable=unused-import; used in docstring
from .._traffic.frame import Frame  # for type hinting
from .._traffic.ipv4.frame import IPv4Frame
from .._traffic.ipv6.frame import IPv6Frame

FrameConfig = Mapping[str, Any]


def create_frame(
    source_port: Port,
    length: Optional[int] = None,
    udp_src: Optional[int] = None,
    udp_dest: Optional[int] = None,
    ip_tos: Optional[int] = None,
    latency_tag: bool = False
) -> Frame:
    """Create a frame based on the (source) Port type.

    :param source_port: Port which will be transmitting the Frame.
       Used to identify which Frame implementation we need
       (:class:`~traffic.IPv4Frame` or :class:`~traffic.IPv6Frame`)
    :type source_port: Port
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
    :param ip_tos: IPv4 TOS field, defaults to `DEFAULT_IPV4_TOS`
       for an `IPv4Frame`.

       .. warning:: Should not be given overridden for IPv6.
    :type ip_tos: Optional[int], optional
    :param latency_tag: Enable latency tag generation in the Frame,
       defaults to ``False``
    :type latency_tag: bool, optional
    :raises ValueError: When an unknown Port implementation is given.
    :raises ValueError: When providing ``ip_tos`` for IPv6
    :raises ValueError: When an invalid frame length is given.
    :return: New instance of an IPv4 or IPv6 Frame interface
    :rtype: Frame
    """
    if isinstance(source_port, IPv4Port):
        return IPv4Frame(
            length=length,
            udp_src=udp_src,
            udp_dest=udp_dest,
            ip_tos=ip_tos,
            latency_tag=latency_tag
        )

    if isinstance(source_port, IPv6Port):
        if ip_tos is not None:
            raise ValueError('IP ToS is not supported for IPv6 frames.')
        return IPv6Frame(
            length=length,
            udp_src=udp_src,
            udp_dest=udp_dest,
            latency_tag=latency_tag
        )

    raise ValueError('Unsupported Port type')
