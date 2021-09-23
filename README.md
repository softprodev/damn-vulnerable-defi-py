This repo contains the challenges from https://www.damnvulnerabledefi.xyz/index.html ported to Python/Brownie.

All challenges have now been ported. Please find more information and challenge details in the link above.

Should just work out the box assuming you have brownie and pytest set up. 

Choose your challenge in the test folder and fill in run_exploit(). All tests should fail in the after() function before an exploit is implemented.

Command to run your test (using test_unstoppable_challenge.py) - brownie test -k test_unstoppable_challenge