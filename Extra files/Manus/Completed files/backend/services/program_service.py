"""
Program service for the Affiliate Matrix backend.

This module implements the Service Class pattern for program-related operations.
It provides methods for retrieving, creating, updating, and deleting programs,
as well as handling program metrics.
"""

import logging
from typing import Dict, List, Optional, Union, Any
from datetime import datetime
from uuid import uuid4

from fastapi import Depends, Query
from sqlalchemy.orm import Session

from ..core.exceptions import ItemNotFoundError, ValidationError, DatabaseError
from ..models.models import Program, ProgramCreate, ProgramUpdate, ProgramMetrics
from ..config import settings

# Configure logger
logger = logging.getLogger(__name__)


class ProgramService:
    """
    Service class for program-related operations.
    
    This class implements the Service Class pattern and provides methods
    for retrieving, creating, updating, and deleting programs, as well as
    handling program metrics.
    """
    
    def __init__(self, db: Session = None):
        """
        Initialize the program service.
        
        Args:
            db: Database session
        """
        self.db = db
        logger.info("ProgramService initialized")
    
    async def get_programs_list(
        self,
        page: int = 1,
        limit: int = None,
        sort: Optional[str] = None,
        order: Optional[str] = "asc",
        status: Optional[str] = None,
        category: Optional[str] = None,
        tag: Optional[str] = None,
        source: Optional[str] = None,
        search: Optional[str] = None,
        min_commission: Optional[float] = None,
        max_commission: Optional[float] = None,
        min_epc: Optional[float] = None,
        min_conversion_rate: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve a paginated list of programs with filtering and sorting.
        
        Args:
            page: Page number for pagination
            limit: Number of items per page
            sort: Field to sort by
            order: Sort order (asc or desc)
            status: Filter by status
            category: Filter by category
            tag: Filter by tag
            source: Filter by source
            search: Search term for name, description, or URL
            min_commission: Minimum commission value
            max_commission: Maximum commission value
            min_epc: Minimum earnings per click
            min_conversion_rate: Minimum conversion rate
            
        Returns:
            Dictionary containing programs and pagination information
            
        Raises:
            DatabaseError: If there is an error retrieving programs from the database
        """
        try:
            # Use default page size from settings if limit is not provided
            if limit is None:
                limit = settings.DEFAULT_PAGE_SIZE
            
            # Ensure limit doesn't exceed maximum page size
            limit = min(limit, settings.MAX_PAGE_SIZE)
            
            # Calculate offset for pagination
            offset = (page - 1) * limit
            
            logger.info(f"Retrieving programs list (page={page}, limit={limit})")
            
            # In a real implementation, this would query the database
            # For now, we'll return mock data
            
            # Mock implementation - in a real app, this would be a database query
            # SELECT * FROM programs
            # WHERE (status = :status OR :status IS NULL)
            # AND (category @> ARRAY[:category] OR :category IS NULL)
            # AND (tags @> ARRAY[:tag] OR :tag IS NULL)
            # AND (source = :source OR :source IS NULL)
            # AND (name ILIKE :search OR description ILIKE :search OR url ILIKE :search OR :search IS NULL)
            # AND (commission->>'value' >= :min_commission OR :min_commission IS NULL)
            # AND (commission->>'value' <= :max_commission OR :max_commission IS NULL)
            # AND (epc >= :min_epc OR :min_epc IS NULL OR epc IS NULL)
            # AND (conversion_rate >= :min_conversion_rate OR :min_conversion_rate IS NULL OR conversion_rate IS NULL)
            # ORDER BY 
            #   CASE WHEN :sort = 'name' AND :order = 'asc' THEN name END ASC,
            #   CASE WHEN :sort = 'name' AND :order = 'desc' THEN name END DESC,
            #   -- other sort fields
            #   id ASC
            # LIMIT :limit OFFSET :offset;
            
            # INFO: Extend filtering here with additional fields as needed
            # INFO: Consider adding full-text search for more efficient text searching
            # INFO: Add custom scoring logic here for ranking programs by relevance
            
            # Mock data for demonstration
            total = 100  # Total number of programs (would come from COUNT query)
            mock_programs = []
            
            # Generate some mock programs for the current page
            for i in range(min(limit, total - offset)):
                program_id = f"prog_{offset + i + 1}"
                mock_programs.append({
                    "id": program_id,
                    "name": f"Program {offset + i + 1}",
                    "description": f"Description for Program {offset + i + 1}",
                    "url": f"https://example.com/program{offset + i + 1}",
                    "category": ["category1", "category2"],
                    "commission": {
                        "type": "percentage",
                        "value": 10.0,
                        "details": "10% commission on all sales"
                    },
                    "cookieDuration": 30,
                    "paymentFrequency": "monthly",
                    "minimumPayout": 50.0,
                    "paymentMethods": ["paypal", "bank_transfer"],
                    "epc": 1.5,
                    "conversionRate": 2.5,
                    "dateAdded": datetime.now().isoformat(),
                    "lastUpdated": datetime.now().isoformat(),
                    "status": "active",
                    "tags": ["tag1", "tag2"],
                    "source": "manual"
                })
            
            # Calculate total pages
            total_pages = (total + limit - 1) // limit
            
            return {
                "data": mock_programs,
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": total,
                    "total_pages": total_pages
                }
            }
            
        except Exception as e:
            logger.error(f"Error retrieving programs list: {str(e)}")
            raise DatabaseError(message="Error retrieving programs", details=str(e))
    
    async def get_program_by_id(self, program_id: str) -> Dict[str, Any]:
        """
        Retrieve a specific program by ID.
        
        Args:
            program_id: Program ID
            
        Returns:
            Program data
            
        Raises:
            ItemNotFoundError: If the program is not found
            DatabaseError: If there is an error retrieving the program
        """
        try:
            logger.info(f"Retrieving program with ID: {program_id}")
            
            # In a real implementation, this would query the database
            # For now, we'll return mock data or raise an error
            
            # Mock implementation - in a real app, this would be a database query
            # SELECT * FROM programs WHERE id = :program_id;
            
            # For demonstration, let's assume programs with ID starting with "prog_" exist
            if program_id.startswith("prog_"):
                # Mock data for demonstration
                return {
                    "id": program_id,
                    "name": f"Program {program_id}",
                    "description": f"Description for Program {program_id}",
                    "url": f"https://example.com/{program_id}",
                    "category": ["category1", "category2"],
                    "commission": {
                        "type": "percentage",
                        "value": 10.0,
                        "details": "10% commission on all sales"
                    },
                    "cookieDuration": 30,
                    "paymentFrequency": "monthly",
                    "minimumPayout": 50.0,
                    "paymentMethods": ["paypal", "bank_transfer"],
                    "epc": 1.5,
                    "conversionRate": 2.5,
                    "dateAdded": datetime.now().isoformat(),
                    "lastUpdated": datetime.now().isoformat(),
                    "status": "active",
                    "tags": ["tag1", "tag2"],
                    "source": "manual"
                }
            else:
                # Program not found
                raise ItemNotFoundError(item_type="Program", item_id=program_id)
            
        except ItemNotFoundError:
            # Re-raise ItemNotFoundError to be handled by the error handler
            raise
        except Exception as e:
            logger.error(f"Error retrieving program {program_id}: {str(e)}")
            raise DatabaseError(message=f"Error retrieving program {program_id}", details=str(e))
    
    async def create_program(self, program_data: ProgramCreate) -> Dict[str, Any]:
        """
        Create a new program.
        
        Args:
            program_data: Program data
            
        Returns:
            Created program data
            
        Raises:
            ValidationError: If the program data is invalid
            DatabaseError: If there is an error creating the program
        """
        try:
            logger.info("Creating new program")
            
            # In a real implementation, this would insert into the database
            # For now, we'll return mock data
            
            # Mock implementation - in a real app, this would be a database insert
            # INSERT INTO programs (...) VALUES (...) RETURNING *;
            
            # Generate a new program ID
            program_id = f"prog_{uuid4()}"
            
            # Create program with current timestamp
            now = datetime.now().isoformat()
            
            # Combine program data with generated fields
            program = {
                "id": program_id,
                **program_data.dict(),
                "dateAdded": now,
                "lastUpdated": now
            }
            
            logger.info(f"Program created with ID: {program_id}")
            
            return program
            
        except Exception as e:
            logger.error(f"Error creating program: {str(e)}")
            raise DatabaseError(message="Error creating program", details=str(e))
    
    async def update_program(self, program_id: str, program_data: ProgramUpdate) -> Dict[str, Any]:
        """
        Update an existing program.
        
        Args:
            program_id: Program ID
            program_data: Program data to update
            
        Returns:
            Updated program data
            
        Raises:
            ItemNotFoundError: If the program is not found
            ValidationError: If the program data is invalid
            DatabaseError: If there is an error updating the program
        """
        try:
            logger.info(f"Updating program with ID: {program_id}")
            
            # First, check if the program exists
            existing_program = await self.get_program_by_id(program_id)
            
            # In a real implementation, this would update the database
            # For now, we'll return mock data
            
            # Mock implementation - in a real app, this would be a database update
            # UPDATE programs SET ... WHERE id = :program_id RETURNING *;
            
            # Update the program with the new data
            # Only update fields that are provided (exclude_unset=True in dict())
            updated_program = {
                **existing_program,
                **program_data.dict(exclude_unset=True),
                "lastUpdated": datetime.now().isoformat()
            }
            
            logger.info(f"Program {program_id} updated successfully")
            
            return updated_program
            
        except ItemNotFoundError:
            # Re-raise ItemNotFoundError to be handled by the error handler
            raise
        except Exception as e:
            logger.error(f"Error updating program {program_id}: {str(e)}")
            raise DatabaseError(message=f"Error updating program {program_id}", details=str(e))
    
    async def delete_program(self, program_id: str) -> None:
        """
        Delete a program.
        
        Args:
            program_id: Program ID
            
        Raises:
            ItemNotFoundError: If the program is not found
            DatabaseError: If there is an error deleting the program
        """
        try:
            logger.info(f"Deleting program with ID: {program_id}")
            
            # First, check if the program exists
            await self.get_program_by_id(program_id)
            
            # In a real implementation, this would delete from the database
            # For now, we'll just log the deletion
            
            # Mock implementation - in a real app, this would be a database delete
            # DELETE FROM programs WHERE id = :program_id;
            
            logger.info(f"Program {program_id} deleted successfully")
            
        except ItemNotFoundError:
            # Re-raise ItemNotFoundError to be handled by the error handler
            raise
        except Exception as e:
            logger.error(f"Error deleting program {program_id}: {str(e)}")
            raise DatabaseError(message=f"Error deleting program {program_id}", details=str(e))
    
    async def get_program_metrics(self, program_id: str, period: str = "month") -> Dict[str, Any]:
        """
        Retrieve metrics for a specific program.
        
        Args:
            program_id: Program ID
            period: Time period for metrics (day, week, month, year)
            
        Returns:
            Program metrics
            
        Raises:
            ItemNotFoundError: If the program is not found
            ValidationError: If the period is invalid
            DatabaseError: If there is an error retrieving the metrics
        """
        try:
            logger.info(f"Retrieving metrics for program {program_id} (period: {period})")
            
            # First, check if the program exists
            await self.get_program_by_id(program_id)
            
            # Validate period
            valid_periods = ["day", "week", "month", "year"]
            if period not in valid_periods:
                raise ValidationError(message=f"Invalid period: {period}", errors=[
                    {"loc": ["period"], "msg": f"Value must be one of: {', '.join(valid_periods)}"}
                ])
            
            # In a real implementation, this would query the database for metrics
            # For now, we'll return mock data
            
            # Mock implementation - in a real app, this would be a database query
            # SELECT * FROM program_metrics WHERE program_id = :program_id AND period = :period;
            
            # Generate mock metrics based on the period
            mock_metrics = {
                "clicks": 1000 if period == "month" else 250 if period == "week" else 30 if period == "day" else 12000,
                "conversions": 50 if period == "month" else 12 if period == "week" else 2 if period == "day" else 600,
                "revenue": 5000.0 if period == "month" else 1200.0 if period == "week" else 150.0 if period == "day" else 60000.0,
                "roi": 5.0,
                "averag
(Content truncated due to size limit. Use line ranges to read in chunks)