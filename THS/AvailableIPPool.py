from pytdx.pool.ippool import AvailableIPPool as BasePool


class AvailableIPPool(BasePool):
    def __init__(self, hq_class, ips):
        super(AvailableIPPool, self).__init__(hq_class, ips)
        self.next_ip_pos = 0

    def teardown(self):
        self.stop_event.set()
        if self.worker_thread and self.worker_thread.is_alive():
            self.worker_thread.join()
        self.worker_thread = None

    def get_next_ip(self):
        if self.next_ip_pos >= len(self.ips) or self.next_ip_pos < 0:
            return None
        r = self.ips[self.next_ip_pos]
        self.next_ip_pos = (self.next_ip_pos + 1) % len(self.ips)
        return r
