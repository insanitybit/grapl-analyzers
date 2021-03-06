import os
from typing import Any, Type

import redis
from grapl_analyzerlib.analyzer import Analyzer, OneOrMany, A
from grapl_analyzerlib.counters import ParentChildCounter
from grapl_analyzerlib.prelude import ProcessQuery, ProcessView
# from grapl_analyzerlib.execution import ExecutionHit
from pydgraph import DgraphClient

COUNTCACHE_ADDR = os.environ['COUNTCACHE_ADDR']
COUNTCACHE_PORT = int(os.environ['COUNTCACHE_PORT'])

r = redis.Redis(host=COUNTCACHE_ADDR, port=COUNTCACHE_PORT, db=0, decode_responses=True)


class UniqueParentChild(Analyzer):

    def __init__(self, dgraph_client: DgraphClient, counter: ParentChildCounter):
        super(UniqueParentChild, self).__init__(dgraph_client)
        self.counter = counter

    @classmethod
    def build(cls: Type[A], dgraph_client: DgraphClient) -> A:
        counter = ParentChildCounter(dgraph_client)
        return UniqueParentChild(dgraph_client, counter)

    def get_queries(self) -> OneOrMany[ProcessQuery]:
        return (
            ProcessQuery()
            .with_process_name()
            .with_parent(
                ProcessQuery()
                .with_process_name()
            )
        )

    def on_response(self, response: ProcessView, output: Any):
        parent = response.get_parent()

        # count = self.counter.get_count_for(
        #     parent_process_name=response.get_process_name(),
        #     child_process_name=parent.get_process_name(),
        # )
        #
        # if count < 2:
        #     output.send(
        #         ExecutionHit(
        #             analyzer_name="Rare Parent Child Process",
        #             node_view=response,
        #             risk_score=5,
        #         )
        #     )
