"""This is the main file for the sdk cli.

It is responsible for handling the cli commands and passing them to the sdk module.
"""
import json
import logging
from enum import Enum
from logging import getLogger
from pathlib import Path

# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
from typing import List, Optional

import typer
import yaml
from trogon import Trogon
from typer.main import get_group
import iris.sdk as sdk

from .sdk.utils import exception_to_json_error, valid_qlora

logger = getLogger(__name__)
logger.setLevel(sdk.conf_mgr.LOG_LEVEL)

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                   sdk CLI Module                                                     #

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

# create the typer object
main = typer.Typer()


def conf_callback(ctx: typer.Context, param: typer.CallbackParam, value: str):
    """This is a typer callback that loads a yaml file (value) and uses it to override the command line arguments.

       If this is provided as the callback for an argument with is_eager=True,
       it runs before loading the other arguments and provides them from the yaml.
       If they're set manually, they get overriden in the config.

    Args:
        ctx (typer.Context): the typer context
        param (typer.CallbackParam): the typer param (name?)
        value (str): the value of the param (the filepath of the yaml)

    Raises:
        typer.BadParameter: if there is an exception while parsing

    Returns:
        value: the path
    """
    if value:
        logger.debug(f"Loading args from: {value}")
        try:
            with open(value, "r") as f:  # Load config file
                conf = yaml.safe_load(f)
            ctx.default_map = ctx.default_map or {}  # Initialize the default map
            logger.debug(f"original default map {ctx.default_map}")
            ctx.default_map.update(conf)  # Merge the config dict into default_map
            logger.debug(f"loaded: {ctx.default_map}")
        except Exception as ex:
            raise typer.BadParameter(str(ex))
    return value


@main.command()
def login():
    """Login to iris."""
    try:
        user_name = sdk.login()
        print(f"Logged in as {user_name}")
    except Exception as e:
        json_error = exception_to_json_error(e)
        print(json_error)
        raise typer.Abort()


@main.command()
def logout():
    """Logout from iris."""
    try:
        logged_out = sdk.logout()
        if logged_out:
            print("Successfully logged out")
        else:
            raise Exception("Failed to logout")
    except Exception as e:
        json_error = exception_to_json_error(e)
        print(json_error)
        raise typer.Abort()


@main.command()
def version():
    """Print the version of iris."""
    from importlib.metadata import version

    print(version("titan-iris"))


@main.command()
def ui(ctx: typer.Context):
    """Run the tui.

    Args:
        ctx (typer.Context): The typer context
    """
    Trogon(get_group(main), click_context=ctx).run()


class Task(str, Enum):
    """The task to optimize the model for."""

    sequence_classification = "sequence_classification"
    glue = "glue"
    question_answering = "question_answering"
    token_classification = "token_classification"
    language_modelling = "language_modelling"


class Object(str, Enum):
    """The various kinds of API objects that the TitanML platform supports."""

    experiment = "experiment"
    artefact = "artefact"
    inference_session = "inference-session"


class Artefact(str, Enum):
    """Artefacts: models, datasets, etc."""

    model = "model"
    dataset = "dataset"


# Ex-post arguments which are now shared between athena, pontus and post. Define once here to avoid duplication.
MODEL_ARG = typer.Option(..., "--model", "-m", help="The models to optimize.")
DATASET_ARG = typer.Option(..., "--dataset", "-d", help="The dataset to optimize the model with.")
TASK_ARG = typer.Option(..., "--task", "-t", help="The task to optimize the model for.")
SUBSET_ARG = typer.Option(None, "--subset", "-ss", help="The subset of a dataset to optimize on")
NAME_ARG = typer.Option(
    "",
    "--name",
    "-n",
    help="The name to use for this job. Visible in the TitanML Hub.",
)
NUM_LABELS_ARG = typer.Option(
    None,
    "--num-labels",
    "-nl",
    help="Number of labels. Required for sequence_classification tasks.",
)

