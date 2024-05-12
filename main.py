from argparse import Namespace, ArgumentParser
from os import environ
from typing import Optional

from src.engine import SearchEngine


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--openai-key", type=str, required=False, default=None)
    parser.add_argument("--gpt-version", type=str, required=False, default=SearchEngine.GPT3_5)
    parser.add_argument("--num-candidates", type=int, required=False, default=SearchEngine.DEFAULT_NUM_CANDIDATES)
    parser.add_argument("--num-results", type=int, required=False, default=SearchEngine.DEFAULT_NUM_RESULTS)
    return parser.parse_args()


def run(openai_key: Optional[str], gpt_version: str, num_candidates: int, num_results: int) -> None:
    if openai_key is None:
        openai_key = environ.get("OPENAI_API_KEY")
        if openai_key is None:
            print(
                "[WARNING] OpenAI API key was not provided in the CMD line arguments "
                "and OPENAI_API_KEY was not found in environment variables. "
                "The program will not be able to summarize semantic search results using GPT."
            )

    use_gpt = False
    search_engine = SearchEngine(
        openai_key=openai_key,
        gpt_version=gpt_version,
        num_candidates=num_candidates,
        max_results=num_results
    )
    print("Semantic search engine initialized!")

    try:
        while True:
            query = input(("[gpt] " if use_gpt else "") + ">>> ")

            if query == "\t":
                use_gpt = not use_gpt
                continue

            try:
                if use_gpt and openai_key is None:
                    print(
                        "Unable to use GPT summarization because OpenAI API key was not provided. "
                        "Type and enter the TAB key to disable RAG to GPT pipeline."
                    )
                    continue

                print(search_engine.semantic_search(query, use_gpt=use_gpt))

            except ValueError:
                pass

    except KeyboardInterrupt:
        print("Program terminated.")
        return


if __name__ == "__main__":
    run(**vars(parse_args()))
