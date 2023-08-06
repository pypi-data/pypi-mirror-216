import asyncio
import json
from typing import Type
from datetime import datetime
import random
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi import HTTPException
from xia_engine import Acl, Base
from xia_broadcast import Broadcaster
from xia_logger import Logger


class BroadcasterFastapi(Broadcaster):
    @classmethod
    async def accept(cls, websocket):
        await asyncio.sleep(random.random())  # Avoiding flood attack
        await websocket.accept()

    @classmethod
    async def send_message_async(cls, websocket, message: str):
        await websocket.send_text(message)

    @classmethod
    def subscriber_is_connected(cls, websocket):
        return True if websocket.application_state.name == "CONNECTED" else False

    @classmethod
    def get_fastapi_api(cls,
                        ws_endpoint: str,
                        logger_class: Type[Logger],
                        logger_param: dict,
                        class_list: list = None,
                        auth_client=None):
        """Get Websocket Endpoint of Fastapi (root)

        Args:
            ws_endpoint: Websocket endpoint path
            logger_class: The class of logger to pull data from
            logger_param (dict): The logger parameter to be passed to logger stream pull function
            class_list (list): Predefined accepted class names
            auth_client: Authorization client. None means no security check

        Returns:
            app object of Fastapi
        """
        app = FastAPI()

        @app.websocket(f"/{ws_endpoint}")
        async def websocket_endpoint(websocket: WebSocket):
            # Step 1: Http handshake to Websocket handshake
            await cls.accept(websocket)
            # Step 2: Get connection information from the first request
            try:
                connection_info = await asyncio.wait_for(websocket.receive_text(), timeout=10)
                connection_params = json.loads(connection_info)
            except asyncio.TimeoutError:
                await websocket.close(code=4400, reason=f"Need connection information")
                return
            except json.JSONDecodeError:
                await websocket.close(code=4400, reason=f"Connection information should be a Json string")
                return
            # Step 3: Get ACL from APL
            header_info = connection_params.pop("_header", {})
            if auth_client:  # When auth client is defined, API key must be provided in header
                api_id = header_info.get("X-Api-Id", None)
                api_key = header_info.get("X-Api-Key", None)
                app_name = header_info.get("X-App-Name", None)
                if not api_key or not app_name:
                    await websocket.close(code=4401, reason=f"App Name or API Key missing for authentication")
                    return
                else:
                    api_detail, status_code = auth_client.get_api_acl(api_key, app_name, api_id)
                    if status_code == 200:
                        user_name = api_detail["user_name"]
                        acl = Acl.from_display(**api_detail["acl"])
                    else:
                        await websocket.close(code=4401,
                                              reason=f"Authentication Error: {status_code}")
                        return
            else:  # No auth_client means public access
                user_name = "Anonymous"
                acl = None
            # Step 4: Subscription
            subscribed = {}
            for class_name, sub_info in connection_params.items():
                if class_list and class_name not in class_list:  # Simply check if class name is listed or not
                    continue
                sub_info.update({"acl": acl, "user_name": user_name, "start_time": datetime.now().timestamp()})
                subscribed[class_name] = await cls.subscribe(websocket, class_name, **sub_info)
            if not subscribed:
                await websocket.close(code=4404, reason=f"Class requested Not Found")
                return
            await cls.send_message_async(websocket, json.dumps(
                subscribed,
                ensure_ascii=False,
                default=lambda o: o.get_display_data() if isinstance(o, Base) else o
            ))
            try:
                while True:
                    await websocket.receive_text()
            except WebSocketDisconnect:
                cls.disconnect(websocket)

        @app.on_event("startup")
        async def startup_event():
            loop = asyncio.get_event_loop()
            loop.create_task(logger_class.streaming_async(callback=cls.document_sent_async, **logger_param))

        return app