LABEL_NAMES_ARG = typer.Option(
    None,
    "--label-names",
    "-ln",
    help=(
        "Names of token labels. Required for token_classification tasks."
        "Specify as a mapping with no spaces: -ln 0:label1 -ln 1:label2"
    ),
)
LABEL_COLUMN_ARG = typer.Option("label", "--labels-column", "-lc", help="The name of the column containing the labels.")
TEXT_FIELDS_ARG = typer.Option(
    None,
    "--text-fields",
    "-tf",
    help="The field(s) containing input texts. Required for sequence_classification tasks",
)
BATCH_SIZE_ARG = typer.Option(
    "4",
    "--batch-size",
    "-bs",
    help="The batch size to use for training. Specifying 'auto' will use the maximum "
    "batch_size achievable under reasonable hardware constraints.",
)
LEARNING_RATE_ARG = typer.Option(2e-5, "--learning-rate", "-lr", help="The learning rate to use for training.")

TEST_ARG = typer.Option(
    False,
    "--short-run",
    "-s",
    help="Truncates the run after 1 batch and 1 epoch. \
            Will provide bad results, but useful to check that the model and dataset choices are valid.",
)
HAS_NEGATIVE_ARG = typer.Option(
    False,
    "--has-negative",
    "-hn",
    help="Whether the dataset includes examples which have 'no answer'. Required for question_answering tasks",
)
QLORA_ARG = typer.Option(
    False,
    "--no-qlora",
    "-nql",
    help="Do not use QLoRA, even when available. If not given, then QLoRA will be used " "where possible.",
)
# new
TRAIN_SPLIT_NAME = typer.Option(
    "train",
    "--train-split-name",
    "-tsn",
    help="The name of the train data split",
)
VALID_SPLIT_NAME = typer.Option(
    "validation",
    "--val-split-name",
    "-vsn",
    help="The name of the validation data split",
)
JSON_ARG = typer.Option(
    False,
    "--json",
    "-j",
    help="Print output as JSON. Default: Rich output",
)

FILE_ARG = typer.Option(
    "",
    "--file",
    "-f",
    help="Load the options from a config file",
    callback=conf_callback,
    is_eager=True,
)
HEADERS_ARG = typer.Option(
    [],
    "--headers",
    "-H",
    help="Headers to send with the get request. \
            Should be provided as colon separated key value pairs: -h a:b -h c:d -> {a:b, c:d}",
)


@main.command()
def post(
    model: str = MODEL_ARG,
    dataset: str = DATASET_ARG,
    task: Task = TASK_ARG,
    subset: Optional[str] = SUBSET_ARG,
    experiment_name: str = NAME_ARG,
    file: str = FILE_ARG,
    test: bool = TEST_ARG,
    num_labels: int = NUM_LABELS_ARG,
    text_fields: Optional[List[str]] = TEXT_FIELDS_ARG,
    has_negative: bool = HAS_NEGATIVE_ARG,
    train_split_name: Optional[str] = TRAIN_SPLIT_NAME,
    val_split_name: Optional[str] = VALID_SPLIT_NAME,
    label_names: Optional[List[str]] = LABEL_NAMES_ARG,
    headers: List[str] = HEADERS_ARG,
    json_output: bool = JSON_ARG,
    label_column: str = LABEL_COLUMN_ARG,
    no_qlora: bool = QLORA_ARG,
):
    """Submit a pipelining job (currently defaults to distillation)."""
    dispatch("athena", **locals(), batch_size="auto", learning_rate=None, num_epochs=5)


@main.command()
def distil(
    model: str = MODEL_ARG,
    dataset: str = DATASET_ARG,
    task: Task = TASK_ARG,
    subset: Optional[str] = SUBSET_ARG,
    experiment_name: str = NAME_ARG,
    file: str = FILE_ARG,
    test: bool = TEST_ARG,
    num_labels: int = NUM_LABELS_ARG,
    text_fields: Optional[List[str]] = TEXT_FIELDS_ARG,
    has_negative: bool = HAS_NEGATIVE_ARG,
    train_split_name: Optional[str] = TRAIN_SPLIT_NAME,
    val_split_name: Optional[str] = VALID_SPLIT_NAME,
    label_names: Optional[List[str]] = LABEL_NAMES_ARG,
    headers: List[str] = HEADERS_ARG,
    json_output: bool = JSON_ARG,
    label_column: str = LABEL_COLUMN_ARG,
    no_qlora: bool = QLORA_ARG,
):
    """Submit a knowledge distillation job."""
    dispatch("athena", **locals(), batch_size="32", learning_rate=2e-05, num_epochs=5)


