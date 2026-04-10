from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

def _handle_PacketIn(event):
    # Create a packet-out message
    msg = of.ofp_packet_out()
    msg.data = event.ofp

    # Flood packet to all ports
    msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))

    # Send to switch
    event.connection.send(msg)

    log.info("Packet received and flooded")

def launch():
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    log.info("Controller is Running...")
