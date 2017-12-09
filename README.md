# GAMEr

*Power-up your machine to solve GAME models*

[![Python version](https://img.shields.io/badge/Python-2.7-blue.svg)](https://www.python.org/download/releases/2.7.1/)

[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://opensource.org/licenses/Apache-2.0) [![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/sirfoga/gamer/issues) [![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)


## Key Features
The algorithm itself is quite naive and can be extended to support many other kind of cloud computing.
The core of the algorithm relies in a simple `while` loop:

```python
while keep_going_on:
    scan_config_folder()  # that somebody put there previously
    parse_configs_found()
    launch_multithreading_alg()  # using (100 - x) % CPU
    wait_until_all_done()
    write_output()  # send email, write logs, enjoy a beer ...
```

The idea is to run at full speed (or at least at `(100 - x) %` CPU) long computations and to run as many as possible in a parallel way.

## Install
No need to install anything out of the ordinary, just the standard python lib and the depedencies needed to run the [GAME algorithm](https://github.com/grazianoucci/game).


## Questions and issues
The [github issue tracker](https://github.com/sirfoga/gamer/issues) is **only** for bug reports and feature requests. Anything else, such as questions for help in using the library, should be posted as [pull requests](https://github.com/sirfoga/gamer/pulls).


## Contributing
[Fork](https://github.com/sirfoga/gamer/fork) | Patch | Push | [Pull request](https://github.com/sirfoga/gamer/pulls)


## License
[Apache License](http://www.apache.org/licenses/LICENSE-2.0) Version 2.0, January 2004


## You may also like...

- [GAME](https://github.com/grazianoucci/game) - Original algorithm
- [GAMEplayground](https://github.com/Archetipo95/GAMEplayground) - Web interface for cloud-computing GAME models
