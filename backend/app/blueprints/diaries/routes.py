"""Thought Diary routes blueprint.

This module provides RESTful API endpoints for managing thought diary entries,
including CRUD operations, pagination, AI sentiment analysis integration, and
statistics.
"""

from typing import Tuple, Dict, Any
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from sqlalchemy import desc
from flasgger import swag_from

from app.extensions import db
from app.models import ThoughtDiary
from app.blueprints.diaries.schemas import (
    DiaryCreateSchema,
    DiaryUpdateSchema,
    DiarySchema,
    DiaryListSchema,
    DiaryStatsSchema
)
from app.services.ai_service import analyze_sentiment


# Create blueprint
diaries_bp = Blueprint('diaries', __name__, url_prefix='/diaries')

# Initialize schemas
diary_create_schema = DiaryCreateSchema()
diary_update_schema = DiaryUpdateSchema()
diary_schema = DiarySchema()
diaries_schema = DiarySchema(many=True)
diary_list_schema = DiaryListSchema()
diary_stats_schema = DiaryStatsSchema()


@diaries_bp.route('', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Thought Diaries'],
    'summary': 'List user\'s thought diaries',
    'description': 'Retrieve a paginated list of thought diary entries for the authenticated user, sorted by creation date (newest first)',
    'parameters': [
        {
            'name': 'page',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'default': 1,
            'description': 'Page number (starts at 1)'
        },
        {
            'name': 'per_page',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'default': 10,
            'description': 'Number of items per page (max 100)'
        }
    ],
    'responses': {
        200: {
            'description': 'List of thought diaries',
            'schema': {
                'type': 'object',
                'properties': {
                    'items': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'content': {'type': 'string'},
                                'analyzed_content': {'type': 'string'},
                                'positive_count': {'type': 'integer'},
                                'negative_count': {'type': 'integer'},
                                'created_at': {'type': 'string', 'format': 'date-time'},
                                'updated_at': {'type': 'string', 'format': 'date-time'}
                            }
                        }
                    },
                    'page': {'type': 'integer', 'example': 1},
                    'per_page': {'type': 'integer', 'example': 10},
                    'total': {'type': 'integer', 'example': 50},
                    'pages': {'type': 'integer', 'example': 5}
                }
            }
        },
        401: {
            'description': 'Unauthorized',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'},
                    'code': {'type': 'string', 'example': 'MISSING_TOKEN'}
                }
            }
        }
    },
    'security': [{'Bearer': []}]
})
def list_diaries() -> Tuple[Dict[str, Any], int]:
    """List all thought diaries for the current user with pagination.
    
    Query Parameters:
        page (int): Page number (default: 1).
        per_page (int): Number of items per page (default: 10, max: 100).
        
    Returns:
        Tuple[Dict, int]: JSON response with paginated diaries and status code 200.
        
    Response Format:
        {
            "items": [...],
            "page": 1,
            "per_page": 10,
            "total": 50,
            "pages": 5
        }
        
    Error Responses:
        401: Unauthorized (missing or invalid token)
    """
    # Get current user ID from JWT
    current_user_id = int(get_jwt_identity())
    
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Limit per_page to reasonable maximum
    per_page = min(per_page, 100)
    
    # Query diaries for current user with pagination, sorted by created_at descending
    pagination = ThoughtDiary.query.filter_by(user_id=current_user_id)\
        .order_by(desc(ThoughtDiary.created_at))\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    # Prepare response
    response = {
        'items': diaries_schema.dump(pagination.items),
        'page': pagination.page,
        'per_page': pagination.per_page,
        'total': pagination.total,
        'pages': pagination.pages
    }
    
    return jsonify(response), 200


