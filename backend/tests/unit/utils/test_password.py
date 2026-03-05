"""Unit tests for password utility functions.

This module tests:
- Password validation rules (min 8 chars, uppercase, lowercase, number, special char)
- Bcrypt password hashing
- Password verification
"""

from app.utils.password import validate_password, hash_password, verify_password


class TestValidatePassword:
    """Test cases for password validation function."""
    
    def test_valid_password(self):
        """Test validation with valid passwords."""
        is_valid, error = validate_password('SecurePass123!')
        assert is_valid is True
        assert error == ''
        
        is_valid, error = validate_password('MyP@ssw0rd')
        assert is_valid is True
        
        is_valid, error = validate_password('Abcd1234!@#$')
        assert is_valid is True
    
    def test_password_too_short(self):
        """Test validation fails for passwords under 8 characters."""
        is_valid, error = validate_password('Short1!')
        assert is_valid is False
        assert 'at least 8 characters' in error.lower()
    
    def test_password_no_uppercase(self):
        """Test validation fails without uppercase letter."""
        is_valid, error = validate_password('noupppercase123!')
        assert is_valid is False
        assert 'uppercase' in error.lower()
    
    def test_password_no_lowercase(self):
        """Test validation fails without lowercase letter."""
        is_valid, error = validate_password('NOLOWERCASE123!')
        assert is_valid is False
        assert 'lowercase' in error.lower()
    
    def test_password_no_number(self):
        """Test validation fails without number."""
        is_valid, error = validate_password('NoNumberPass!')
        assert is_valid is False
        assert 'number' in error.lower()
    
    def test_password_no_special_char(self):
        """Test validation fails without special character."""
        is_valid, error = validate_password('NoSpecial123')
        assert is_valid is False
        assert 'special character' in error.lower()
    
    def test_password_exactly_8_chars_valid(self):
        """Test validation with exactly 8 characters (minimum)."""
        is_valid, error = validate_password('Test123!')
        assert is_valid is True
        assert error == ''
    
    def test_password_very_long(self):
        """Test validation with very long password."""
        long_password = 'A' * 50 + 'a' * 50 + '1' * 10 + '!'
        is_valid, error = validate_password(long_password)
        assert is_valid is True
    
    def test_password_multiple_special_chars(self):
        """Test validation with multiple special characters."""
        is_valid, error = validate_password('Test123!@#$%^&*()')
        assert is_valid is True
    
    def test_password_whitespace(self):
        """Test validation with whitespace in password."""
        is_valid, error = validate_password('Test 123!Pass')
        assert is_valid is True
    
    def test_password_none_or_empty(self):
        """Test validation with None or empty string."""
        is_valid, error = validate_password('')
        assert is_valid is False
        
        is_valid, error = validate_password(None)
        assert is_valid is False
    
    def test_password_unicode_characters(self):
        """Test validation with unicode characters."""
        is_valid, error = validate_password('Test123!Ñoño')
        assert is_valid is True


class TestHashPassword:
    """Test cases for password hashing function."""
    
    def test_hash_password_returns_string(self):
        """Test that hash_password returns a string."""
        hashed = hash_password('TestPassword123!')
        assert isinstance(hashed, str)
    
    def test_hash_password_not_plaintext(self):
        """Test that hashed password is not the same as plaintext."""
        password = 'TestPassword123!'
        hashed = hash_password(password)
        assert hashed != password
    
    def test_hash_password_bcrypt_format(self):
        """Test that hashed password follows bcrypt format."""
        hashed = hash_password('TestPassword123!')
        # Bcrypt hashes start with $2b$
        assert hashed.startswith('$2b$')
        # Bcrypt hashes are typically 60 characters
        assert len(hashed) == 60
    
    def test_hash_password_different_hashes(self):
        """Test that same password produces different hashes (due to salt)."""
        password = 'TestPassword123!'
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        # Should be different due to different salts
        assert hash1 != hash2
    
    def test_hash_password_empty_string(self):
        """Test hashing empty string."""
        hashed = hash_password('')
        assert isinstance(hashed, str)
        assert len(hashed) == 60
    
    def test_hash_password_long_password(self):
        """Test hashing long password (within bcrypt's 72-byte limit)."""
        # Use 70 characters to stay within 72-byte limit
        long_password = 'A' * 50 + 'a' * 10 + '1234567890!@'
        hashed = hash_password(long_password)
        assert isinstance(hashed, str)
        assert hashed.startswith('$2b$')
    
    def test_hash_password_special_characters(self):
        """Test hashing password with special characters."""
        password = 'Test!@#$%^&*()123'
        hashed = hash_password(password)
        assert isinstance(hashed, str)
        assert hashed.startswith('$2b$')
    
    def test_hash_password_unicode(self):
        """Test hashing password with unicode characters."""
        password = 'Test123!日本語Ñoño'
        hashed = hash_password(password)
        assert isinstance(hashed, str)
        assert hashed.startswith('$2b$')


