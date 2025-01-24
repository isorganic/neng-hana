import asyncio
import aiohttp
from datetime import datetime, timedelta
from colorama import init, Fore, Style
import os

init(autoreset=True)

api_url = "https://hanafuda-backend-app-520478841386.us-central1.run.app/graphql"
headers = {
    'Accept': '*/*',
    'Content-Type': 'application/json',
    'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
}

async def colay(session, url, method, payload_data=None):
    async with session.request(method, url, headers=headers, json=payload_data) as response:
        if response.status != 200:
            raise Exception(f'HTTP error! Status: {response.status}')
        return await response.json()

async def refresh_access_token(session, refresh_token):
    api_key = "AIzaSyDipzN0VRfTPnMGhQ5PSzO27Cxm3DohJGY"
    async with session.post(
        f'https://securetoken.googleapis.com/v1/token?key={api_key}',
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=f'grant_type=refresh_token&refresh_token={refresh_token}'
    ) as response:
        if response.status != 200:
            raise Exception("Failed to refresh access token")
        data = await response.json()
        return data.get('access_token')

async def handle_grow(session, refresh_token):
    new_access_token = await refresh_access_token(session, refresh_token)
    headers['authorization'] = f'Bearer {new_access_token}'

    grow_action_query = {
        "query": """
            mutation executeGrowAction {
                executeGrowAction(withAll: true) {
                    totalValue
                    multiplyRate
                }
                executeSnsShare(actionType: GROW, snsType: X) {
                    bonus
                }
            }
        """,
        "operationName": "executeGrowAction"
    }

    try:
        grow_response = await colay(session, api_url, 'POST', grow_action_query)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format waktu saat ini

        if grow_response and 'data' in grow_response and 'executeGrowAction' in grow_response['data']:
            reward = grow_response['data']['executeGrowAction']['totalValue']
            print(f"{Fore.YELLOW}[{current_time}] Grow successful! Reward: {reward}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[{current_time}] Error: Unexpected response format: {grow_response}{Style.RESET_ALL}")
    except Exception as e:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{Fore.RED}[{current_time}] Error during grow action: {str(e)}{Style.RESET_ALL}")

async def run_grow_periodically(refresh_tokens):
    while True:
        now = datetime.now()
        # Hitung waktu berikutnya pada menit xx:05
        next_run = now.replace(minute=5, second=0, microsecond=0) + timedelta(hours=1) if now.minute >= 5 else now.replace(minute=5, second=0, microsecond=0)
        wait_time = (next_run - now).total_seconds()

        print(f"{Fore.GREEN}[{now.strftime('%Y-%m-%d %H:%M:%S')}] Menunggu hingga {next_run.strftime('%Y-%m-%d %H:%M:%S')} untuk menjalankan grow...{Style.RESET_ALL}")
        await asyncio.sleep(wait_time)  # Tunggu hingga waktu berikutnya

        async with aiohttp.ClientSession() as session:
            for refresh_token in refresh_tokens:
                await handle_grow(session, refresh_token)

def load_refresh_tokens(file_path):
    if not os.path.exists(file_path):
        print(f"{Fore.RED}File {file_path} tidak ditemukan! Pastikan file ada dan coba lagi.{Style.RESET_ALL}")
        return []

    with open(file_path, 'r') as file:
        tokens = [line.strip() for line in file if line.strip()]
    
    if not tokens:
        print(f"{Fore.RED}File {file_path} kosong! Tambahkan refresh token dan coba lagi.{Style.RESET_ALL}")
    return tokens

async def main():
    token_file = "token.txt"  # Nama file yang berisi refresh token
    refresh_tokens = load_refresh_tokens(token_file)

    if not refresh_tokens:
        print(f"{Fore.RED}Tidak ada refresh token yang dapat digunakan. Program berhenti.{Style.RESET_ALL}")
        return

    await run_grow_periodically(refresh_tokens)

if __name__ == '__main__':
    asyncio.run(main())
