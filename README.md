Example repo for a time locked contract.
---

The contract given in template.clvm allows alice to spend at any time or bob to spend after
a certain number of seconds.  The test in tests/test_coin.py is discovered by chialisp test
and runs with a fresh simulation each time, allowing us to check the global effects of taking
actions on the chia blockchain.

The purpose of 'chialisp test' is to provide an analog to truffle's ethereum unit tests
in javascript (https://www.trufflesuite.com/docs/truffle/testing/writing-tests-in-javascript).
which uses web3 to communicate with a local blockchain simulator.  In chia's case,
the code required to simulate the blockchain is already packaged in chialisp_dev_utility
and we provide a python unittest compatible wrapper to allow tests to be written in a
succinct style.

I provide a domain specific vocabulary for running tests on chia contracts: Wallet,
ContractWrapper, Network with allow the user to interact with the running simulation
that is freshly created for each test.