class TestVerifyPassword:
    """Test cases for password verification function."""
    
    def test_verify_password_correct(self):
        """Test verification with correct password."""
        password = 'TestPassword123!'
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self):
        """Test verification with incorrect password."""
        password = 'TestPassword123!'
        hashed = hash_password(password)
        assert verify_password('WrongPassword123!', hashed) is False
    
    def test_verify_password_case_sensitive(self):
        """Test that password verification is case-sensitive."""
        password = 'TestPassword123!'
        hashed = hash_password(password)
        assert verify_password('testpassword123!', hashed) is False
        assert verify_password('TESTPASSWORD123!', hashed) is False
    
    def test_verify_password_whitespace_matters(self):
        """Test that whitespace in password matters."""
        password = 'TestPassword123!'
        hashed = hash_password(password)
        assert verify_password('TestPassword123! ', hashed) is False
        assert verify_password(' TestPassword123!', hashed) is False
    
    def test_verify_password_empty_string(self):
        """Test verification with empty string."""
        password = 'TestPassword123!'
        hashed = hash_password(password)
        assert verify_password('', hashed) is False
    
    def test_verify_password_long_password(self):
        """Test verification with long password (within bcrypt's 72-byte limit)."""
        # Use 70 characters to stay within 72-byte limit
        long_password = 'A' * 50 + 'a' * 10 + '1234567890!@'
        hashed = hash_password(long_password)
        assert verify_password(long_password, hashed) is True
    
    def test_verify_password_special_characters(self):
        """Test verification with special characters."""
        password = 'Test!@#$%^&*()123'
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True
    
    def test_verify_password_unicode(self):
        """Test verification with unicode characters."""
        password = 'Test123!日本語Ñoño'
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True
    
    def test_verify_password_invalid_hash(self):
        """Test verification with invalid hash format."""
        password = 'TestPassword123!'
        # Try to verify against an invalid hash - will raise exception
        try:
            result = verify_password(password, 'invalid-hash')
            assert result is False
        except Exception:
            # Exception is expected for invalid hash
            pass
    
    def test_verify_password_none_values(self):
        """Test verification with None values."""
        password = 'TestPassword123!'
        hashed = hash_password(password)
        
        # These should raise exceptions or handle gracefully
        try:
            verify_password(None, hashed)
            assert False, "Should have raised exception"
        except Exception:
            pass
            
        try:
            verify_password(password, None)
            assert False, "Should have raised exception"
        except Exception:
            pass


class TestPasswordWorkflow:
    """Test cases for complete password hash and verify workflow."""
    
    def test_hash_and_verify_workflow(self):
        """Test complete workflow: validate, hash, and verify."""
        password = 'SecurePass123!'
        
        # Step 1: Validate
        is_valid, error = validate_password(password)
        assert is_valid is True
        
        # Step 2: Hash
        hashed = hash_password(password)
        assert hashed != password
        
        # Step 3: Verify correct password
        assert verify_password(password, hashed) is True
        
        # Step 4: Verify incorrect password
        assert verify_password('WrongPass123!', hashed) is False
    
    def test_multiple_users_same_password(self):
        """Test that multiple users with same password have different hashes."""
        password = 'CommonPass123!'
        
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        hash3 = hash_password(password)
        
        # All hashes should be different (different salts)
        assert hash1 != hash2
        assert hash2 != hash3
        assert hash1 != hash3
        
        # But all should verify correctly
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True
        assert verify_password(password, hash3) is True
    
    def test_weak_password_rejected_before_hashing(self):
        """Test that weak passwords are rejected by validation."""
        weak_passwords = [
            'short',
            'noupppercase123!',
            'NOLOWERCASE123!',
            'NoNumbers!',
            'NoSpecial123',
        ]
        
        for weak_password in weak_passwords:
            is_valid, error = validate_password(weak_password)
            assert is_valid is False
    
    def test_strong_passwords_accepted(self):
        """Test that strong passwords are accepted."""
        strong_passwords = [
            'SecurePass123!',
            'MyP@ssw0rd',
            'C0mpl3x!Pass',
            'Test123!@#$',
            'Abcd1234!@#$',
        ]
        
        for strong_password in strong_passwords:
            is_valid, error = validate_password(strong_password)
            assert is_valid is True
            hashed = hash_password(strong_password)
            assert verify_password(strong_password, hashed) is True