@diaries_bp.route('', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['Thought Diaries'],
    'summary': 'Create a new thought diary',
    'description': 'Create a new thought diary entry with AI-powered sentiment analysis. The content will be analyzed to identify positive and negative sentiment words.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['content'],
                'properties': {
                    'content': {
                        'type': 'string',
                        'example': 'I felt both excitement and anxious after I got elected to join a team for international math competition.',
                        'description': 'The thought diary entry text (max 5000 characters)'
                    }
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Diary created successfully with AI analysis',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer', 'example': 1},
                    'content': {'type': 'string'},
                    'analyzed_content': {
                        'type': 'string',
                        'example': 'I felt both <span class="positive">excitement</span> and <span class="negative">anxious</span> after...'
                    },
                    'positive_count': {'type': 'integer', 'example': 1},
                    'negative_count': {'type': 'integer', 'example': 1},
                    'created_at': {'type': 'string', 'format': 'date-time'},
                    'updated_at': {'type': 'string', 'format': 'date-time'}
                }
            }
        },
        400: {
            'description': 'Validation error',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'},
                    'code': {'type': 'string', 'example': 'VALIDATION_ERROR'}
                }
            }
        },
        401: {
            'description': 'Unauthorized',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'},
                    'code': {'type': 'string', 'example': 'MISSING_TOKEN'}
                }
            }
        }
    },
    'security': [{'Bearer': []}]
})
def create_diary() -> Tuple[Dict[str, Any], int]:
    """Create a new thought diary entry with AI sentiment analysis.
    
    Request Body:
        {
            "content": "Diary entry text..."
        }
        
    Returns:
        Tuple[Dict, int]: JSON response with created diary and status code 201.
        
    Response Format:
        {
            "id": 1,
            "user_id": 1,
            "content": "Original text...",
            "analyzed_content": "HTML with sentiment markers...",
            "positive_count": 5,
            "negative_count": 2,
            "created_at": "2026-01-12T10:00:00Z",
            "updated_at": "2026-01-12T10:00:00Z"
        }
        
    Error Responses:
        400: Bad request (validation error)
        401: Unauthorized (missing or invalid token)
    """
    # Get current user ID from JWT
    current_user_id = int(get_jwt_identity())
    
    try:
        # Validate request data
        data = diary_create_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({
            'error': 'Validation failed',
            'code': 'VALIDATION_ERROR',
            'details': err.messages
        }), 400
    
    # Analyze sentiment using AI service
    content = data['content']
    analyzed_content, positive_count, negative_count = analyze_sentiment(content)
    
    # Create new diary entry
    diary = ThoughtDiary(
        user_id=current_user_id,
        content=content,
        analyzed_content=analyzed_content,
        positive_count=positive_count,
        negative_count=negative_count
    )
    
    # Save to database
    db.session.add(diary)
    db.session.commit()
    
    return jsonify(diary_schema.dump(diary)), 201


@diaries_bp.route('/<int:diary_id>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Thought Diaries'],
    'summary': 'Get a specific thought diary',
    'description': 'Retrieve a specific thought diary entry by ID. Users can only access their own diaries.',
    'parameters': [
        {
            'name': 'diary_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the diary entry to retrieve'
        }
    ],
    'responses': {
        200: {
            'description': 'Diary retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'content': {'type': 'string'},
                    'analyzed_content': {'type': 'string'},
                    'positive_count': {'type': 'integer'},
                    'negative_count': {'type': 'integer'},
                    'created_at': {'type': 'string', 'format': 'date-time'},
                    'updated_at': {'type': 'string', 'format': 'date-time'}
                }
            }
        },
        401: {
            'description': 'Unauthorized',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'},
                    'code': {'type': 'string', 'example': 'MISSING_TOKEN'}
                }
            }
        },
        403: {
            'description': 'Forbidden - diary belongs to another user',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'You do not have permission to access this diary'},
                    'code': {'type': 'string', 'example': 'FORBIDDEN'}
                }
            }
        },
        404: {
            'description': 'Diary not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Diary not found'},
                    'code': {'type': 'string', 'example': 'NOT_FOUND'}
                }
            }
        }
    },
    'security': [{'Bearer': []}]
})
def get_diary(diary_id: int) -> Tuple[Dict[str, Any], int]:
    """Get a specific thought diary entry by ID.
    
    Args:
        diary_id (int): The ID of the diary entry to retrieve.
        
    Returns:
        Tuple[Dict, int]: JSON response with diary data and status code 200.
        
    Response Format:
        {
            "id": 1,
            "user_id": 1,
            "content": "Original text...",
            "analyzed_content": "HTML with sentiment markers...",
            "positive_count": 5,
            "negative_count": 2,
            "created_at": "2026-01-12T10:00:00Z",
            "updated_at": "2026-01-12T10:00:00Z"
        }
        
    Error Responses:
        401: Unauthorized (missing or invalid token)
        403: Forbidden (diary belongs to another user)
        404: Not found (diary does not exist)
    """
    # Get current user ID from JWT
    current_user_id = int(get_jwt_identity())
    
    # Query diary by ID
    diary = ThoughtDiary.query.get(diary_id)
    
    # Check if diary exists
    if not diary:
        return jsonify({
            'error': 'Diary entry not found',
            'code': 'DIARY_NOT_FOUND'
        }), 404
    
    # Check if diary belongs to current user
    if diary.user_id != current_user_id:
        return jsonify({
            'error': 'You do not have permission to access this diary entry',
            'code': 'FORBIDDEN'
        }), 403
    
    return jsonify(diary_schema.dump(diary)), 200