@main.command()
def finetune(
    model: str = MODEL_ARG,
    dataset: str = DATASET_ARG,
    task: Task = TASK_ARG,
    subset: Optional[str] = SUBSET_ARG,
    experiment_name: str = NAME_ARG,
    test: bool = TEST_ARG,
    num_labels: int = NUM_LABELS_ARG,
    text_fields: Optional[List[str]] = TEXT_FIELDS_ARG,
    has_negative: bool = HAS_NEGATIVE_ARG,
    train_split_name: Optional[str] = TRAIN_SPLIT_NAME,
    val_split_name: Optional[str] = VALID_SPLIT_NAME,
    label_names: Optional[List[str]] = LABEL_NAMES_ARG,
    headers: List[str] = HEADERS_ARG,
    batch_size: str = BATCH_SIZE_ARG,
    learning_rate: float = LEARNING_RATE_ARG,
    json_output: bool = JSON_ARG,
    num_epochs: int = typer.Option(1, "--num-epochs", "-ne", help="The number of epochs to finetune for."),
    file: str = FILE_ARG,
    label_column: str = LABEL_COLUMN_ARG,
    no_qlora: bool = QLORA_ARG,
):
    """Submit a finetuning job."""
    dispatch("pontus", **locals())


def dispatch(
    type,
    model,
    dataset,
    task,
    subset,
    experiment_name,
    file,
    test,
    num_labels,
    text_fields,
    has_negative,
    train_split_name,
    val_split_name,
    label_names,
    headers,
    batch_size,
    learning_rate,
    num_epochs,
    json_output,
    label_column,
    no_qlora,
):
    """Dispatch a job to the TitanML platform. Distil, Post and Athena ultimately run through here."""
    # get the enum value as task
    headers = {x.partition(":")[0]: x.partition(":")[-1] for x in headers}
    task = task.value
    # baseline flags
    flags = {
        "model": model,
        "dataset": dataset,
        "task": task,
        "test": test,
        "subset": subset,
        "type": type,
        "num_epochs": num_epochs,
        "train_split_name": train_split_name,  # new
        "val_split_name": val_split_name,  # new
        "label_column": label_column,
    }
    # lots of argument checking
    if experiment_name != "":
        flags.update({"name": experiment_name})
    if task == "sequence_classification":
        # sequence of task specific flags
        # if the flag shouldn't be accepted, set error_message to the error string to print.
        # if it should be, and you want to warn, print, but don't set error_message
        error_message = False
        if not num_labels and not len(label_names):
            error_message = (
                "Please provide either the number of labels (--num-labels, -nl) or "
                "a mapping between user labels and (integer) dataset labels."
            )
        elif num_labels and len(label_names) != num_labels and len(label_names):
            error_message = (
                "The given label map has a different number of labels to " "that specified with --num-labels"
            )
        elif num_labels and len(label_names):
            print("If providing label_names, num_labels does not need to be provided.")
        elif label_names:
            if not all(":" in x for x in label_names):
                error_message = (
                    "Label names should be specified as a map from integers to labels, e.g. "
                    "'-ln 0:Positive -ln 1:Negative ...'"
                )
            if error_message:
                print(error_message)
                raise typer.Abort()
            else:
                label_names_dict = {int(i): label for i, label in map(lambda x: x.split(":"), label_names)}
                label_names_num = len(list(label_names_dict.keys()))
                max_label_num = max(i for i in label_names_dict.keys())
                min_label_num = min(i for i in label_names_dict.keys())
                if max_label_num != (len(list(label_names_dict.keys())) - 1):
                    print("Label names must have contiguous indices")
                    raise typer.Abort()

                if min_label_num != 0:
                    print("Label indices must start at zero")
                    raise typer.Abort()

                label_names_list = [label_names_dict[i] for i in range(label_names_num)]
                flags.update({"label_names": label_names_list})
        if text_fields is None or len(text_fields) == 0:
            error_message = "Please provide the text fields to tokenize (--text-fields, -tf)"
        if has_negative:
            print("has_negative is not necessary for sequence classification tasks")
        if error_message:
            print(error_message)
            raise typer.Abort(error_message)

        else:
            # new: label_names
            flags.update({"num_labels": num_labels, "text_fields": text_fields})
    elif task == "question_answering":
        is_error = False
        # sequence of task specific flags
        # if the flag shouldn't be accepted, set is_error=True
        # if it should be, and you want to warn, print, but don't set is_error
        if num_labels is not None:
            print("num_labels is not necessary for question answering tasks")
        if text_fields is not None and len(text_fields) > 0:
            print("text_fields is not necessary for question answering tasks")
        if label_names is not None and len(label_names) > 0:
            print("label_names is not necessary for question_answering tasks")
        if is_error:
            raise typer.Abort()
        else:
            flags.update({"has_negative": has_negative})
    elif task == "glue":
        # sequence of task specific flags
        # if the flag shouldn't be accepted, set is_error=True
        # if it should be, and you want to warn, print, but don't set is_error
        is_error = False
        if num_labels is not None:
            print("num_labels is not necessary for glue tasks")
        if label_names is not None and len(label_names) > 0:
            print("label_names is not necessary for glue tasks")
        if text_fields is not None and text_fields != []:
            print("text_fields is not necessary for glue tasks")
        if has_negative:
            print("has_negative is not necessary for glue tasks")
        if is_error:
            raise typer.Abort()
        else:
            pass
    elif task == "token_classification":
        error_message = False
        if num_labels is not None:
            print("num_labels is not necessary for token classification tasks")
        if label_names is None:
            error_message = "Please provide the label names of the tokens"
        if not all(":" in x for x in label_names):
            error_message = "Label names should be specified as a map, e.g. '-ln 0:PER -ln 1:ORG ...'"
        if error_message:
            print(error_message)
            raise typer.Abort()
        else:
            label_names_dict = {int(i): label for i, label in map(lambda x: x.split(":"), label_names)}
            label_names_num = len(list(label_names_dict.keys()))
            max_label_num = max(i for i in label_names_dict.keys())
            min_label_num = min(i for i in label_names_dict.keys())
            if max_label_num != (len(list(label_names_dict.keys())) - 1):
                print("Label names must have contiguous indices")
                raise typer.Abort()

            if min_label_num != 0:
                print("Label indices must start at zero")
                raise typer.Abort()

            label_names_list = [label_names_dict[i] for i in range(label_names_num)]
            flags.update({"label_names": label_names_list})

    elif task == "language_modelling" or task == "language_modeling":
        # sequence of task specific flags
        # if the flag shouldn't be accepted, set error_message to the error string to print.
        # if it should be, and you want to warn, print, but don't set error_message
        error_message = False
        if type == "athena":
            error_message = "Knowledge distillation is not yet supported for language modelling."
        if label_column and len(label_column):
            if label_column != LABEL_COLUMN_ARG.default:
                print("label_column is not necessary for language modelling tasks")
            flags.pop("label_column")
        if num_labels is not None:
            print("num_labels is not necessary for language modelling tasks")
        if label_names is not None and len(label_names) > 0:
            print("label_names is not necessary for language modelling tasks")
        if has_negative:
            print("has_negative is not necessary for language modelling tasks")

        if no_qlora and valid_qlora(model):  # If want to disable qlora, but qlora is available:
            print(f"QLoRA manually disabled for {model}")
            use_qlora = False
        elif not no_qlora and not valid_qlora(model):  # If qlora isn't explicitly disabled, but is not available.
            print(f"QLoRA not available for {model}. Proceeding without QLoRA.")
            use_qlora = False
        elif no_qlora and not valid_qlora(model):  # Qlora disabled, but it wasn't available anyways.
            use_qlora = False
        else:  # Qlora not explicitly disabled, and qlora is available.
            print("QLoRA is available and will be used.")
            use_qlora = True

        if error_message:
            print(error_message)
            raise typer.Abort()
        else:
            flags.update({"text_fields": text_fields, "use_qlora": use_qlora})
    else:
        print(f"Unrecognised task {task}")
        raise typer.Abort()

    if num_epochs >= 99:
        logging.warning(
            "Woah there cowboy, that's a mighty high number of epochs you got there. "
            "Are you sure you didn't mistype it?"
        )
    if batch_size:
        if batch_size == "auto":
            flags["batch_size"] = batch_size
        elif "." not in batch_size and batch_size.isdigit():
            n = int(batch_size)
            if not ((n != 0) and (n & (n - 1) == 0)):  # Check if batch size is power of 2.
                print(
                    "Note that batch sizes which are a base-2 value (2,4,16,32,64,128...) will result in faster "
                    "training."
                )
            flags["batch_size"] = int(batch_size)
        else:
            print(f"Unrecognised batch size format {batch_size}")
            raise typer.Abort()
    if learning_rate:
        try:
            flags["learning_rate"] = float(learning_rate)
        except ValueError:
            print(f"Unrecognised learning rate format {batch_size}")
            raise typer.Abort()

    # post the resulting flags
    sdk.post(headers, **flags, json_output=json_output)


