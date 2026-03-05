"""Unit tests for thought diary endpoints.

This module tests:
- Listing diaries with pagination
- Creating diaries with AI analysis
- Getting specific diary entries
- Updating diaries with AI re-analysis
- Deleting diary entries
- Getting user statistics
- Authorization checks
"""

from unittest.mock import patch
from app.models.thought_diary import ThoughtDiary


class TestListDiariesEndpoint:
    """Test cases for GET /diaries endpoint."""
    
    def test_list_diaries_empty(self, client, auth_headers):
        """Test listing diaries when user has no entries."""
        response = client.get('/diaries', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'items' in data
        assert 'total' in data
        assert len(data['items']) == 0
        assert data['total'] == 0
    
    def test_list_diaries_with_entries(self, client, auth_headers, test_diary):
        """Test listing diaries with existing entries."""
        response = client.get('/diaries', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'items' in data
        assert len(data['items']) == 1
        assert data['items'][0]['id'] == test_diary.id
        assert data['items'][0]['content'] == test_diary.content
        assert data['items'][0]['analyzed_content'] == test_diary.analyzed_content
    
    def test_list_diaries_pagination(self, client, auth_headers, app, db, test_user):
        """Test pagination with multiple diary entries."""
        with app.app_context():
            # Create 15 diary entries
            for i in range(15):
                diary = ThoughtDiary(
                    user_id=test_user.id,
                    content=f'Diary entry {i}',
                    analyzed_content=f'Diary entry {i}',
                    positive_count=0,
                    negative_count=0
                )
                db.session.add(diary)
            db.session.commit()
        
        # Get first page (default 10 items)
        response = client.get('/diaries', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['items']) == 10
        assert data['page'] == 1
        assert data['per_page'] == 10
        assert data['total'] == 15
        assert data['pages'] == 2
        
        # Get second page
        response = client.get('/diaries?page=2', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['items']) == 5
        assert data['page'] == 2
    
    def test_list_diaries_sorted_by_date_descending(self, client, auth_headers, multiple_diaries):
        """Test that diaries are sorted by created_at descending."""
        response = client.get('/diaries', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['items']) >= 2
        
        # Check that dates are in descending order
        dates = [diary['created_at'] for diary in data['items']]
        assert dates == sorted(dates, reverse=True)
    
    def test_list_diaries_without_auth(self, client):
        """Test listing diaries without authentication."""
        response = client.get('/diaries')
        
        assert response.status_code == 401
    
    def test_list_diaries_custom_page_size(self, client, auth_headers, app, db, test_user):
        """Test pagination with custom page size."""
        with app.app_context():
            # Create 25 diary entries
            for i in range(25):
                diary = ThoughtDiary(
                    user_id=test_user.id,
                    content=f'Diary entry {i}',
                    analyzed_content=f'Diary entry {i}',
                    positive_count=0,
                    negative_count=0
                )
                db.session.add(diary)
            db.session.commit()
        
        # Request with custom page size
        response = client.get('/diaries?per_page=5', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['items']) == 5
        assert data['per_page'] == 5
        assert data['pages'] == 5


class TestCreateDiaryEndpoint:
    """Test cases for POST /diaries endpoint."""
    
    @patch('app.blueprints.diaries.routes.analyze_sentiment')
    def test_create_diary_success(self, mock_analyze, client, auth_headers, app, db):
        """Test successful diary creation with AI analysis."""
        # Mock AI service response - returns tuple of (analyzed_content, positive_count, negative_count)
        mock_analyze.return_value = (
            'I felt <span class="positive">happy</span> today.',
            1,
            0
        )
        
        response = client.post(
            '/diaries',
            headers=auth_headers,
            json={'content': 'I felt happy today.'}
        )
        
        assert response.status_code == 201
        data = response.get_json()
        assert 'id' in data
        assert data['content'] == 'I felt happy today.'
        assert data['analyzed_content'] == 'I felt <span class="positive">happy</span> today.'
        assert data['positive_count'] == 1
        assert data['negative_count'] == 0
        
        # Verify AI service was called
        mock_analyze.assert_called_once_with('I felt happy today.')
    
    @patch('app.blueprints.diaries.routes.analyze_sentiment')
    def test_create_diary_ai_failure_graceful(self, mock_analyze, client, auth_headers):
        """Test diary creation when AI analysis fails."""
        # Mock AI service to return error (returns original content)
        mock_analyze.return_value = (
            'Original content here.',
            0,
            0
        )
        
        response = client.post(
            '/diaries',
            headers=auth_headers,
            json={'content': 'Original content here.'}
        )
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['content'] == 'Original content here.'
        # Should still create diary even if AI fails
        assert data['analyzed_content'] == 'Original content here.'
    
    def test_create_diary_missing_content(self, client, auth_headers):
        """Test creating diary without content field."""
        response = client.post(
            '/diaries',
            headers=auth_headers,
            json={}
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_create_diary_empty_content(self, client, auth_headers):
        """Test creating diary with empty content."""
        response = client.post(
            '/diaries',
            headers=auth_headers,
            json={'content': ''}
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_create_diary_content_too_long(self, client, auth_headers):
        """Test creating diary with content exceeding max length."""
        long_content = 'A' * 10001  # Over 10000 chars
        
        response = client.post(
            '/diaries',
            headers=auth_headers,
            json={'content': long_content}
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_create_diary_without_auth(self, client):
        """Test creating diary without authentication."""
        response = client.post(
            '/diaries',
            json={'content': 'Test content'}
        )
        
        assert response.status_code == 401


class TestGetDiaryEndpoint:
    """Test cases for GET /diaries/<id> endpoint."""
    
    def test_get_diary_success(self, client, auth_headers, test_diary):
        """Test getting a specific diary entry."""
        response = client.get(f'/diaries/{test_diary.id}', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'id' in data
        assert data['id'] == test_diary.id
        assert data['content'] == test_diary.content
        assert data['analyzed_content'] == test_diary.analyzed_content
        assert data['positive_count'] == test_diary.positive_count
        assert data['negative_count'] == test_diary.negative_count
    
    def test_get_diary_not_found(self, client, auth_headers):
        """Test getting non-existent diary."""
        response = client.get('/diaries/99999', headers=auth_headers)
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
    
    def test_get_diary_unauthorized_user(self, client, app, db, test_user2, test_diary):
        """Test getting another user's diary (should return 403)."""
        # Create auth headers for test_user2
        response = client.post(
            '/auth/login',
            json={
                'email': test_user2.email,
                'password': 'TestPassword123!'
            }
        )
        
        other_user_headers = {
            'Authorization': f'Bearer {response.get_json()["access_token"]}'
        }
        
        # Try to access test_user's diary with test_user2's token
        response = client.get(f'/diaries/{test_diary.id}', headers=other_user_headers)
        
        assert response.status_code == 403
        data = response.get_json()
        assert 'error' in data
    
    def test_get_diary_without_auth(self, client, test_diary):
        """Test getting diary without authentication."""
        response = client.get(f'/diaries/{test_diary.id}')
        
        assert response.status_code == 401


class TestUpdateDiaryEndpoint:
    """Test cases for PUT /diaries/<id> endpoint."""
    
    @patch('app.blueprints.diaries.routes.analyze_sentiment')
    def test_update_diary_success(self, mock_analyze, client, auth_headers, test_diary):
        """Test successful diary update with AI re-analysis."""
        # Mock AI service response
        mock_analyze.return_value = (
            'Updated <span class="positive">content</span>.',
            1,
            0
        )
        
        response = client.put(
            f'/diaries/{test_diary.id}',
            headers=auth_headers,
            json={'content': 'Updated content.'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'id' in data
        assert data['content'] == 'Updated content.'
        assert data['analyzed_content'] == 'Updated <span class="positive">content</span>.'
        
        # Verify AI service was called with new content
        mock_analyze.assert_called_once_with('Updated content.')
    
    def test_update_diary_not_found(self, client, auth_headers):
        """Test updating non-existent diary."""
        response = client.put(
            '/diaries/99999',
            headers=auth_headers,
            json={'content': 'Updated content'}
        )
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
    
    def test_update_diary_unauthorized_user(self, client, app, db, test_user2, test_diary):
        """Test updating another user's diary (should return 403)."""
        # Create auth headers for test_user2
        response = client.post(
            '/auth/login',
            json={
                'email': test_user2.email,
                'password': 'TestPassword123!'
            }
        )
        
        other_user_headers = {
            'Authorization': f'Bearer {response.get_json()["access_token"]}'
        }
        
        # Try to update test_user's diary with test_user2's token
        response = client.put(
            f'/diaries/{test_diary.id}',
            headers=other_user_headers,
            json={'content': 'Hacked content'}
        )
        
        assert response.status_code == 403
        data = response.get_json()
        assert 'error' in data
    
    def test_update_diary_empty_content(self, client, auth_headers, test_diary):
        """Test updating diary with empty content."""
        response = client.put(
            f'/diaries/{test_diary.id}',
            headers=auth_headers,
            json={'content': ''}
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_update_diary_without_auth(self, client, test_diary):
        """Test updating diary without authentication."""
        response = client.put(
            f'/diaries/{test_diary.id}',
            json={'content': 'Updated content'}
        )
        
        assert response.status_code == 401


class TestDeleteDiaryEndpoint:
    """Test cases for DELETE /diaries/<id> endpoint."""
    
    def test_delete_diary_success(self, client, auth_headers, test_diary, app, db):
        """Test successful diary deletion."""
        diary_id = test_diary.id
        
        response = client.delete(f'/diaries/{diary_id}', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data
        
        # Verify diary was deleted from database
        with app.app_context():
            deleted_diary = db.session.get(ThoughtDiary, diary_id)
            assert deleted_diary is None
    
    def test_delete_diary_not_found(self, client, auth_headers):
        """Test deleting non-existent diary."""
        response = client.delete('/diaries/99999', headers=auth_headers)
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
    
    def test_delete_diary_unauthorized_user(self, client, app, db, test_user2, test_diary):
        """Test deleting another user's diary (should return 403)."""
        # Create auth headers for test_user2
        response = client.post(
            '/auth/login',
            json={
                'email': test_user2.email,
                'password': 'TestPassword123!'
            }
        )
        
        other_user_headers = {
            'Authorization': f'Bearer {response.get_json()["access_token"]}'
        }
        
        # Try to delete test_user's diary with test_user2's token
        response = client.delete(f'/diaries/{test_diary.id}', headers=other_user_headers)
        
        assert response.status_code == 403
        data = response.get_json()
        assert 'error' in data
        
        # Verify diary was NOT deleted
        with app.app_context():
            diary_still_exists = db.session.get(ThoughtDiary, test_diary.id)
            assert diary_still_exists is not None
    
    def test_delete_diary_without_auth(self, client, test_diary):
        """Test deleting diary without authentication."""
        response = client.delete(f'/diaries/{test_diary.id}')
        
        assert response.status_code == 401


class TestDiaryStatsEndpoint:
    """Test cases for GET /diaries/stats endpoint."""
    
    def test_stats_no_entries(self, client, auth_headers):
        """Test statistics when user has no diary entries."""
        response = client.get('/diaries/stats', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'total_entries' in data
        assert data['total_entries'] == 0
        assert data['positive_entries'] == 0
        assert data['negative_entries'] == 0
        assert data['neutral_entries'] == 0
    
    def test_stats_with_mixed_entries(self, client, auth_headers, multiple_diaries):
        """Test statistics with positive, negative, and neutral entries."""
        response = client.get('/diaries/stats', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'total_entries' in data
        assert data['total_entries'] == 3
        assert data['positive_entries'] == 1  # One positive entry
        assert data['negative_entries'] == 1  # One negative entry
        assert data['neutral_entries'] == 1   # One neutral entry
    
    def test_stats_only_positive(self, client, auth_headers, app, db, test_user):
        """Test statistics with only positive entries."""
        with app.app_context():
            diary = ThoughtDiary(
                user_id=test_user.id,
                content='Great day!',
                analyzed_content='<span class="positive">Great</span> day!',
                positive_count=5,
                negative_count=1
            )
            db.session.add(diary)
            db.session.commit()
        
        response = client.get('/diaries/stats', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['total_entries'] == 1
        assert data['positive_entries'] == 1
        assert data['negative_entries'] == 0
        assert data['neutral_entries'] == 0
    
    def test_stats_only_negative(self, client, auth_headers, app, db, test_user):
        """Test statistics with only negative entries."""
        with app.app_context():
            diary = ThoughtDiary(
                user_id=test_user.id,
                content='Terrible day.',
                analyzed_content='<span class="negative">Terrible</span> day.',
                positive_count=1,
                negative_count=5
            )
            db.session.add(diary)
            db.session.commit()
        
        response = client.get('/diaries/stats', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['total_entries'] == 1
        assert data['positive_entries'] == 0
        assert data['negative_entries'] == 1
        assert data['neutral_entries'] == 0
    
    def test_stats_without_auth(self, client):
        """Test getting statistics without authentication."""
        response = client.get('/diaries/stats')
        
        assert response.status_code == 401


class TestAuthorizationChecks:
    """Test cases for authorization across diary endpoints."""
    
    def test_users_only_see_own_diaries(self, client, app, db, test_user, test_user2):
        """Test that users can only see their own diary entries."""
        with app.app_context():
            # Create diary for test_user
            diary1 = ThoughtDiary(
                user_id=test_user.id,
                content='User 1 diary',
                analyzed_content='User 1 diary',
                positive_count=0,
                negative_count=0
            )
            # Create diary for test_user2
            diary2 = ThoughtDiary(
                user_id=test_user2.id,
                content='User 2 diary',
                analyzed_content='User 2 diary',
                positive_count=0,
                negative_count=0
            )
            db.session.add(diary1)
            db.session.add(diary2)
            db.session.commit()
        
        # Login as test_user
        response = client.post(
            '/auth/login',
            json={
                'email': test_user.email,
                'password': 'TestPassword123!'
            }
        )
        user1_headers = {
            'Authorization': f'Bearer {response.get_json()["access_token"]}'
        }
        
        # Get diaries for test_user
        response = client.get('/diaries', headers=user1_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        # Should only see their own diary
        assert len(data['items']) == 1
        assert data['items'][0]['content'] == 'User 1 diary'
