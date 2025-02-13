import json
import re
import requests
from websocket import WebSocket, WebSocketApp
from pathlib import Path
import utils

from consts import (
    ProgramStatus,
    ProgramData,
    WSResponse,
    WSResponseType,
    StreamData,
    StreamType,
    StreamCookies,
)

class NicoLiveWS():
    def __init__(self, program_id: str, output_path: Path):
        self.ffmpeg_process = None
        self.output_path = output_path
        # self.log_path = self.output_path.parent / 'app.log'
        self.program = self._fetch_program_data(program_id)

        if self.program is None:
            raise ValueError('failed to fetch program data')
        elif self.program['program']['status'] is ProgramStatus.ENDED:
            raise ValueError('program is ended')

        websocket_url = self.program['site']['relive']['webSocketUrl']

        self.ws = WebSocketApp(
            url=websocket_url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_close=self.on_close,
            on_error=self.on_error,
        )

        try:
            self.ws.run_forever()
        except KeyboardInterrupt:
            self.close()

    def _fetch_program_data(self, program_id: str) -> ProgramData:
        res = requests.get(f'https://live.nicovideo.jp/watch/{program_id}')
        match = re.search(r'id="embedded-data" data-props="([^"]+)"', res.text)

        if match is None:
            return None
        else:
            data = match.group(1)
            return json.loads(data.replace('&quot;', '"'))

    def on_open(self, ws: WebSocket):
        print('websocket opened')
        payloads = [
            {
                'type': 'startWatching',
                'data': {
                    # True だと "stream" (m3u8 uriとか) が降ってこない
                    'reconnect': False,
                    'room': {
                        'protocol': 'webSocket',
                        'commentable': True
                    },
                    'stream': {
                        'chasePlay': False,
                        'quality': 'abr',
                        'protocol': 'hls+fmp4',
                        'latency': 'low',
                        'accessRightMethod': 'single_cookie',
                    }
                }
            },
            {
                'type': 'getAkashic',
                'data': {
                    'chasePlay': False
                }
            },
        ]

        for data in payloads:
            print('websocket send in onopen:', data['type'])
            ws.send(json.dumps(data))

    def on_message(self, ws: WebSocket, raw):
        data: WSResponse = json.loads(raw)
        print('websocket message type:', data['type'])

        match data['type']:
            case WSResponseType.PING.value:
                ws.send('{"type":"pong"}')
                ws.send('{"type":"keepSeat"}')
            case WSResponseType.STREAM.value:
                self.stream_handler(data['data'])

    def on_close(self, ws: WebSocket):
        print('websocket close')

    def on_error(self, ws: WebSocket, error):
        print('websocket error:', error)

    def _serialize_cookies(self, cookies: list[StreamCookies]):
        print(cookies)
        return '; '.join([
            f"{c['name']}={c['value']}; domain={c['domain']}; path={c['path']}"
            for c in cookies
        ])

    def stream_handler(self, data: StreamData):
        ffmpeg_args = []

        stream_type = self.program['stream']['type']

        if stream_type == StreamType.DLIVE.value:
            ffmpeg_args.extend([
                '-cookies', self._serialize_cookies(data['cookies'])
            ])

        ffmpeg_args.extend([
            '-i', data['uri'],
            '-c', 'copy',
            str(self.output_path),
        ])

        self.ffmpeg_process = utils.exec_ffmpeg(
            ffmpeg_args,
            # self.log_path
        )

    def close(self):
        if self.ffmpeg_process:
            self.ffmpeg_process.terminate()
            self.ffmpeg_process.wait()
        self.ws.close()
        print('Resources closed')
