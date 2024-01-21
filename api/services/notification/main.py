from typing import Optional
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRoute
from fastapi import FastAPI, Depends, HTTPException
from share.notification.subscriptions import (addSubscription, getAllSubscriptions, deleteSubscription, printAllRedisData)
from typing import List

app = FastAPI()

class SubscriptionRequest(BaseModel):
    callback_url: str | None = None
    email: str | None = None

@app.post("/users/{user_id}/subscribe/{section_id}")
def subscribe(
    user_id: str,
    section_id: str,
    req: SubscriptionRequest
    ):
    addSubscription(section_id, user_id, req.callback_url, req.email)
    return {"detail": "subscription successful"}

class Subscription(BaseModel):
    section_id: str
    callback_url: str
    email: str

class SubscriptionResponse(BaseModel):
    subscriptions: List[Subscription]

@app.get("/users/{user_id}/subscriptions")
def subscriptions(    
    user_id: str,
    ) -> SubscriptionResponse:
    printAllRedisData()
    subscriptions = getAllSubscriptions(user_id)
    return SubscriptionResponse(subscriptions=subscriptions)


@app.delete("/users/{user_id}/unsubscribe/{section_id}")
def unsubscribe(
    user_id: str,
    section_id: str,
    ):
    
    deleteSubscription(user_id, section_id)
    return {"detail": "subscription successfully deleted"}

# class Webhook(BaseModel):
#     message: str

@app.post("/webhook")
async def webhook(data: dict):
    print(f"Webhook received with message: {data}")
    return {"detail": "Webhook successfully received"}

# https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#using-the-path-operation-function-name-as-the-operationid
for route in app.routes:
    if isinstance(route, APIRoute):
        route.operation_id = route.name
