# Spamhaus NFQUEUE Block

This is Python code to block IPv4 addresses that Spamhaus identifies as malware.

## Files/Directories
- `main.py`: Main script.
- `config.py`: Configuration file. You can run it to see your current configuration.
- `iptables.py`: Script to set up iptables. You can run it to automatically set/remove iptables rules.
- `util.py`: Extension for `main.py` to fetch and parse Spamhaus data.
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

4. The `config.py` file is ready to use by default. However, you may want to change only `NFQUEUE_NUM`, `IPTABLES_CHAINS`, and/or `EXPIRE_AFTER`.

5. Run `main.py` as root. The script will now block bad addresses:
    ```shell
    python main.py
    # To suppress 'DROP packet from/to {src_ip}' display:
    python main.py > /dev/null
    ```

## Notes
- Ensure your operating system is GNU/Linux.
- This script works only with iptables, so ensure you have iptables installed.
- I tested it with Python 3.12.7, Arch Linux, and iptables v1.8.10 (legacy).
- If you change iptables rules, ensure that the script's rules are below others. Alternatively, stop the script, change the rules, and run it again.
- The script updates the blocklist once per start.


## License
GNU General v3. Check the `COPYING` file