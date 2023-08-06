import concurrent
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

import typer
from google.protobuf.json_format import MessageToDict

from ascend_io_cli.support import get_client, print_response, COMPONENT_PAUSE_METHODS

app = typer.Typer(help='Pause component execution', no_args_is_help=True)


@app.command()
def component(
    ctx: typer.Context,
    data_service: Optional[str] = typer.Argument(..., help='Data Service id containing the component to pause', show_default=False),
    dataflow: Optional[str] = typer.Argument(..., help='Dataflow id containing the component to pause', show_default=False),
    component: Optional[str] = typer.Argument(..., help='Component id to pause', show_default=False),
):
  """Pause a component"""
  pause_resume_components(ctx, True, data_service, dataflow, component)


@app.command()
def dataflow(
    ctx: typer.Context,
    data_service: Optional[str] = typer.Argument(..., help='Data Service id', show_default=False),
    dataflow: Optional[str] = typer.Argument(..., help='Dataflow id', show_default=False),
):
  """Pause all components in a dataflow"""
  pause_resume_components(ctx, True, data_service, dataflow, None)


def pause_resume_components(ctx: typer.Context, pause_flag: bool, service_id: str, flow_id: str, component_id: str):
  client = get_client(ctx)

  def _pause_resume(component, pause: bool):
    if COMPONENT_PAUSE_METHODS.get(component.type, None):
      return getattr(client, COMPONENT_PAUSE_METHODS[component.type])(data_service_id=c.organization.id,
                                                                      dataflow_id=c.project.id,
                                                                      id=c.id,
                                                                      body='',
                                                                      paused=pause).data
    return None

  results = []
  if service_id and flow_id:
    components = client.list_dataflow_components(service_id, flow_id, deep=False, kind='source,view,sink').data
    futures = []
    with ThreadPoolExecutor(max_workers=ctx.obj.workers) as executor:
      for c in components:
        if not component_id or (component_id and c.id == component_id):
          futures.append(executor.submit(_pause_resume, c, pause_flag))

    for future in concurrent.futures.as_completed(futures):
      result = future.result(10)
      results.append(MessageToDict(result))

  print_response(ctx, results)
