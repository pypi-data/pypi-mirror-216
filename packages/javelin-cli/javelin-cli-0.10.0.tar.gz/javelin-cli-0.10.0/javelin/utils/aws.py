"""AWS
"""

import sys
import time

import boto3
import yaml

##
## PUBLIC
##

def start_pipeline_execution_and_wait(project_name, env):
  codepipeline = boto3.client("codepipeline")
  pipeline_name = _get_project_pipeline_name(project_name, env)

  if not pipeline_name:
    return True

  res = codepipeline.start_pipeline_execution(name=pipeline_name)

  if res["ResponseMetadata"]["HTTPStatusCode"] != 200:
    print("javelin: couldn't start pipeline")
    sys.exit(2)

  pipeline_execution_id = res["pipelineExecutionId"]

  while True:
    try:
      res = codepipeline.get_pipeline_execution(
        pipelineName=pipeline_name,
        pipelineExecutionId=pipeline_execution_id
      )

      status = res["pipelineExecution"]["status"]

      if status == "InProgress":
        print("\033[A\033[A")
        print(f"({pipeline_execution_id}) In progress...")
      elif status == "Succeeded":
        print(f"({pipeline_execution_id}) Succeeded.")
        return True
      else:
        print(f"({pipeline_execution_id}) Execution ended with status \"{status}\"")
        return False
    except codepipeline.exceptions.PipelineExecutionNotFoundException:
      print(f"({pipeline_execution_id}) Waiting...")

    time.sleep(5)

def approve_pipeline_execution(project_name, env):
  codepipeline = boto3.client("codepipeline")
  pipeline_name = _get_project_pipeline_name(project_name, env)

  while True:
    res = codepipeline.get_pipeline_state(name=pipeline_name)

    approve_stage = next(stage for stage in res["stageStates"] if stage["stageName"] == "Approve")

    if approve_stage["latestExecution"]["status"] == "InProgress":
      approve_action = approve_stage["actionStates"][0]

      try:
        codepipeline.put_approval_result(
          pipelineName=pipeline_name,
          stageName=approve_stage["stageName"],
          actionName=approve_action["actionName"],
          token=approve_action["latestExecution"]["token"],
          result={
            "summary": "Approved with Javelin",
            "status": "Approved"
          }
        )

        return approve_stage["latestExecution"]["pipelineExecutionId"]
      except (
        codepipeline.Client.exceptions.InvalidApprovalTokenException,
        codepipeline.Client.exceptions.ApprovalAlreadyCompletedException,
        codepipeline.Client.exceptions.PipelineNotFoundException,
        codepipeline.Client.exceptions.StageNotFoundException,
        codepipeline.Client.exceptions.ActionNotFoundException,
        codepipeline.Client.exceptions.ValidationException
      ):
        return None
    else:
      time.sleep(5)

def wait_for_pipeline_execution_finish(project_name, env, pipeline_execution_id):
  codepipeline = boto3.client("codepipeline")
  pipeline_name = _get_project_pipeline_name(project_name, env)

  if not pipeline_name:
    return True

  while True:
    try:
      res = codepipeline.get_pipeline_execution(
        pipelineName=pipeline_name,
        pipelineExecutionId=pipeline_execution_id
      )

      status = res["pipelineExecution"]["status"]

      if status == "InProgress":
        print("\033[A\033[A")
        print(f"({pipeline_execution_id}) In progress...")
      elif status == "Succeeded":
        print(f"({pipeline_execution_id}) Succeeded.")
        return True
      else:
        print(f"({pipeline_execution_id}) Execution ended with status \"{status}\"")
        return False
    except codepipeline.exceptions.PipelineExecutionNotFoundException:
      print(f"({pipeline_execution_id}) Waiting...")

    time.sleep(5)

##
## PRIVATE
##

def _get_project_pipeline_name(project_name, env):
  with open("./config/projects.yml", "r", encoding="utf-8") as stream:
    try:
      config = yaml.safe_load(stream)

      return config[project_name]["codepipeline_names"][env]
    except (KeyError, yaml.YAMLError):
      return None
