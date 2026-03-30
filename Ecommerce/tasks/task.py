import os
import time

from celery import shared_task
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


@shared_task
def make_image(prompet):
    cleint = OpenAI(api_key=os.getenv("API_Key"))
    response = cleint.images.generate(
        model="dall-e-3",
        prompt=prompet,
        size="1024x1024",
        n=1,
    )

    print(prompet)
    print(response.data[0].url)


@shared_task
def Sleeping(prompet):
    time.sleep(1)
    print(prompet)
    return prompet


@shared_task
def Schduled_task_celery_beat():
    print("Running Each 20 Seconds ")


@shared_task
def Schduled_task_celery__tow_day():
    print("Running Each 20 Seconds ")


@shared_task
def Red_beat_Schedule_task(input, schedule_name):
    print(
        f"Red_beat_Schedule_task is called  =>>>>>>>>>>>>>>>> {input} = > schedule_name {schedule_name} "
    )
