# Spamhaus NFQUEUE Block

This is Python code to block IPv4/IPv6 addresses that Spamhaus identifies as malware.

## Files/Directories
- `main4.py`: Main script for IPv4.
- `main6.py`: Main Script for IPv6
- `config.py`: Configuration file. You can run it to see your current configuration.
- `iptables.py`: Extension for `main{4,6}.py` to set up/clean iptables rules
- `util.py`: Extension for `main{4,6}.py` to fetch and parse Spamhaus data.
- `cache/`: Directory for caching Spamhaus data and the last data fetch in UNIX timestamp.

## Usage
0. Open a root shell
1. Create a virtual environment:
    ```shell
    python -m venv env
    ```
2. Activate the virtual environment:
    ```shell
    source env/bin/activate
    ```
3. Install requirements:
    ```shell
    pip install -r requirements.txt
    ```

4. The `config.py` file is ready to use by default. However, you may want to change some values.

5. Run `main4.py` or `main6.py` as root or with Python binary with CAP_NET_ADMIN. The script will now block bad addresses:
    ```shell
    # For IPv4
    ## Show all output
    python main4.py
    ## To suppress 'DROP packet from/to {src_ip}' display:
    python main4.py > /dev/null

    # For IPv6
    ## Show all output
    python main4.py
    ## To suppress non-error inforamation display:
    python main4.py > /dev/null
    ```

## Contributing

I welcome contributions to this project! If you have suggestions, improvements, or bug fixes, please feel free to submit a pull request.

## Notes
- Ensure your operating system is GNU/Linux.


- This script works only with iptables, so ensure you have iptables installed.


- I tested it with Python 3.12.7, Arch Linux, and iptables v1.8.10 (legacy).


- If you change iptables rules, ensure that the script's rules are below others. Alternatively, stop the script, change the rules, and run it again.


- The script updates the blocklist once per start if the cache has expired.


- <i>This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.</i>


## License
GNU General Public License v3. Check the `COPYING` file