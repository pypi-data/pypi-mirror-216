#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from typing import Dict, Callable
import logging
import logging.config
import importlib
from uuid import uuid4
from firebird.rabbitmq import get_connection, RabbitMQ
from firebird import zkdb
from kubernetes import client, config

logger = logging.getLogger(__name__)

def register_command(config:dict, pipeline_namespace_name:str, pipeline_image_name:str, pipeline_module_name:str):
    pipeline = importlib.import_module(pipeline_module_name).get_pipeline(None)
    pipeline_info = pipeline.to_json()

    mq = RabbitMQ(
        connection = get_connection(**config["rabbitmq"]),
        topic = pipeline.id
    )
    # create rabbitmq topic, etc
    mq.initialize()

    with zkdb(**config['zookeeper']) as db:
        db.register_pipeline(pipeline.id, pipeline_namespace_name, pipeline_image_name, pipeline_module_name)

def unregister_command(config:dict, pipeline_id:str):
    with zkdb(**config['zookeeper']) as db:
        db.unregister_pipeline(pipeline_id)

def list_command(config):
    with zkdb(**config['zookeeper']) as db:
        pipelines = db.get_pipelines()

    for pipeline in pipelines:
        print(f"{pipeline['info']['id']}:")
        print(f"    module: {pipeline['module']}")
        if len(pipeline["executors"]) == 0:
            print("    executors: None")
        else:
            print("    executors:")
            for executor in pipeline["executors"]:
                executor_info = executor["info"]
                print(f"        {executor_info['id']}:")
                print(f"            worker_count          = {executor_info['worker_count']}")
                print(f"            start_time            = {executor_info['start_time']}")
                print(f"            pid                   = {executor_info['pid']}")

def stop_command(config:dict, pipeline_id:str, executor_id:str):
    with zkdb(**config['zookeeper']) as db:
        db.stop_executor(pipeline_id, executor_id)


def start_command(config, pipeline_id):
    print("Not implemented")
