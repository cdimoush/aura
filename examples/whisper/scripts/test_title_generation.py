#!/usr/bin/env python3
"""Test script for title generation with diverse sample transcriptions."""

import sys
import time
from generate_title import generate_title

# Test samples covering different types of voice memos
TEST_SAMPLES = [
    {
        "name": "Code/Feature Discussion",
        "text": "I want to refactor the authentication system to use JWT tokens instead of sessions. "
                "The current session-based approach is causing scaling issues and we need something stateless. "
                "JWT will let us distribute auth across multiple services without a shared session store."
    },
    {
        "name": "Meeting Notes",
        "text": "Standup update - finished the user dashboard yesterday, got all the charts working nicely. "
                "Today I'm working on API rate limiting, need to implement token bucket algorithm. "
                "Tomorrow I'll focus on documentation for the new endpoints."
    },
    {
        "name": "Research Ideas",
        "text": "Look into using Redis for caching the API responses, especially for the analytics endpoints. "
                "Those queries are super expensive and they don't change that often. "
                "Could set TTL to like 5 minutes and save a ton of database load."
    },
    {
        "name": "Task List",
        "text": "TODO: update the documentation for the new authentication flow, "
                "fix the mobile responsive layout on the dashboard, "
                "and review the pull requests from the team. "
                "Also need to schedule that deployment for Friday."
    },
    {
        "name": "Short Memo",
        "text": "Call Sarah about the deployment schedule tomorrow morning"
    },
    {
        "name": "Rambling/Unclear",
        "text": "So yeah, um, I was thinking about like, you know, the thing we talked about yesterday. "
                "Maybe we could, uh, try a different approach? Not sure exactly what but, "
                "yeah, something to think about I guess."
    },
    {
        "name": "Technical Discussion",
        "text": "The database migration is failing because of foreign key constraints. "
                "We need to drop the constraints first, run the migration, then re-add them. "
                "Or maybe we should just use a soft delete pattern instead of actually removing rows."
    },
    {
        "name": "Bug Report",
        "text": "Found a critical bug in production - the payment processing is timing out for users with "
                "more than 10 items in their cart. Looks like we're making N+1 queries to the database. "
                "Need to add eager loading for the product relationships ASAP."
    }
]


def main():
    """Run title generation on all test samples and display results."""
    print("Testing Title Generation")
    print("=" * 80)
    print()

    for i, sample in enumerate(TEST_SAMPLES, 1):
        print(f"Test {i}: {sample['name']}")
        print(f"Input: {sample['text'][:100]}{'...' if len(sample['text']) > 100 else ''}")

        try:
            title = generate_title(sample['text'])
            print(f"Generated Title: {title}")
        except Exception as e:
            print(f"Error: {e}")

        print("-" * 80)
        print()

        # Add delay to avoid rate limiting (3 requests per minute limit)
        if i < len(TEST_SAMPLES):
            print("Waiting 20 seconds to avoid rate limits...")
            time.sleep(20)

    print("Testing complete!")


if __name__ == "__main__":
    main()
