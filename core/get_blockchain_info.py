import requests


def get_block_data(block_hash: str) -> dict:
    url = f"https://blockchain.info/rawblock/{block_hash}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()


def run():
    # Example usage
    block_hash = "0000000000000bae09a7a393a8acded75aa67e46cb81f7acaa5ad94f9eacd103"
    block_data = get_block_data(block_hash)

    for key, item in block_data.items():
        print(key)
        print(item)
        print("---------------------------------------")


if __name__ == '__main__':
    run()
