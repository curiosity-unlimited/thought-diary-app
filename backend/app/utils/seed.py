"""
Development seed data module.

This module provides functionality to populate the database with sample data
for development and testing purposes. It creates sample users and thought diary
entries with realistic content and sentiment analysis.

Example:
    Run from command line:
        $ flask seed

    Or programmatically:
        >>> from app.utils.seed import seed_all
        >>> seed_all(clear_existing=True)
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta, UTC

from app.extensions import db
from app.models import User, ThoughtDiary


# Sample users data
SAMPLE_USERS: List[Dict[str, str]] = [
    {
        "email": "alice@example.com",
        "password": "Alice123!",  # Dev only - meets strict password requirements
    },
    {
        "email": "bob@example.com",
        "password": "Bob123!",  # Dev only - meets strict password requirements
    },
]

# Sample diary entries with pre-analyzed content
# These entries demonstrate positive, negative, and neutral sentiments
SAMPLE_DIARIES: List[Dict[str, Any]] = [
    {
        "content": "I felt both excitement and anxious after I got elected to join a team for international math competition.",
        "analyzed_content": 'I felt both <span class="positive">excitement</span> and <span class="negative">anxious</span> after I got elected to join a team for international math competition.',
        "positive_count": 1,
        "negative_count": 1,
        "days_ago": 1,
    },
    {
        "content": "Today was amazing! I finally completed my project and received wonderful feedback from my mentor. I feel accomplished and proud.",
        "analyzed_content": 'Today was <span class="positive">amazing</span>! I finally <span class="positive">completed</span> my project and received <span class="positive">wonderful</span> feedback from my mentor. I feel <span class="positive">accomplished</span> and <span class="positive">proud</span>.',
        "positive_count": 5,
        "negative_count": 0,
        "days_ago": 2,
    },
    {
        "content": "I'm feeling overwhelmed with all the deadlines. Everything seems impossible and I can't stop worrying about failing.",
        "analyzed_content": 'I\'m feeling <span class="negative">overwhelmed</span> with all the deadlines. Everything seems <span class="negative">impossible</span> and I can\'t stop <span class="negative">worrying</span> about <span class="negative">failing</span>.',
        "positive_count": 0,
        "negative_count": 4,
        "days_ago": 3,
    },
    {
        "content": "Had a productive meeting with the team. We discussed the project timeline and assigned tasks.",
        "analyzed_content": 'Had a <span class="positive">productive</span> meeting with the team. We discussed the project timeline and assigned tasks.',
        "positive_count": 1,
        "negative_count": 0,
        "days_ago": 4,
    },
    {
        "content": "I struggled with the coding problem for hours. It was frustrating, but I finally solved it and learned something new.",
        "analyzed_content": 'I <span class="negative">struggled</span> with the coding problem for hours. It was <span class="negative">frustrating</span>, but I finally <span class="positive">solved</span> it and <span class="positive">learned</span> something new.',
        "positive_count": 2,
        "negative_count": 2,
        "days_ago": 5,
    },
    {
        "content": "Spent the afternoon at the park. Weather was nice. Read a book.",
        "analyzed_content": 'Spent the afternoon at the park. Weather was <span class="positive">nice</span>. Read a book.',
        "positive_count": 1,
        "negative_count": 0,
        "days_ago": 6,
    },
    {
        "content": "Today I felt grateful for my supportive friends. They encouraged me when I was feeling down and helped me see the positive side.",
        "analyzed_content": 'Today I felt <span class="positive">grateful</span> for my <span class="positive">supportive</span> friends. They <span class="positive">encouraged</span> me when I was feeling <span class="negative">down</span> and helped me see the <span class="positive">positive</span> side.',
        "positive_count": 4,
        "negative_count": 1,
        "days_ago": 7,
    },
    {
        "content": "Had a terrible day. Everything went wrong from the moment I woke up. Feeling stressed and disappointed.",
        "analyzed_content": 'Had a <span class="negative">terrible</span> day. Everything went <span class="negative">wrong</span> from the moment I woke up. Feeling <span class="negative">stressed</span> and <span class="negative">disappointed</span>.',
        "positive_count": 0,
        "negative_count": 4,
        "days_ago": 8,
    },
    {
        "content": "Attended a workshop on mindfulness. It was interesting and gave me new techniques to manage stress.",
        "analyzed_content": 'Attended a workshop on mindfulness. It was <span class="positive">interesting</span> and gave me new techniques to manage stress.',
        "positive_count": 1,
        "negative_count": 0,
        "days_ago": 9,
    },
    {
        "content": "Reflected on my progress this month. Some ups and downs, but overall I'm moving forward. Need to stay focused.",
        "analyzed_content": 'Reflected on my progress this month. Some ups and downs, but overall I\'m <span class="positive">moving forward</span>. Need to stay <span class="positive">focused</span>.',
        "positive_count": 2,
        "negative_count": 0,
        "days_ago": 10,
    },
]


def clear_data() -> None:
    """
    Clear all existing data from the database.

    This function removes all thought diary entries and users from the database.
    Use with caution as this operation is irreversible.

    Note:
        This should only be used in development environments.
    """
    ThoughtDiary.query.delete()
    User.query.delete()
    db.session.commit()
    print("✓ Cleared existing data")


def create_sample_users() -> List[User]:
    """
    Create sample users with hashed passwords.

    Returns:
        List[User]: List of created User objects.

    Note:
        Passwords meet strict validation requirements:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one number
        - At least one special character
    """
    users = []
    for user_data in SAMPLE_USERS:
        # Check if user already exists
        existing_user = User.query.filter_by(email=user_data["email"]).first()
        if existing_user:
            users.append(existing_user)
            print(f"✓ User {user_data['email']} already exists")
            continue

        user = User(email=user_data["email"])
        user.set_password(user_data["password"])
        db.session.add(user)
        users.append(user)
        print(f"✓ Created user: {user_data['email']}")

    db.session.commit()
    return users


def create_sample_diaries(users: List[User]) -> None:
    """
    Create sample thought diary entries for each user.

    Args:
        users: List of User objects to create diaries for.

    Note:
        Each diary entry includes:
        - Original content
        - Analyzed content with sentiment span tags
        - Positive and negative word counts
        - Realistic timestamps (backdated for variety)
    """
    for user in users:
        print(f"\nCreating diaries for {user.email}:")
        for diary_data in SAMPLE_DIARIES:
            # Calculate created_at timestamp
            created_at = datetime.now(UTC) - timedelta(days=diary_data["days_ago"])

            diary = ThoughtDiary(
                user_id=user.id,
                content=diary_data["content"],
                analyzed_content=diary_data["analyzed_content"],
                positive_count=diary_data["positive_count"],
                negative_count=diary_data["negative_count"],
                created_at=created_at,
                updated_at=created_at,
            )
            db.session.add(diary)
            print(
                f"  ✓ Created diary (pos: {diary_data['positive_count']}, "
                f"neg: {diary_data['negative_count']}, {diary_data['days_ago']} days ago)"
            )

    db.session.commit()


def seed_all(clear_existing: bool = False) -> None:
    """
    Run all seeding operations.

    This is the main function to populate the database with sample data.
    It is idempotent and can be run multiple times safely.

    Args:
        clear_existing: If True, clears all existing data before seeding.
                       Defaults to False.

    Example:
        >>> from app.utils.seed import seed_all
        >>> seed_all(clear_existing=True)
    """
    print("\n" + "=" * 60)
    print("Starting database seeding...")
    print("=" * 60 + "\n")

    if clear_existing:
        clear_data()

    users = create_sample_users()
    create_sample_diaries(users)

    print("\n" + "=" * 60)
    print("✓ Database seeding completed successfully!")
    print(f"  - Created {len(users)} users")
    print(f"  - Created {len(SAMPLE_DIARIES) * len(users)} diary entries")
    print("=" * 60 + "\n")