@main.command()
def get(
    object: Object = typer.Argument("experiment", help="What type of object to get"),
    id: Optional[str] = typer.Option(
        None,
        "--id",
        "-i",
        help="Which object to get. None, or '' correspond to getting all objects. Evaluated server-side.",
    ),
    query: Optional[str] = typer.Option(
        None,
        "--query",
        "-q",
        help="A JMESPath string, to filter the objects returned by the API. Evaluated client-side.",
    ),
    headers: List[str] = HEADERS_ARG,
    json_output: Optional[bool] = JSON_ARG,
):
    """Get objects from the TitanML Store."""
    # get the string from the enum
    headers = {x.partition(":")[0]: x.partition(":")[-1] for x in headers}
    object = object.value
    try:
        sdk.get(object, id, query, headers, json_output=json_output)
    except Exception:
        raise typer.Abort()


@main.command()
def delete(
    object: Object = typer.Argument("experiment", help="What type of object to delete"),
    id: Optional[str] = typer.Option(
        ...,
        "--id",
        "-i",
        help="Which object to delete",
    ),
    json_output: bool = JSON_ARG,
):
    """Delete objects from the TitanML store."""
    # delete the string from the enum
    object = object.value
    try:
        sdk.delete(object, id, json_output=json_output)
    except Exception as e:
        print(exception_to_json_error(e))
        raise typer.Abort()