@diaries_bp.route('/<int:diary_id>', methods=['PUT'])
@jwt_required()
@swag_from({
    'tags': ['Thought Diaries'],
    'summary': 'Update a thought diary',
    'description': 'Update an existing thought diary entry. The content will be re-analyzed for sentiment.',
    'parameters': [
        {
            'name': 'diary_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the diary entry to update'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['content'],
                'properties': {
                    'content': {
                        'type': 'string',
                        'example': 'Updated diary entry text...',
                        'description': 'The updated thought diary entry text (max 5000 characters)'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Diary updated successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'content': {'type': 'string'},
                    'analyzed_content': {'type': 'string'},
                    'positive_count': {'type': 'integer'},
                    'negative_count': {'type': 'integer'},
                    'created_at': {'type': 'string', 'format': 'date-time'},
                    'updated_at': {'type': 'string', 'format': 'date-time'}
                }
            }
        },
        400: {
            'description': 'Validation error',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'},
                    'code': {'type': 'string', 'example': 'VALIDATION_ERROR'}
                }
            }
        },
        401: {
            'description': 'Unauthorized',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'},
                    'code': {'type': 'string', 'example': 'MISSING_TOKEN'}
                }
            }
        },
        403: {
            'description': 'Forbidden',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'},
                    'code': {'type': 'string', 'example': 'FORBIDDEN'}
                }
            }
        },
        404: {
            'description': 'Diary not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'},
                    'code': {'type': 'string', 'example': 'NOT_FOUND'}
                }
            }
        }
    },
    'security': [{'Bearer': []}]
})
def update_diary(diary_id: int) -> Tuple[Dict[str, Any], int]:
    """Update a specific thought diary entry with AI sentiment re-analysis.
    
    Args:
        diary_id (int): The ID of the diary entry to update.
        
    Request Body:
        {
            "content": "Updated diary entry text..."
        }
        
    Returns:
        Tuple[Dict, int]: JSON response with updated diary and status code 200.
        
    Response Format:
        {
            "id": 1,
            "user_id": 1,
            "content": "Updated text...",
            "analyzed_content": "HTML with sentiment markers...",
            "positive_count": 3,
            "negative_count": 4,
            "created_at": "2026-01-12T10:00:00Z",
            "updated_at": "2026-01-12T11:00:00Z"
        }
        
    Error Responses:
        400: Bad request (validation error)
        401: Unauthorized (missing or invalid token)
        403: Forbidden (diary belongs to another user)
        404: Not found (diary does not exist)
    """
    # Get current user ID from JWT
    current_user_id = int(get_jwt_identity())
    
    # Query diary by ID
    diary = ThoughtDiary.query.get(diary_id)
    
    # Check if diary exists
    if not diary:
        return jsonify({
            'error': 'Diary entry not found',
            'code': 'DIARY_NOT_FOUND'
        }), 404
    
    # Check if diary belongs to current user
    if diary.user_id != current_user_id:
        return jsonify({
            'error': 'You do not have permission to update this diary entry',
            'code': 'FORBIDDEN'
        }), 403
    
    try:
        # Validate request data
        data = diary_update_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({
            'error': 'Validation failed',
            'code': 'VALIDATION_ERROR',
            'details': err.messages
        }), 400
    
    # Re-analyze sentiment with updated content
    content = data['content']
    analyzed_content, positive_count, negative_count = analyze_sentiment(content)
    
    # Update diary fields
    diary.content = content
    diary.analyzed_content = analyzed_content
    diary.positive_count = positive_count
    diary.negative_count = negative_count
    
    # Save changes to database
    db.session.commit()
    
    return jsonify(diary_schema.dump(diary)), 200


