"""Unit tests for validator utility functions.

This module tests:
- Email format validation
- Email normalization
- Input sanitization
"""

from app.utils.validators import validate_email, normalize_email, sanitize_string


class TestValidateEmail:
    """Test cases for email validation function."""
    
    def test_valid_emails(self):
        """Test validation with valid email addresses."""
        valid_emails = [
            'user@example.com',
            'test.user@example.com',
            'test+tag@example.com',
            'user123@example.com',
            'user_name@example.com',
            'user-name@example.com',
            'test@subdomain.example.com',
            'user@example.co.uk',
            'a@example.com',
            'test123@test123.com',
        ]
        
        for email in valid_emails:
            assert validate_email(email) is True, f"Failed for valid email: {email}"
    
    def test_invalid_emails(self):
        """Test validation with invalid email addresses."""
        invalid_emails = [
            '',
            'invalid',
            'invalid@',
            '@example.com',
            'user@',
            'user @example.com',
            'user@example',
            'user..name@example.com',
            'user@.example.com',
            'user@example..com',
            '.user@example.com',
            'user.@example.com',
            'user name@example.com',
            'user@exam ple.com',
        ]
        
        for email in invalid_emails:
            assert validate_email(email) is False, f"Failed for invalid email: {email}"
    
    def test_email_with_special_characters(self):
        """Test validation with special characters in email."""
        # Valid special characters per RFC 5322
        assert validate_email('user+tag@example.com') is True
        assert validate_email('user_name@example.com') is True
        assert validate_email('user-name@example.com') is True
        assert validate_email('user.name@example.com') is True
        assert validate_email('user%name@example.com') is True  # % is allowed in local part
        
        # These might be invalid depending on implementation
        # Skip testing them since RFC 5322 is complex
    
    def test_email_case_sensitivity(self):
        """Test that email validation works regardless of case."""
        assert validate_email('User@Example.com') is True
        assert validate_email('USER@EXAMPLE.COM') is True
        assert validate_email('user@example.com') is True
    
    def test_email_with_numbers(self):
        """Test validation with numbers in email."""
        assert validate_email('user123@example.com') is True
        assert validate_email('123user@example.com') is True
        assert validate_email('test@example123.com') is True
    
    def test_email_none_or_empty(self):
        """Test validation with None or empty string."""
        assert validate_email('') is False
        assert validate_email(None) is False
    
    def test_email_whitespace(self):
        """Test validation with whitespace."""
        assert validate_email(' user@example.com') is False
        assert validate_email('user@example.com ') is False
        assert validate_email(' user@example.com ') is False
    
    def test_email_multiple_at_signs(self):
        """Test validation with multiple @ signs."""
        assert validate_email('user@@example.com') is False
        assert validate_email('user@example@com') is False
    
    def test_email_subdomain(self):
        """Test validation with subdomains."""
        assert validate_email('user@mail.example.com') is True
        assert validate_email('user@mail.sub.example.com') is True
    
    def test_email_top_level_domain(self):
        """Test validation with various top-level domains."""
        assert validate_email('user@example.com') is True
        assert validate_email('user@example.co.uk') is True
        assert validate_email('user@example.io') is True
        assert validate_email('user@example.tech') is True


class TestNormalizeEmail:
    """Test cases for email normalization function."""
    
    def test_normalize_lowercase(self):
        """Test that email is converted to lowercase."""
        assert normalize_email('User@Example.com') == 'user@example.com'
        assert normalize_email('USER@EXAMPLE.COM') == 'user@example.com'
        assert normalize_email('TeSt@ExAmPlE.cOm') == 'test@example.com'
    
    def test_normalize_strip_whitespace(self):
        """Test that whitespace is stripped from email."""
        assert normalize_email(' user@example.com') == 'user@example.com'
        assert normalize_email('user@example.com ') == 'user@example.com'
        assert normalize_email(' user@example.com ') == 'user@example.com'
    
    def test_normalize_already_normalized(self):
        """Test normalizing already normalized email."""
        email = 'user@example.com'
        assert normalize_email(email) == email
    
    def test_normalize_empty_string(self):
        """Test normalizing empty string."""
        assert normalize_email('') == ''
    
    def test_normalize_none(self):
        """Test normalizing None value."""
        result = normalize_email(None)
        # Should return empty string or handle gracefully
        assert result == '' or result is None
    
    def test_normalize_with_plus_sign(self):
        """Test normalizing email with plus sign."""
        assert normalize_email('User+Tag@Example.com') == 'user+tag@example.com'
    
    def test_normalize_with_dots(self):
        """Test normalizing email with dots."""
        assert normalize_email('First.Last@Example.com') == 'first.last@example.com'


