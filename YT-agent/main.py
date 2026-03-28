"""
YT-agent – Kundensupport-Agent für Sandras Friseurwagon
========================================================
Ein vollständiger Kundensupport-Chatbot powered by Claude Agent SDK.
Unterstützt mehrstufige Gespräche mit Sitzungsgedächtnis.
"""

import asyncio
import os
from dotenv import load_dotenv

from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    AssistantMessage,
    ResultMessage,
    TextBlock,
    ClaudeSDKError,
    CLINotFoundError,
    CLIConnectionError,
    ProcessError,
)
from config import SYSTEM_PROMPT

load_dotenv()


def check_api_key() -> None:
    if not os.getenv("ANTHROPIC_API_KEY"):
        raise EnvironmentError(
            "ANTHROPIC_API_KEY nicht gesetzt.\n"
            "Kopiere .env.example zu .env und trage deinen API-Key ein."
        )


def build_options() -> ClaudeAgentOptions:
    return ClaudeAgentOptions(
        system_prompt=SYSTEM_PROMPT,
        # Nur sichere, lesende Tools erlaubt – kein Bash, kein Write
        allowed_tools=["WebFetch", "WebSearch"],
        permission_mode="default",
        model="claude-haiku-4-5",
        max_turns=30,
    )


def print_header() -> None:
    print("\n" + "=" * 60)
    print("  Willkommen beim Sandras Friseurwagon Kundensupport!")
    print("  Powered by Claude Agent SDK")
    print("  Tippe 'exit' oder 'quit' zum Beenden")
    print("=" * 60 + "\n")


async def run_chat() -> None:
    check_api_key()
    print_header()

    options = build_options()

    async with ClaudeSDKClient(options=options) as client:
        while True:
            try:
                user_input = input("Du: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n\nTschüss! Bis zum nächsten Mal. ✂️")
                break

            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit", "bye", "tschüss"):
                print("\nTschüss! Wir freuen uns auf deinen Besuch. ✂️")
                break

            await client.query(user_input)

            print("\nAssistent: ", end="", flush=True)
            response_received = False

            async for message in client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            print(block.text, end="", flush=True)
                            response_received = True
                elif isinstance(message, ResultMessage):
                    if message.is_error:
                        result_text = (message.result or "").lower()
                        if "maximum turns" in result_text or "max_turns" in result_text:
                            print(
                                "\n[Gesprächslimit erreicht. Bitte starte ein neues Gespräch "
                                "oder ruf uns an: +43 67763349550]"
                            )
                        else:
                            print(f"\n[Fehler aufgetreten. Bitte versuch es erneut.]")
                    elif not response_received and message.result:
                        print(message.result, end="", flush=True)

            print("\n")


def main() -> None:
    try:
        asyncio.run(run_chat())
    except EnvironmentError as e:
        print(f"\n[Konfigurationsfehler] {e}\n")
    except CLINotFoundError:
        print(
            "\n[Fehler] Claude Code CLI nicht gefunden.\n"
            "Installiere es mit: npm install -g @anthropic-ai/claude-code\n"
        )
    except CLIConnectionError as e:
        print(f"\n[Verbindungsfehler] {e}\n")
    except ProcessError as e:
        print(f"\n[Prozessfehler] {e.stderr}\n")
    except ClaudeSDKError as e:
        print(f"\n[SDK-Fehler] {e}\n")


if __name__ == "__main__":
    main()
