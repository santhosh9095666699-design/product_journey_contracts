import smartpy as sp


@sp.module
def main():
    class TraceTrail(sp.Contract):
        def __init__(self):
            self.data.batches = sp.cast(
                sp.big_map(),
                sp.big_map[
                    sp.string,
                    sp.record(
                        registered_by=sp.address,
                        next_step=sp.nat,
                        latest_event=sp.string,
                        events=sp.list[sp.string],
                    ),
                ],
            )

        @sp.entrypoint
        def register_batch(self, params):
            sp.cast(
                params,
                sp.record(batch_id=sp.string, first_event=sp.string),
            )
            assert not self.data.batches.contains(params.batch_id), "BATCH_EXISTS"
            self.data.batches[params.batch_id] = sp.record(
                registered_by=sp.sender,
                next_step=1,
                latest_event=params.first_event,
                events=[params.first_event],
            )

        @sp.entrypoint
        def add_journey_event(self, params):
            sp.cast(
                params,
                sp.record(batch_id=sp.string, step=sp.nat, event=sp.string),
            )
            assert self.data.batches.contains(params.batch_id), "BATCH_NOT_FOUND"
            batch = self.data.batches[params.batch_id]
            assert sp.sender == batch.registered_by, "NOT_AUTHORIZED"
            assert params.step == batch.next_step, "WRONG_STEP"
            self.data.batches[params.batch_id] = sp.record(
                registered_by=batch.registered_by,
                next_step=batch.next_step + 1,
                latest_event=params.event,
                events=sp.cons(params.event, batch.events),
            )


@sp.add_test()
def test_trace_trail():
    scenario = sp.test_scenario("TraceTrail", main)
    producer = sp.test_account("Producer")
    stranger = sp.test_account("Stranger")
    contract = main.TraceTrail()
    scenario += contract

    scenario.h2("Register a batch")
    contract.register_batch(
        sp.record(batch_id="BATCH-001", first_event="Harvested in Coorg"),
        _sender=producer,
    )
    scenario.verify(contract.data.batches["BATCH-001"].next_step == 1)
    scenario.verify(
        contract.data.batches["BATCH-001"].latest_event == "Harvested in Coorg"
    )

    scenario.h2("Reject an unauthorized updater")
    contract.add_journey_event(
        sp.record(batch_id="BATCH-001", step=1, event="Packed"),
        _sender=stranger,
        _valid=False,
    )

    scenario.h2("Reject an event that skips a step")
    contract.add_journey_event(
        sp.record(batch_id="BATCH-001", step=2, event="Shipped"),
        _sender=producer,
        _valid=False,
    )

    scenario.h2("Accept the next event in order")
    contract.add_journey_event(
        sp.record(batch_id="BATCH-001", step=1, event="Packed"),
        _sender=producer,
    )
    scenario.verify(contract.data.batches["BATCH-001"].next_step == 2)
    scenario.verify(contract.data.batches["BATCH-001"].latest_event == "Packed")
    scenario.verify(
        contract.data.batches["BATCH-001"].events
        == ["Packed", "Harvested in Coorg"]
    )

    scenario.h2("Reject a duplicate batch ID")
    contract.register_batch(
        sp.record(batch_id="BATCH-001", first_event="Different origin"),
        _sender=producer,
        _valid=False,
    )
#In our demo, say the contract and test scenario are included, but tests haven’t passed yet and it hasn’t been deployed.