class TestSanitizeString:
    """Test cases for string sanitization function."""
    
    def test_sanitize_normal_text(self):
        """Test sanitizing normal text without special characters."""
        text = 'This is normal text'
        assert sanitize_string(text) == text
    
    def test_sanitize_strip_whitespace(self):
        """Test that leading/trailing whitespace is stripped."""
        assert sanitize_string('  text  ') == 'text'
        assert sanitize_string('\ntext\n') == 'text'
        assert sanitize_string('\ttext\t') == 'text'
    
    def test_sanitize_max_length(self):
        """Test truncation with max_length parameter."""
        text = 'This is a long text'
        assert sanitize_string(text, max_length=10) == 'This is a '
        assert sanitize_string(text, max_length=4) == 'This'
    
    def test_sanitize_empty_string(self):
        """Test sanitizing empty string."""
        assert sanitize_string('') == ''
    
    def test_sanitize_none(self):
        """Test sanitizing None value."""
        result = sanitize_string(None)
        # Should return empty string
        assert result == ''
    
    def test_sanitize_special_characters(self):
        """Test sanitizing text with special characters."""
        text = 'Hello & goodbye! @#$%'
        sanitized = sanitize_string(text)
        # Special characters should be preserved
        assert sanitized == text
    
    def test_sanitize_unicode(self):
        """Test sanitizing unicode characters."""
        text = 'Hello 世界 Ñoño'
        sanitized = sanitize_string(text)
        # Unicode should be preserved
        assert '世界' in sanitized
        assert 'Ñoño' in sanitized
    
    def test_sanitize_long_text(self):
        """Test sanitizing very long text."""
        long_text = 'A' * 10000
        sanitized = sanitize_string(long_text)
        # Should handle long text without issues
        assert isinstance(sanitized, str)
        assert len(sanitized) == len(long_text)
    
    def test_sanitize_long_text_with_max(self):
        """Test sanitizing long text with max_length."""
        long_text = 'A' * 10000
        sanitized = sanitize_string(long_text, max_length=100)
        assert len(sanitized) == 100
    
    def test_sanitize_newlines_and_tabs(self):
        """Test sanitizing text with newlines and tabs."""
        text = 'Line1\nLine2\tTabbed'
        sanitized = sanitize_string(text)
        # Internal newlines and tabs should be preserved
        assert 'Line1' in sanitized
        assert 'Line2' in sanitized
    
    def test_sanitize_whitespace_only(self):
        """Test sanitizing string with only whitespace."""
        assert sanitize_string('   ') == ''
        assert sanitize_string('\n\n\n') == ''
        assert sanitize_string('\t\t\t') == ''


class TestValidatorWorkflow:
    """Test cases for complete validator workflow."""
    
    def test_email_validation_and_normalization_workflow(self):
        """Test complete workflow: validate and normalize email."""
        email = ' User+Tag@Example.com '
        
        # Step 1: Normalize
        normalized = normalize_email(email)
        assert normalized == 'user+tag@example.com'
        
        # Step 2: Validate normalized email
        assert validate_email(normalized) is True
    
    def test_reject_invalid_email_early(self):
        """Test that invalid emails are rejected before normalization."""
        invalid_emails = [
            'invalid',
            'no-at-sign',
            '@example.com',
            'user@',
        ]
        
        for email in invalid_emails:
            # Should be rejected by validation
            assert validate_email(email) is False
    
    def test_sanitize_before_storage(self):
        """Test sanitizing input before database storage."""
        user_input = '  Test Content with extra spaces  '
        
        # Sanitize
        sanitized = sanitize_string(user_input)
        
        # Verify sanitization removed extra whitespace
        assert sanitized == 'Test Content with extra spaces'
    
    def test_multiple_inputs_batch_validation(self):
        """Test validating multiple inputs."""
        inputs = [
            ('user1@example.com', True),
            ('user2@example.com', True),
            ('invalid-email', False),
            ('user3@test.com', True),
            ('@example.com', False),
        ]
        
        for email, expected_valid in inputs:
            assert validate_email(email) == expected_valid
    
    def test_email_normalization_consistency(self):
        """Test that normalization is consistent across multiple calls."""
        email = 'User@Example.com'
        
        normalized1 = normalize_email(email)
        normalized2 = normalize_email(email)
        normalized3 = normalize_email(email)
        
        # All normalizations should be identical
        assert normalized1 == normalized2 == normalized3 == 'user@example.com'
    
    def test_string_sanitization_with_max_length(self):
        """Test sanitizing and truncating in one step."""
        long_text = '  ' + 'A' * 1000 + '  '
        
        # Sanitize with max_length
        sanitized = sanitize_string(long_text, max_length=10)
        
        # Should strip whitespace first, then truncate
        assert len(sanitized) == 10
        assert sanitized == 'A' * 10