@diaries_bp.route('/<int:diary_id>', methods=['DELETE'])
@jwt_required()
@swag_from({
    'tags': ['Thought Diaries'],
    'summary': 'Delete a thought diary',
    'description': 'Delete a specific thought diary entry. Users can only delete their own diaries.',
    'parameters': [
        {
            'name': 'diary_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'The ID of the diary entry to delete'
        }
    ],
    'responses': {
        200: {
            'description': 'Diary deleted successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'Diary entry deleted successfully'
                    }
                }
            }
        },
        401: {
            'description': 'Unauthorized',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'},
                    'code': {'type': 'string', 'example': 'MISSING_TOKEN'}
                }
            }
        },
        403: {
            'description': 'Forbidden',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'},
                    'code': {'type': 'string', 'example': 'FORBIDDEN'}
                }
            }
        },
        404: {
            'description': 'Diary not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'},
                    'code': {'type': 'string', 'example': 'NOT_FOUND'}
                }
            }
        }
    },
    'security': [{'Bearer': []}]
})
def delete_diary(diary_id: int) -> Tuple[Dict[str, str], int]:
    """Delete a specific thought diary entry.
    
    Args:
        diary_id (int): The ID of the diary entry to delete.
        
    Returns:
        Tuple[Dict, int]: JSON response with success message and status code 200.
        
    Response Format:
        {
            "message": "Diary entry deleted successfully"
        }
        
    Error Responses:
        401: Unauthorized (missing or invalid token)
        403: Forbidden (diary belongs to another user)
        404: Not found (diary does not exist)
    """
    # Get current user ID from JWT
    current_user_id = int(get_jwt_identity())
    
    # Query diary by ID
    diary = ThoughtDiary.query.get(diary_id)
    
    # Check if diary exists
    if not diary:
        return jsonify({
            'error': 'Diary entry not found',
            'code': 'DIARY_NOT_FOUND'
        }), 404
    
    # Check if diary belongs to current user
    if diary.user_id != current_user_id:
        return jsonify({
            'error': 'You do not have permission to delete this diary entry',
            'code': 'FORBIDDEN'
        }), 403
    
    # Delete diary from database
    db.session.delete(diary)
    db.session.commit()
    
    return jsonify({
        'message': 'Diary entry deleted successfully'
    }), 200


@diaries_bp.route('/stats', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Thought Diaries'],
    'summary': 'Get diary statistics',
    'description': 'Retrieve statistics about the user\'s thought diary entries, including total, positive, negative, and neutral counts',
    'responses': {
        200: {
            'description': 'Statistics retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'total_entries': {
                        'type': 'integer',
                        'example': 50,
                        'description': 'Total number of diary entries'
                    },
                    'positive_entries': {
                        'type': 'integer',
                        'example': 20,
                        'description': 'Number of entries with more positive than negative sentiment'
                    },
                    'negative_entries': {
                        'type': 'integer',
                        'example': 15,
                        'description': 'Number of entries with more negative than positive sentiment'
                    },
                    'neutral_entries': {
                        'type': 'integer',
                        'example': 15,
                        'description': 'Number of entries with equal positive and negative sentiment'
                    }
                }
            }
        },
        401: {
            'description': 'Unauthorized',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'},
                    'code': {'type': 'string', 'example': 'MISSING_TOKEN'}
                }
            }
        }
    },
    'security': [{'Bearer': []}]
})
def get_stats() -> Tuple[Dict[str, int], int]:
    """Get statistics about the current user's thought diaries.
    
    Returns:
        Tuple[Dict, int]: JSON response with statistics and status code 200.
        
    Response Format:
        {
            "total_entries": 50,
            "positive_entries": 20,
            "negative_entries": 15,
            "neutral_entries": 15
        }
        
    Error Responses:
        401: Unauthorized (missing or invalid token)
    """
    # Get current user ID from JWT
    current_user_id = int(get_jwt_identity())
    
    # Query all diaries for current user
    diaries = ThoughtDiary.query.filter_by(user_id=current_user_id).all()
    
    # Calculate statistics
    total_entries = len(diaries)
    positive_entries = sum(1 for d in diaries if d.positive_count > d.negative_count)
    negative_entries = sum(1 for d in diaries if d.negative_count > d.positive_count)
    neutral_entries = sum(1 for d in diaries if d.positive_count == d.negative_count)
    
    # Prepare response
    stats = {
        'total_entries': total_entries,
        'positive_entries': positive_entries,
        'negative_entries': negative_entries,
        'neutral_entries': neutral_entries
    }
    
    return jsonify(stats), 200