@main.command()
def pull(
    image: str = typer.Argument(..., help="The image to pull. Should be displayed in the TitanML Hub."),
    json_output: bool = JSON_ARG,
):
    """Pull the titan-optimized server docker image."""
    try:
        sdk.pull(image, json_output=json_output)
    except Exception as e:
        json_error = exception_to_json_error(e)
        print(json_error)
        raise typer.Abort()


@main.command()
def download(
    image: str = typer.Argument(..., help="The model to pull. Should be displayed in the TitanML Hub."),
    json_output: bool = JSON_ARG,
):
    """Download the titan-optimized onnx model."""
    try:
        sdk.download(image, json_output=json_output)
    except Exception as e:
        json_error = exception_to_json_error(e)
        print(json_error)
        raise typer.Abort()


@main.command()
def infer(
    target: str = typer.Option("localhost", "--target", help="The url to run the server on."),
    port: int = typer.Option(8000, "--port", "-p", help="The port to run the server on."),
    task: Task = typer.Option(..., "--task", help="The task to optimize the model for."),
    runtime: str = typer.Option(
        "trt",
        "--runtime",
        help="The runtime to use. Can be one of 'trt', 'onnx'. Defaults to 'trt'.",
    ),
    text: List[str] = typer.Option(
        ...,
        "--text",
        help="The text to run the server in. In classification tasks, this is the TEXT to be classified. \
            In question answering tasks, this is the QUESTION to be answered.",
    ),
    context: Optional[str] = typer.Option(
        "",
        "--context",
        "-c",
        help="The context in question answering tasks. Only used in question answering tasks.",
    ),
):
    """Run inference on a model."""
    url = f"{target}:{port}"

    try:
        if task == "sequence_classification":
            if context is None or context != "":
                print("context is not necessary for classification tasks")
                raise typer.Abort()
            res = sdk.infer(url=url, task_name=task, runtime=runtime, text=text)
            print(res)
        elif task == "question_answering":
            if context is None or context == "":
                print("context is required for question answering tasks")
                raise typer.Abort()
            if len(text) != 1:
                print("text should only contain one question")
                raise typer.Abort()
            res = sdk.infer(url=url, task_name=task, runtime=runtime, text=text, context=context)
            print(res)
        else:
            print(f"Unrecognised task {task}")
            raise typer.Abort()
    except Exception as e:
        json_error = exception_to_json_error(e)
        print(json_error)
        raise typer.Abort() from e


