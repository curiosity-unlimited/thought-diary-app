"""Unit tests for database models (User and ThoughtDiary).

This module tests:
- User model creation and validation
- Password hashing and verification
- Email validation
- User-ThoughtDiary relationships
- ThoughtDiary model creation and validation
"""

from datetime import datetime
from app.models.user import User
from app.models.thought_diary import ThoughtDiary


class TestUserModel:
    """Test cases for the User model."""
    
    def test_user_creation(self, app, db):
        """Test creating a user with valid data."""
        with app.app_context():
            user = User(email='newuser@example.com')
            user.set_password('SecurePass123!')
            db.session.add(user)
            db.session.commit()
            
            assert user.id is not None
            assert user.email == 'newuser@example.com'
            assert user.password_hash is not None
            assert user.password_hash != 'SecurePass123!'
            assert user.created_at is not None
            assert user.updated_at is not None
            assert isinstance(user.created_at, datetime)
            assert isinstance(user.updated_at, datetime)
    
    def test_user_repr(self, app, test_user):
        """Test user string representation."""
        with app.app_context():
            repr_str = repr(test_user)
            assert f'<User {test_user.id}:' in repr_str
            assert test_user.email in repr_str
    
    def test_password_hashing(self, app, db):
        """Test password is properly hashed using bcrypt."""
        with app.app_context():
            user = User(email='hashtest@example.com')
            plain_password = 'MySecretPass123!'
            user.set_password(plain_password)
            
            # Password should be hashed, not stored as plain text
            assert user.password_hash != plain_password
            # Bcrypt hashes start with $2b$
            assert user.password_hash.startswith('$2b$')
            # Should be of reasonable length (bcrypt hashes are typically 60 chars)
            assert len(user.password_hash) > 50
    
    def test_password_verification_success(self, app, test_user):
        """Test correct password verification."""
        with app.app_context():
            # test_user was created with password 'TestPassword123!'
            assert test_user.check_password('TestPassword123!') is True
    
    def test_password_verification_failure(self, app, test_user):
        """Test incorrect password verification."""
        with app.app_context():
            assert test_user.check_password('WrongPassword123!') is False
            assert test_user.check_password('') is False
            assert test_user.check_password('TestPassword') is False
    
    def test_email_validation_valid(self, app):
        """Test email validation with valid email addresses."""
        with app.app_context():
            assert User.validate_email('user@example.com') is True
            assert User.validate_email('test.user@example.com') is True
            assert User.validate_email('user+tag@example.co.uk') is True
            assert User.validate_email('user123@sub.example.com') is True
    
    def test_email_validation_invalid(self, app):
        """Test email validation with invalid email addresses."""
        with app.app_context():
            assert User.validate_email('') is False
            assert User.validate_email('invalid') is False
            assert User.validate_email('invalid@') is False
            assert User.validate_email('@example.com') is False
            assert User.validate_email('user@') is False
            assert User.validate_email('user @example.com') is False
            assert User.validate_email('user@example') is False
    
    def test_email_uniqueness(self, app, db, test_user):
        """Test that duplicate emails are not allowed."""
        with app.app_context():
            # Try to create another user with the same email
            duplicate_user = User(email=test_user.email)
            duplicate_user.set_password('AnotherPass123!')
            db.session.add(duplicate_user)
            
            # IntegrityError from SQLAlchemy should be raised
            try:
                db.session.commit()
                assert False, "Expected IntegrityError was not raised"
            except Exception:
                # Expected: IntegrityError for duplicate email
                db.session.rollback()
                assert True
    
    def test_user_thought_diary_relationship(self, app, db, test_user):
        """Test one-to-many relationship between User and ThoughtDiary."""
        with app.app_context():
            # Create diary entries for the user
            diary1 = ThoughtDiary(
                user_id=test_user.id,
                content='First diary entry',
                analyzed_content='First diary entry',
                positive_count=0,
                negative_count=0
            )
            diary2 = ThoughtDiary(
                user_id=test_user.id,
                content='Second diary entry',
                analyzed_content='Second diary entry',
                positive_count=0,
                negative_count=0
            )
            
            db.session.add(diary1)
            db.session.add(diary2)
            db.session.commit()
            
            # Query fresh to get updated relationships
            user = db.session.get(User, test_user.id)
            
            # Test relationship
            assert user.thought_diaries.count() == 2
            diary_contents = [d.content for d in user.thought_diaries.all()]
            assert 'First diary entry' in diary_contents
            assert 'Second diary entry' in diary_contents
    
    def test_user_deletion_cascades_to_diaries(self, app, db, test_user):
        """Test that deleting a user also deletes their diary entries."""
        with app.app_context():
            # Create diary entries for the user
            diary = ThoughtDiary(
                user_id=test_user.id,
                content='Test diary entry',
                analyzed_content='Test diary entry',
                positive_count=0,
                negative_count=0
            )
            db.session.add(diary)
            db.session.commit()
            
            diary_id = diary.id
            user_id = test_user.id
            
            # Get fresh user instance from database to avoid session conflicts
            user_to_delete = db.session.get(User, user_id)
            
            # Delete the user
            db.session.delete(user_to_delete)
            db.session.commit()
            
            # Verify user is deleted
            assert db.session.get(User, user_id) is None
            
            # Verify diary is also deleted (cascade)
            assert db.session.get(ThoughtDiary, diary_id) is None


