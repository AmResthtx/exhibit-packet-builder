"""Exhibit organization module."""

from datetime import datetime
from typing import List
from loguru import logger


class ExhibitOrganizer:
    """Organizes source documents into exhibits in chronological order."""
    
    def organize_by_date(self, documents: List) -> List:
        """
        Sort documents chronologically and group into exhibits.
        """
        # Sort by extracted date
        sorted_docs = sorted(
            documents,
            key=lambda d: d.extracted_date or datetime.max
        )
        
        logger.info(f"Organized {len(sorted_docs)} documents chronologically")
        return sorted_docs
    
    def generate_exhibit_numbers(self, count: int, prefix: str = "") -> List[str]:
        """
        Generate exhibit numbers (A, B, C... or custom format).
        """
        # Standard alphabet numbering
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        numbers = []
        
        i = 0
        while i < count:
            if i < 26:
                numbers.append(f"{prefix}{letters[i]}")
            else:
                # Handle exhibits beyond Z (AA, AB, etc.)
                first = (i // 26) - 1
                second = i % 26
                numbers.append(f"{prefix}{letters[first]}{letters[second]}")
            i += 1
        
        return numbers
    
    def create_exhibit_titles(self, documents: List, numbers: List) -> dict:
        """
        Create exhibit titles based on document content and date.
        """
        exhibits = {}
        
        for i, (doc, number) in enumerate(zip(documents, numbers)):
            date_str = doc.extracted_date.strftime("%b %d, %Y") if doc.extracted_date else "Unknown Date"
            title = f"{number} - {doc.original_filename.split('.')[0]} ({date_str})"
            
            exhibits[number] = {
                "exhibit_number": number,
                "title": title,
                "source_doc": doc,
                "display_order": i,
            }
        
        return exhibits


# Initialize organizer
exhibit_organizer = ExhibitOrganizer()
