from bot import Bot
import os
    
def main():
    if token := os.environ['MR_PUKEKO_TOKEN']:
        client = Bot(token)
        client.run()
    else:
        raise EnvironmentError("Token not found in system environment variables.\n Set MR_PUKEKO_TOKEN environment variable.")

if __name__ == "__main__":
    main()