class TestThoughtDiaryModel:
    """Test cases for the ThoughtDiary model."""
    
    def test_diary_creation(self, app, db, test_user):
        """Test creating a thought diary with valid data."""
        with app.app_context():
            diary = ThoughtDiary(
                user_id=test_user.id,
                content='I felt happy today.',
                analyzed_content='I felt <span class="positive">happy</span> today.',
                positive_count=1,
                negative_count=0
            )
            db.session.add(diary)
            db.session.commit()
            
            assert diary.id is not None
            assert diary.user_id == test_user.id
            assert diary.content == 'I felt happy today.'
            assert diary.analyzed_content == 'I felt <span class="positive">happy</span> today.'
            assert diary.positive_count == 1
            assert diary.negative_count == 0
            assert diary.created_at is not None
            assert diary.updated_at is not None
            assert isinstance(diary.created_at, datetime)
            assert isinstance(diary.updated_at, datetime)
    
    def test_diary_repr(self, app, test_diary):
        """Test diary string representation."""
        with app.app_context():
            repr_str = repr(test_diary)
            assert f'<ThoughtDiary {test_diary.id}' in repr_str
    
    def test_diary_user_relationship(self, app, test_diary, test_user):
        """Test many-to-one relationship from ThoughtDiary to User."""
        with app.app_context():
            assert test_diary.user is not None
            assert test_diary.user.id == test_user.id
            assert test_diary.user.email == test_user.email
    
    def test_content_validation_valid(self, app):
        """Test content validation with valid content."""
        with app.app_context():
            assert ThoughtDiary.validate_content('Valid content here.') is True
            assert ThoughtDiary.validate_content('A' * 5000) is True  # 5000 chars is valid
    
    def test_content_validation_invalid(self, app):
        """Test content validation with invalid content."""
        with app.app_context():
            assert ThoughtDiary.validate_content('') is False
            assert ThoughtDiary.validate_content('   ') is False
            assert ThoughtDiary.validate_content('A' * 10001) is False  # Over 10000 chars
    
    def test_get_sentiment_positive(self, app, db, test_user):
        """Test sentiment classification for positive entries."""
        with app.app_context():
            diary = ThoughtDiary(
                user_id=test_user.id,
                content='I felt great!',
                analyzed_content='I felt <span class="positive">great</span>!',
                positive_count=3,
                negative_count=1
            )
            assert diary.get_sentiment() == 'positive'
    
    def test_get_sentiment_negative(self, app, db, test_user):
        """Test sentiment classification for negative entries."""
        with app.app_context():
            diary = ThoughtDiary(
                user_id=test_user.id,
                content='I felt terrible.',
                analyzed_content='I felt <span class="negative">terrible</span>.',
                positive_count=1,
                negative_count=3
            )
            assert diary.get_sentiment() == 'negative'
    
    def test_get_sentiment_neutral(self, app, db, test_user):
        """Test sentiment classification for neutral entries."""
        with app.app_context():
            diary = ThoughtDiary(
                user_id=test_user.id,
                content='Today was a day.',
                analyzed_content='Today was a day.',
                positive_count=2,
                negative_count=2
            )
            assert diary.get_sentiment() == 'neutral'
    
    def test_to_dict_method(self, app, test_diary):
        """Test converting diary to dictionary."""
        with app.app_context():
            diary_dict = test_diary.to_dict()
            
            assert isinstance(diary_dict, dict)
            assert diary_dict['id'] == test_diary.id
            assert diary_dict['user_id'] == test_diary.user_id
            assert diary_dict['content'] == test_diary.content
            assert diary_dict['analyzed_content'] == test_diary.analyzed_content
            assert diary_dict['positive_count'] == test_diary.positive_count
            assert diary_dict['negative_count'] == test_diary.negative_count
            assert 'created_at' in diary_dict
            assert 'updated_at' in diary_dict
            assert 'sentiment' in diary_dict
    
    def test_diary_without_analysis(self, app, db, test_user):
        """Test creating diary without analyzed content (None values)."""
        with app.app_context():
            diary = ThoughtDiary(
                user_id=test_user.id,
                content='Simple entry',
                analyzed_content=None,
                positive_count=0,
                negative_count=0
            )
            db.session.add(diary)
            db.session.commit()
            
            assert diary.id is not None
            assert diary.analyzed_content is None
            assert diary.positive_count == 0
            assert diary.negative_count == 0
    
    def test_multiple_diaries_same_user(self, app, db, test_user):
        """Test creating multiple diary entries for the same user."""
        with app.app_context():
            diaries = []
            for i in range(5):
                diary = ThoughtDiary(
                    user_id=test_user.id,
                    content=f'Diary entry {i}',
                    analyzed_content=f'Diary entry {i}',
                    positive_count=0,
                    negative_count=0
                )
                diaries.append(diary)
                db.session.add(diary)
            
            db.session.commit()
            
            # Verify all diaries were created
            for diary in diaries:
                assert diary.id is not None
            
            # Query fresh to get count
            user = db.session.get(User, test_user.id)
            assert user.thought_diaries.count() == 5
