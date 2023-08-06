from typing import Optional

import typer

from ascend_io_cli.commands.pause import pause_resume_components

app = typer.Typer(help='Resume component execution', no_args_is_help=True)


@app.command()
def component(
    ctx: typer.Context,
    data_service: Optional[str] = typer.Argument(..., help='Data Service id', show_default=False),
    dataflow: Optional[str] = typer.Argument(..., help='Dataflow id', show_default=False),
    component: Optional[str] = typer.Argument(..., help='Component id', show_default=False),
):
  """Resume a component"""
  pause_resume_components(ctx, False, data_service, dataflow, component)


@app.command()
def dataflow(
    ctx: typer.Context,
    data_service: Optional[str] = typer.Argument(..., help='Data Service id', show_default=False),
    dataflow: Optional[str] = typer.Argument(..., help='Dataflow id', show_default=False),
):
  """Resume all components in a dataflow"""
  pause_resume_components(ctx, False, data_service, dataflow, None)