@main.command()
def demo(
    target: str = typer.Option("localhost", "--target", help="The url to run the server on."),
    port: int = typer.Option(8000, "--port", "-p", help="The port to run the server on."),
):
    """Run the gradio demo.

    Here the target and port are the same as the infer command, which is where the triton server is running.
    The default is localhost:8000.
    """
    url = f"{target}:{port}"
    try:
        from iris.gradio.run import run

        run(url)
    except Exception as e:
        json_error = exception_to_json_error(e)
        print(json_error)
        raise typer.Abort()


@main.command()
def upload(
    src: Path = typer.Argument(
        ...,
        help="The location of the artefact on disk. Should be a folder, containing either a model or a dataset.\
              For more information on the supported formats, see the TitanML documentation.",
    ),
    name: str = typer.Argument(None, help="The name of the artefact. Displayed in the TitanML Hub."),
    description: str = typer.Argument(
        None,
        help="A short description of the artefact. Displayed in the TitanML Hub.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        "-j",
        help="Print output as JSON (default: Rich output)",
    ),
):
    """Upload an artefact to the TitanML Hub."""
    try:
        sdk.upload(name, src, description, json_output=json_output)
    except Exception as e:
        json_error = exception_to_json_error(e)
        print(json_error)
        raise typer.Abort()


@main.command()
def status(
    id: str = typer.Option(..., "--id", "-i", help="The id of the experiment to get the status of"),
    headers: List[str] = HEADERS_ARG,
    json_output: bool = JSON_ARG,
):
    """Get the status of an experiment."""
    headers = {x.partition(":")[0]: x.partition(":")[-1] for x in headers}
    summary = ""
    try:
        summary = sdk.get(
            "experiment",
            id,
            "experiment.jobs[*].tasks[*].{name:name, status:status, message:message}",
            headers,
            json_output=json_output,
        )
        return summary
    except Exception:
        raise typer.Abort()


@main.command()
def makesafe(
    model: str = typer.Argument("model", help="The model to convert to safe_tensors"),
):
    """Convert a non-safetensor model into a safetensor model, including for models with shared weights."""
    try:
        sdk.makesafe(model)
    except Exception as e:
        json_error = exception_to_json_error(e)
        print(json_error)
        raise typer.Abort()


@main.command()
def query(artefact_id: str, data: str = typer.Option("", "--data", "-d")):
    """Create/query an inference endpoint for a given model.

    The data should be a json string, with the following format:
    """
    try:
        data = json.dumps(data)
    except Exception:
        print({"status": "Failed", "message": "data should be a json string"})
        raise typer.Abort()
    response = sdk.query(artefact_id, data)
    print(response)


if __name__ == "__main__":
    main()
