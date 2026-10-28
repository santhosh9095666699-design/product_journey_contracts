# TraceTrail

TraceTrail is a minimal Tezos smart contract prototype for recording a product batch's journey. It stores a batch's latest event and enforces that journey events are submitted by the batch's registering account and in sequential order.

## What it does

- Registers a unique batch ID and its first event.
- Lets only the registering account add journey events for that batch.
- Requires each journey event to use the next step number, preventing skipped or repeated steps.
- Keeps the full event list, latest event, and next expected step on-chain. The list is stored newest first to keep updates simple.

The contract stores only short text descriptions. It does not verify that a reported event is physically true, and this prototype has no role transfer or consumer lookup UI. Avoid putting private or sensitive information on-chain.

## Files

- `trace_trail.py` — SmartPy contract and scenario tests.

## Run and verify

1. Open [SmartPy IDE](https://smartpy.io/ide) in a browser.
2. Paste the full contents of `trace_trail.py` into a new file in the IDE.
3. Run the code. The scenario checks successful registration and ordered updates, plus rejection of an unauthorized update, a skipped step, and duplicate registration.
4. Confirm the IDE reports that compilation and the scenario completed successfully before presenting this as verified.

SmartPy's IDE compiles the contract and runs its test scenario. The local development environment used to prepare this repository did not have Python or SmartPy installed, so local tests have not been run here.

## Example flow

1. `register_batch("BATCH-001", "Harvested in Coorg")`
2. `add_journey_event("BATCH-001", 1, "Packed")`
3. `add_journey_event("BATCH-001", 2, "Shipped")`

Each write is an on-chain operation when deployed. This repository has not been deployed to a Tezos network.

## GitHub

Create a new public repository named `TraceTrail`, then upload `trace_trail.py` and this README. Add a `.gitignore` or license later if your team needs one. Do not upload wallet secrets, seed phrases, or private keys.

## Optional testnet demo

Only attempt this after the IDE tests pass and you still have time. A deployment requires a Tezos testnet wallet and test tokens. Use a testnet account only, never share its recovery phrase or private key, and do not deploy with real funds. The contract has not been deployed as part of this project.
