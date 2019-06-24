
from typing import Any

from grapl_analyzerlib.entity_queries import Not
from grapl_analyzerlib.execution import ExecutionHit
from pydgraph import DgraphClient
from grapl_analyzerlib.entities import ProcessQuery, SubgraphView, FileQuery, NodeView


def analyzer(client: DgraphClient, node: NodeView, sender: Any):

    valid_parents = [
        Not("services.exe"),
        Not("smss.exe"),
        Not("ngentask.exe"),
        Not("userinit.exe"),
    ]

    process = node.as_process_view()
    if not process:
        return

    p = (
        ProcessQuery()
        .with_process_name(eq=valid_parents)
        .with_children(
            ProcessQuery().with_process_name(eq="svchost.exe")
        )
        .query_first(client, contains_node_key=process.node_key)
    )

    if p:
        sender.send(
            ExecutionHit(
                analyzer_name="Suspicious svchost",
                node_view=p,
                risk_score=10,
            )
        )
