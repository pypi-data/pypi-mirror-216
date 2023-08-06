import threading

from . import tests_base

import osef
from osef.multi_streamer import MultiOsefStreamer


class TestStreamer(tests_base.BaseTestCase):
    def _read_osef(self, tcp_url, received_timestamps_list):
        for frame_dict in osef.parser.parse(tcp_url, auto_reconnect=False):
            received_timestamps_list.append(
                frame_dict["timestamped_data"]["timestamp_microsecond"]
            )

    def test_stream_osef_file(self):
        received_timestamps_single_streamer = []
        HOSTNAME = "localhost"
        PORT = 11120
        server_thread = threading.Thread(
            target=osef.streamer.stream_osef_file,
            args=[self.SLAM_FILEPATH, HOSTNAME, PORT],
        )
        client_thread = threading.Thread(
            target=self._read_osef,
            args=[f"tcp://{HOSTNAME}:{PORT}", received_timestamps_single_streamer],
        )
        server_thread.start()
        client_thread.start()
        server_thread.join()
        client_thread.join()

        timestamps = []
        for frame_dict in osef.parser.parse(self.SLAM_FILEPATH):
            timestamps.append(frame_dict["timestamped_data"]["timestamp_microsecond"])
        self.assertListEqual(timestamps, received_timestamps_single_streamer)

    def test_multi_osef_streamer(self):
        received_timestamps_multi_1 = []
        received_timestamps_multi_2 = []

        HOSTNAME = "127.0.0.1"
        FIRST_PORT = 11111
        SECOND_PORT = 11112
        osef_list = [
            {"osef_path": self.SLAM_FILEPATH, "ip": HOSTNAME, "port": FIRST_PORT},
            {"osef_path": self.SLAM_FILEPATH, "ip": HOSTNAME, "port": SECOND_PORT},
        ]
        client_thread_1 = threading.Thread(
            target=self._read_osef,
            args=[f"tcp://{HOSTNAME}:{FIRST_PORT}", received_timestamps_multi_1],
        )
        client_thread_2 = threading.Thread(
            target=self._read_osef,
            args=[f"tcp://{HOSTNAME}:{SECOND_PORT}", received_timestamps_multi_2],
        )
        client_thread_1.start()
        client_thread_2.start()
        with MultiOsefStreamer(osef_list) as multi_streamer:
            multi_streamer.run()
        client_thread_1.join()
        client_thread_2.join()
        timestamps = []
        for frame_dict in osef.parser.parse(self.SLAM_FILEPATH):
            timestamps.append(frame_dict["timestamped_data"]["timestamp_microsecond"])
        self.assertListEqual(timestamps, received_timestamps_multi_1)

        timestamps = []
        for frame_dict in osef.parser.parse(self.SLAM_FILEPATH):
            timestamps.append(frame_dict["timestamped_data"]["timestamp_microsecond"])
        self.assertListEqual(timestamps, received_timestamps_multi_2)
