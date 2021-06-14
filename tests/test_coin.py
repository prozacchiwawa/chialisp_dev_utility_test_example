from lib.std.test import TestGroup
from lib.std.types.program import Program
from lib.std.util.load_clvm import load_clvm

from clvm_tools.curry import curry

class CoinTests(TestGroup):
    # Imagine we have coin that lets bob spend it after 60 seconds, or alice at any time.
    def start_test(self):
        self.coin_amount = int(0.0987654321 * self.coin_multiple)

        template_program = load_clvm('template.clvm')

        # Make wallets for our actors.
        alice = self.network.make_wallet('alice')
        bob = self.network.make_wallet('bob')

        # Load the contract and set alice and bob as the participants.
        coin_source = template_program.curry(
            alice.puzzle_hash,
            bob.puzzle_hash,
            self.coin_amount,
            60
        )

        # Time skipping allows us to farm some coins.
        self.network.skip_time('10s', farmer=alice)
        self.network.skip_time('10s', farmer=bob)

        # Check that the bundle can be launched
        hwcoin = alice.launch_contract(coin_source, amt=self.coin_amount)
        assert hwcoin

        # Return the contract's new coin and the actors.
        return hwcoin, alice, bob

    # Check that bob can't spend the coin right away.
    def test_bob_cant_spend(self):
        hwcoin, alice, bob = self.start_test()
        bob_start_balance = bob.balance()

        res = bob.spend_coin(hwcoin)

        assert res.error
        assert bob.balance() <= bob_start_balance

    # Check that alice cna spend the coin right away.
    def test_alice_can_recover(self):
        hwcoin, alice, bob = self.start_test()
        alice_start_balance = alice.balance()

        # Check that alice can spend before 2 days.
        res = alice.spend_coin(hwcoin, args=[alice.puzzle_hash])
        alice_payment = res.find_standard_coins(alice.puzzle_hash)

        assert len(alice_payment) > 0
        assert alice.balance() >= alice_start_balance
        assert alice_payment[0].amount == self.coin_amount

    # Check that bob can spend the coin after the timeout.
    def test_bob_can_spend_later(self):
        hwcoin, alice, bob = self.start_test()
        bob_start_balance = bob.balance()

        # Check that bob can spend after interval
        self.network.skip_time('5m')
        res = bob.spend_coin(hwcoin, args=[bob.puzzle_hash])
        bob_payment = res.find_standard_coins(bob.puzzle_hash)
        assert len(bob_payment) > 0
        assert bob.balance() >= bob_start_balance