"""
Device controller module.
Provides services to monitor and operate device's system.
"""
from threading import Thread
from client.board_controller.system_monitor import SystemMonitor


system_monitor = SystemMonitor()

system_monitor_thread = Thread(target=system_monitor.run)
system_monitor_thread.start()
