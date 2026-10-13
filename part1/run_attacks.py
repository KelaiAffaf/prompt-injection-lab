"""Run every attack several times against the agent and print success rates.

Usage:
    python run_attacks.py              # naive agent
    python run_attacks.py --hardened   # agent with the first defense
    python run_attacks.py --runs 5     # fewer calls
"""
import argparse

from agent import summarize, summarize_hardened
from attacks import ATTACKS, attack_succeeded


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=10, help="calls per attack")
    parser.add_argument("--hardened", action="store_true", help="use the hardened agent")
    args = parser.parse_args()

    agent = summarize_hardened if args.hardened else summarize
    label = "hardened" if args.hardened else "naive"
    print(f"Agent: {label}, {args.runs} runs per attack\n")

    results = {}
    for name, payload in ATTACKS.items():
        wins = sum(attack_succeeded(agent(payload)) for _ in range(args.runs))
        results[name] = wins / args.runs
        print(f"{name:<25} success rate: {results[name]:.0%}")

    overall = sum(results.values()) / len(results)
    print(f"\n{'overall':<25} success rate: {overall:.0%}")


if __name__ == "__main__":
    main()
